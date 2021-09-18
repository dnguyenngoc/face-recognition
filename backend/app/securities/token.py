from re import L

from fastapi.exceptions import HTTPException
from settings import config
from datetime import (
    datetime, timedelta
)
from Crypto.Cipher import AES
from passlib.utils.pbkdf2 import pbkdf2_hmac
import binascii
from jose import JWTError, jwt
from sqlalchemy.orm import Session
from fastapi import Depends
from databases.db import get_db
from fastapi import Security
from fastapi.security import OAuth2PasswordBearer
from api.entities import account as account_entity
from databases.logic import user as user_logic


secrect = config.SECRET_KEY.encode(config.ENCODE_TYPE)
algorithm=config.ALGORITHM
salt = config.SALT  
digest = config.DIGEST
rounds = config.ROUNDS
secret_key = pbkdf2_hmac(digest, secrect, salt, rounds)
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/account/login/access-token")


def get_current_user(db: Session = Depends(get_db), token: str = Security(oauth2_scheme)):
    try:
        token = decrypt(token)
        payload = jwt.decode(token, config.SECRET_KEY, algorithms=[algorithm])
        token_data = account_entity.TokenPayload(**payload)
    except JWTError:
        raise HTTPException(status_code=401, detail="token expire")
    user = user_logic.get_user_by_user_id_and_user_name_and_email_and_role_id_join_role(db, token_data.user_id, token_data.user_name, token_data.email, token_data.role_id)
    if not user:
        raise HTTPException(status_code=403, detail="token wrong")
    return user


def create_access_token(data):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=config.ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, config.SECRET_KEY, algorithm=algorithm)
    return encrypt(encoded_jwt)


def create_fresh_token(data):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=config.ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, config.SECRET_KEY, algorithm=algorithm)
    return encrypt(encoded_jwt)


def encrypt(msg):
    ase_ciper = AES.new(secret_key, AES.MODE_GCM)
    cipher_text, auth_tag = ase_ciper.encrypt_and_digest(msg.encode(config.ENCODE_TYPE))
    end = binascii.hexlify(cipher_text + auth_tag + ase_ciper.nonce).decode(config.ENCODE_TYPE)
    return end


def decrypt(msg):
    try:
        byte_msg = binascii.unhexlify(msg.encode(config.ENCODE_TYPE))
        cipher_text = byte_msg[:-2*config.SALT_SIZE]
        auth_tag = byte_msg[-2*config.SALT_SIZE:-config.SALT_SIZE]
        nonce = byte_msg[-config.SALT_SIZE:]
        ase_ciper = AES.new(secret_key, AES.MODE_GCM, nonce)
        decrypted = ase_ciper.decrypt_and_verify(cipher_text, auth_tag)
        end = decrypted.decode(config.ENCODE_TYPE)
        return end
    except: 
        return False
