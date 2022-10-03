from fastapi_pagination import Page, paginate, add_pagination

from application import models
from application.crud import save_info_manager, search_manager_by_username
from application.models import ManagerDB
from application.schemas import Task, Manager, ItemListResource, ManagerInDB, Item, Token
from application.database import engine, SessionLocal

from sqlalchemy.orm import Session

from datetime import datetime, timedelta

import jwt
from fastapi import Depends, FastAPI, HTTPException
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jwt import PyJWTError
from passlib.context import CryptContext
from pydantic import ValidationError
from starlette.status import HTTP_401_UNAUTHORIZED

from fastapi_permissions import (
    Allow,
    Authenticated,
    Deny,
    Everyone,
    configure_permissions,
    list_permissions,
)

app = FastAPI(title="FastAPI_Client")
# oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/token")
models.Base.metadata.create_all(bind=engine)

# SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
# ALGORITHM = "HS256"
# ACCESS_TOKEN_EXPIRE_MINUTES = 30
# pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def get_db():
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()


# ManagerDB = {
# "bob": {
#         "username": "bob",
#         "full_name": "Bobby Bob",
#         "email": "bob@example.com",
#         "hashed_password": pwd_context.hash("secret"),
#         "principals": ["user:bob", "role:admin"],
#     },
# }
#
# db = ManagerDB()

#
# def verify_password(plain_password, hashed_password):
#     return plain_password == hashed_password
#
#
# def get_user(db, username: str):
#     if db.username == username:
#         print("user---", username)
#     return ManagerDB
#
#
# def get_item(item_id: int):
#     if item_id in ManagerDB:  ### manager - fake_items_db
#         item_dict = ManagerDB[item_id]  ### manager - fake_items_db
#         return Item(**item_dict)
#
#
# def authenticate_user(db, username: str, password: str):
#     # user = get_user(db, username)
#     user = db.query(models.ManagerDB).filter(models.ManagerDB.username == username).first()
#     if not user:
#         return False
#     if not verify_password(password, user.hashed_password):
#         return False
#     return user
#
#
# def create_access_token(*, data: dict, expires_delta: timedelta):
#     to_encode = data.copy()
#     expire = datetime.utcnow() + expires_delta
#     to_encode.update({"exp": expire})
#     encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
#     return encoded_jwt
#
#
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
#
#
#
# def get_active_principals(user: Manager = Depends(get_current_user)):
#     if user:
#         # user is logged in
#         principals = [Everyone, Authenticated]
#         principals.extend(getattr(user, "principals", []))
#     else:
#         # user is not logged in
#         principals = [Everyone]
#     return principals


Permission = configure_permissions(get_active_principals)


# Login token url
@app.post("/token", response_model=Token, tags=["Get Token"])
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    """ Login/Get JSON Web Token """
    success = authenticate_user(db, form_data.username, form_data.password)
    if not success:
        raise HTTPException(status_code=400, detail="Incorrect username or password")
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(data={"sub": form_data.username}, expires_delta=access_token_expires)
    return {"access_token": access_token, "token_type": "bearer"}


# TASK URL
# @app.get('/api/all-tasks/', response_model=Page[Task], tags=["GET Methods"])
# async def get_all_tasks( db: Session = Depends(get_db)): #ilr: ItemListResource = Permission("view", ItemListResource),
#     return paginate(db.query(models.TaskDB).all())
#
# add_pagination(app)
#
#
# @app.get('/api/task/{task_id}', tags=["GET Methods"])
# async def get_task(task_id: int, db: Session = Depends(get_db)):
#     return db.query(models.TaskDB).filter(models.TaskDB.id == task_id).first()
#
#
# @app.post("/api/create-task", tags=["POST Methods"])
# async def create_task(task: Task, db: Session = Depends(get_db)):
#     task_model = models.TaskDB()
#     task_model.name = task.name
#     task_model.description = task.description
#     task_model.status = task.status
#     task_model.created_at = task.created_at
#     task_model.updated_at = task.updated_at
#
#     # task_model.managers = task.manager
#
#     db.add(task_model)
#     db.commit()
#
#     return task
#
#
# @app.put("/api/task/{task_id}", tags=["PUT Methods"])
# def update_task(task_id: int, task: Task, db: Session = Depends(get_db)):
#     task_model = db.query(models.TaskDB).filter(models.TaskDB.id == task_id).first()
#     if task_model is None:
#         raise HTTPException(
#             status_code=404,
#             detail=f"ID {task_id} : Does not exist"
#         )
#
#     task_model.name = task.name
#     task_model.description = task.description
#     task_model.status = task.status
#     # task_model.created_at = task.created_at
#     task_model.updated_at = task.updated_at
#     # task_model.managers = managerss.managers
#
#     db.add(task_model)
#     db.commit()
#
#     return task
#
#
# @app.delete("/api/task/{task_id}", tags=["DELETE Methods"])
# def delete_task(task_id: int, db: Session = Depends(get_db)):
#     task_model = db.query(models.TaskDB).filter(models.TaskDB.id == task_id).first()
#
#     if task_model is None:
#         raise HTTPException(
#             status_code=404,
#             detail=f"ID {task_id} : Does not exist"
#         )
#
#     db.query(models.TaskDB).filter(models.TaskDB.id == task_id).delete()
#
#     db.commit()
#
#
# # @app.patch("/update")
# # async def update_profile(task_id: int, task: Task, db: Session = Depends(get_db)):
# #     task_model = db.query(models.TaskDB).filter(models.TaskDB.id == task_id).first()
# #
# #     task_model.update(task.dict(exclude_unset=True))
#
# # for key, value in TaskDB.items():
# #     print("key ----", key)
# #     print("value ----", value)
# #
# #     setattr(task, key, value)
#
# # db.commit()
# # return task_model
#
# # Manager URL


# Manager URLS
@app.post("/api/create-manager", tags=["POST Methods"])
async def create_manager(manager: ManagerInDB, db: Session = Depends(get_db)):
    """ Create user """
    manager_model = models.ManagerDB()
    save_info_manager(manager_model, manager, db)
    return manager


@app.get("/me/", response_model=Manager, tags=["GET Methods"])
async def read_users_me(current_user: Manager = Depends(get_current_user)):
    """ Info about self """
    return current_user


@app.get('/api/manager/{manager_username}', tags=["GET Methods"])
async def get_manager(username: str, db: Session = Depends(get_db),
                      lr: ItemListResource = Permission("view", ItemListResource)):
    """ Get info about user by username """
    return db.query(models.ManagerDB).filter(models.ManagerDB.username == username).first()


@app.put("/api/manager/{manager_username}", tags=["PUT Methods"])
async def update_manager(username: str, manager: ManagerInDB, db: Session = Depends(get_db),
                         lr: ItemListResource = Permission("view", ItemListResource)):
    """ Update info user """
    save_info_manager(search_manager_by_username(username, db), manager, db)
    return manager


@app.delete("/api/manager/{manager_username}", tags=["DELETE Methods"])
async def delete_manager(username: str, db: Session = Depends(get_db),
                         lr: ItemListResource = Permission("view", ItemListResource)):
    """ Delete user by username """
    search_manager_by_username(username, db)
    db.query(models.ManagerDB).filter(models.ManagerDB.username == username).delete()
    db.commit()
    return "Object removed"


@app.get('/api/all-managers/', response_model=Page[ManagerInDB], tags=["GET Methods"])
async def get_all_managers(db: Session = Depends(get_db)):
    """ Get info about all users """
    return paginate(db.query(models.ManagerDB).all())


add_pagination(app)
