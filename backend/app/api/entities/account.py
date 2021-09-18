# Python class represent the entities
from typing import Optional
from pydantic import BaseModel
from datetime import datetime
from decimal import Decimal
from fastapi.param_functions import Form


class Token(BaseModel):
    token_type: Optional[str] = 'bearer'
    access_token: Optional[str]
    refresh_token: Optional[str]
    expire_token: Optional[datetime]
    expire_refresh_token: Optional[datetime]


class TokenCreate(BaseModel):
    user_id: Optional[int]
    email: Optional[str]


class TokenPayload(BaseModel):
    user_id: Optional[int]
    email: Optional[str]


class SigUpRequest:
    def __init__(
        self,
        email: str = Form(...),
        password: str = Form(...),
        re_password: str = Form(...),
        first_name: Optional[str] = Form(None),
        last_name: Optional[str] = Form(None),
        phone: Optional[str] = Form(None),

    ):
        self.email = email
        self.password = password
        self.re_password = re_password
        self.first_name = first_name
        self.last_name = last_name
        self.phone = phone
