from datetime import timedelta, datetime

import jwt
from fastapi import FastAPI, HTTPException, Depends
from fastapi_pagination import Page, paginate, add_pagination
from fastapi_permissions.example import Permission, get_current_user
from pydantic import BaseModel
from starlette import status
from typesystem import Union

from application import models
from application.models import ManagerDB
from application.schemas import Task, Manager, ItemListResource
from application.database import engine, SessionLocal
from application.auth import AuthHandler

from sqlalchemy.orm import Session
#########################
from fastapi_permissions import (
    Allow,
    Authenticated,
    Deny,
    Everyone,
    configure_permissions,
    list_permissions,
)



app = FastAPI(title="FastAPI_Client")
models.Base.metadata.create_all(bind=engine)
auth_handler = AuthHandler()


def get_db():
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()


users = []


#####Auth jwt
@app.post('/register', status_code=201)
def register(auth_details: Manager, db: Session = Depends(get_db)):
    if any(x['username'] == auth_details.username for x in users):
        raise HTTPException(status_code=400, detail='Username is taken')
    hashed_password = auth_handler.get_password_hash(auth_details.password)
    # users.append({
    #     'username': auth_details.username,
    #     'password': hashed_password
    # })
    manager_model = models.ManagerDB()
    manager_model.username = auth_details.username
    manager_model.first_name = auth_details.first_name
    manager_model.last_name = auth_details.last_name
    # manager_model.email = manager.email
    manager_model.password = hashed_password
    manager_model.created_at = auth_details.created_at
    manager_model.updated_at = auth_details.updated_at

    db.add(manager_model)
    db.commit()
    return auth_details



@app.post('/login')
def login(auth_details: Manager, db: Session = Depends(get_db)):
    user = auth_details.username, auth_details.password
    token = auth_handler.encode_token(user)
    return {'token': token}


# @app.get('/unprotected')
# def unprotected():
#     return {'hello': 'world'}


@app.get('/protected')
def protected(username=Depends(auth_handler.auth_wrapper)):
    return {'name': username}

# TASK URL




@app.get('/api/all-tasks/', response_model=Page[Task], tags=["GET Methods"])
async def get_all_tasks( db: Session = Depends(get_db)): #ilr: ItemListResource = Permission("view", ItemListResource),
    return paginate(db.query(models.TaskDB).all())

add_pagination(app)


@app.get('/api/task/{task_id}', tags=["GET Methods"])
async def get_task(task_id: int, db: Session = Depends(get_db)):
    return db.query(models.TaskDB).filter(models.TaskDB.id == task_id).first()


@app.post("/api/create-task", tags=["POST Methods"])
async def create_task(task: Task, db: Session = Depends(get_db)):
    task_model = models.TaskDB()
    task_model.name = task.name
    task_model.description = task.description
    task_model.status = task.status
    task_model.created_at = task.created_at
    task_model.updated_at = task.updated_at

    # task_model.managers = task.manager

    db.add(task_model)
    db.commit()

    return task


@app.put("/api/task/{task_id}", tags=["PUT Methods"])
def update_task(task_id: int, task: Task, db: Session = Depends(get_db)):
    task_model = db.query(models.TaskDB).filter(models.TaskDB.id == task_id).first()
    if task_model is None:
        raise HTTPException(
            status_code=404,
            detail=f"ID {task_id} : Does not exist"
        )

    task_model.name = task.name
    task_model.description = task.description
    task_model.status = task.status
    # task_model.created_at = task.created_at
    task_model.updated_at = task.updated_at
    # task_model.managers = managerss.managers

    db.add(task_model)
    db.commit()

    return task


@app.delete("/api/task/{task_id}", tags=["DELETE Methods"])
def delete_task(task_id: int, db: Session = Depends(get_db)):
    task_model = db.query(models.TaskDB).filter(models.TaskDB.id == task_id).first()

    if task_model is None:
        raise HTTPException(
            status_code=404,
            detail=f"ID {task_id} : Does not exist"
        )

    db.query(models.TaskDB).filter(models.TaskDB.id == task_id).delete()

    db.commit()


# @app.patch("/update")
# async def update_profile(task_id: int, task: Task, db: Session = Depends(get_db)):
#     task_model = db.query(models.TaskDB).filter(models.TaskDB.id == task_id).first()
#
#     task_model.update(task.dict(exclude_unset=True))

# for key, value in TaskDB.items():
#     print("key ----", key)
#     print("value ----", value)
#
#     setattr(task, key, value)

# db.commit()
# return task_model

# Manager URL
@app.get('/api/all-managers/', response_model=Page[Manager], tags=["GET Methods"])
async def get_all_managers(db: Session = Depends(get_db)):
    return paginate(db.query(models.ManagerDB).all())


add_pagination(app)


@app.get('/api/manager/{manager_id}', tags=["GET Methods"])
async def get_manager(manager_id: int, db: Session = Depends(get_db)):
    return db.query(models.ManagerDB).filter(models.ManagerDB.id == manager_id).first()


@app.post("/api/create-manager", tags=["POST Methods"])
def create_manager(manager: Manager, db: Session = Depends(get_db)):
    manager_model = models.ManagerDB()
    manager_model.username = manager.username
    manager_model.first_name = manager.first_name
    manager_model.last_name = manager.last_name
    # manager_model.email = manager.email
    manager_model.password = manager.password
    manager_model.created_at = manager.created_at
    manager_model.updated_at = manager.updated_at

    db.add(manager_model)
    db.commit()

    return manager


@app.put("/api/manager/{manager_id}", tags=["PUT Methods"])
def update_manager(manager_id: int, manager: Manager, db: Session = Depends(get_db)):
    manager_model = db.query(models.ManagerDB).filter(models.ManagerDB.id == manager_id).first()

    if manager_model is None:
        raise HTTPException(
            status_code=404,
            detail=f"ID {manager_id} : Does not exist"
        )
    manager_model.username = manager.username
    manager_model.first_name = manager.first_name
    manager_model.last_name = manager.last_name
    manager_model.email = manager.email
    manager_model.password = manager.password
    manager_model.created_at = manager.created_at
    manager_model.updated_at = manager.updated_at

    db.add(manager_model)
    db.commit()

    return manager


@app.delete("/api/manager/{manager_id}", tags=["DELETE Methods"])
def delete_manager(manager_id: int, db: Session = Depends(get_db)):
    manager_model = db.query(models.ManagerDB).filter(models.ManagerDB.id == manager_id).first()

    if manager_model is None:
        raise HTTPException(
            status_code=404,
            detail=f"ID {manager_id} : Does not exist"
        )

    db.query(models.ManagerDB).filter(models.ManagerDB.id == manager_id).delete()

    db.commit()
