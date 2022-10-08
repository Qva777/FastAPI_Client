""" File with authentication methods """
import os
import dotenv

import jwt
from jwt import PyJWTError

from fastapi import HTTPException
from fastapi_permissions import Everyone, configure_permissions
from fastapi.security import OAuth2PasswordBearer
from fastapi import Depends

from application.schemas import *
from application import models
from application.models import ManagerDB
from application.database import engine, SessionLocal

from datetime import timedelta
from sqlalchemy.orm import Session
from pydantic import ValidationError
from starlette.status import HTTP_401_UNAUTHORIZED
# UPDATE secret key
dotenv_file = os.path.join( ".env")
if os.path.isfile(dotenv_file):
    dotenv.load_dotenv(dotenv_file)
SECRET_KEY = os.environ['SECRET_KEY']
# SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/token")

models.Base.metadata.create_all(bind=engine)


def get_db():
    """ Connecting to database """
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()


async def get_current_user(db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=HTTP_401_UNAUTHORIZED,
        detail="Could not Validate Credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
    except (PyJWTError, ValidationError):
        raise credentials_exception
    user = db.query(models.ManagerDB).filter(models.ManagerDB.username == username).first()
    if user is None:
        raise credentials_exception
    return user


def get_token_with_username(db, form_data):
    success = authenticate_user(db, form_data.username, form_data.password)
    if not success:
        raise HTTPException(status_code=400, detail="Incorrect Username or Password")
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(data={"sub": form_data.username}, expires_delta=access_token_expires)
    return {"access_token": access_token, "token_type": "bearer"}


def verify_password(plain_password, hashed_password):
    return plain_password == hashed_password


def get_user(db, username: str):
    if db.username == username:
        print("user---", username)
    return ManagerDB


def authenticate_user(db, username: str, password: str):
    user = db.query(models.ManagerDB).filter(models.ManagerDB.username == username).first()
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user


def create_access_token(*, data: dict, expires_delta: timedelta):
    """ Create token """
    to_encode = data.copy()
    expire = datetime.utcnow() + expires_delta
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def get_active_principals(user: Manager = Depends(get_current_user)):
    if user:
        # user is logged in
        principals = [Everyone, Authenticated]
        principals.extend(getattr(user, "principals", []))
    else:
        # user is not logged in
        principals = [Everyone]
    return principals


Permission = configure_permissions(get_active_principals)
