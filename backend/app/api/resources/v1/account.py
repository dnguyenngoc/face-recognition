# import
import logging
from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException
from fastapi.param_functions import Form
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.sql.expression import desc

# import
from databases.db import get_db
from databases.logic import user as user_logic
from databases.crud import user as user_crud


from api.entities import account as account_entity
from databases.entities import user as user_entity

from securities import token as token_helper
from helpers import time as time_helper
from datetime import timedelta
from securities import password as password_helper

router = APIRouter()


@router.post("/login/access-token", response_model = account_entity.Token)
def login( 
    db_session: Session = Depends(get_db),
    form_data: OAuth2PasswordRequestForm = Depends(OAuth2PasswordRequestForm)
):

    user_db = user_logic.get_user_by_email(db_session, form_data.username)
    if not user_db:
        raise HTTPException(status_code=400, detail="Incorrect username")
    if password_helper.verify_password(form_data.password, user_db.password) == False:
        raise HTTPException(status_code=400, detail="Incorrect password")
    now = time_helper.now_utc()
    token_create = account_entity.TokenCreate(**user_db.__dict__)
    access_token = token_helper.create_access_token(token_create.__dict__)
    refresh_token = token_helper.create_fresh_token(token_create.__dict__)
    token = account_entity.Token(
        access_token = access_token, 
        refresh_token = refresh_token,
        expire_token= now + timedelta(days=3),
        expire_refresh_token= now + timedelta(days = 7)
    )
    return token


@router.post("/login/refresh-token", response_model = account_entity.Token)
def refresh_token( 
    *, 
    db_session: Session = Depends(get_db),
    refresh_token: str = Form(...),
):
    token = token_helper.decrypt(refresh_token)
    if token == False:
        raise HTTPException(status_code=403, detail="token wrong")
    user_db = token_helper.get_current_user(db_session, token)
    now = time_helper.now_utc()
    token_create = account_entity.TokenCreate(**user_db.__dict__)
    access_token = token_helper.create_access_token(token_create.__dict__)
    refresh_token = token_helper.create_fresh_token(token_create.__dict__)
    token = account_entity.Token(
        access_token = access_token, 
        refresh_token = refresh_token,
        expire_token= now + timedelta(days=3),
        expire_refresh_token= now + timedelta(days = 7)
    )
    return token


@router.post("/sigup")
def create_account(
     *, 
    db_session: Session = Depends(get_db),
    form_data: account_entity.SigUpRequest =  Depends(account_entity.SigUpRequest)
):
    if form_data.password != form_data.re_password:
        raise HTTPException(status_code=400, detail="password not match!")
    user_db = user_logic.get_user_by_email(db_session, form_data.email)
    
    if user_db != None:
        raise HTTPException(status_code=400, detail="user existed!")
    user = user_entity.UserCreate(**form_data.__dict__)
    user.password = password_helper.get_password_hash(user.password)
    user_create = user_crud.create(db =db_session, form_data=user)
    return user_create.__dict__