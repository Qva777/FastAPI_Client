from fastapi_permissions.example import get_current_user
from sqlmodel import Session

from application import models
from application.database import SessionLocal
from application.models import ManagerDB
from application.schemas import Manager#, Item

# from sqlalchemy.orm import Session

from datetime import datetime, timedelta

import jwt
from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from jwt import PyJWTError
from passlib.context import CryptContext
from pydantic import ValidationError
from starlette.status import HTTP_401_UNAUTHORIZED

from fastapi_permissions import (
    Authenticated,
    Everyone,
)


SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/token")


def verify_password(plain_password, hashed_password):
    return plain_password == hashed_password


def get_user(db, username: str):
    if db.username == username:
        print("user---", username)
    return ManagerDB


# def get_item(item_id: int):
#     if item_id in ManagerDB:  ### manager - fake_items_db
#         item_dict = ManagerDB[item_id]  ### manager - fake_items_db
#         return Item(**item_dict)


def authenticate_user(db, username: str, password: str):
    # user = get_user(db, username)
    user = db.query(models.ManagerDB).filter(models.ManagerDB.username == username).first()
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user


def create_access_token(*, data: dict, expires_delta: timedelta):
    to_encode = data.copy()
    expire = datetime.utcnow() + expires_delta
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


# async def get_current_user(db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)):
#     credentials_exception = HTTPException(
#         status_code=HTTP_401_UNAUTHORIZED,
#         detail="Could not validate credentials",
#         headers={"WWW-Authenticate": "Bearer"},
#     )
#     try:
#         payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
#         username: str = payload.get("sub")
#         if username is None:
#             raise credentials_exception
#     except (PyJWTError, ValidationError):
#         raise credentials_exception
#     user = db.query(models.ManagerDB).filter(models.ManagerDB.username == username).first()
#     if user is None:
#         raise credentials_exception
#     return user


def get_active_principals(user: Manager = Depends(get_current_user)):
    if user:
        # user is logged in
        principals = [Everyone, Authenticated]
        principals.extend(getattr(user, "principals", []))
    else:
        # user is not logged in
        principals = [Everyone]
    return principals
