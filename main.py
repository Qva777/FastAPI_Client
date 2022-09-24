from fastapi import FastAPI, HTTPException, Query, Body, Depends
from typing import Optional, List, Union
from application import models
from application.schemas import Task
from application.database import engine, SessionLocal
from sqlalchemy.orm import Session

app = FastAPI(title="FastAPI_Client")
models.Base.metadata.create_all(bind=engine)


def get_db():
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()


# TASK URL
@app.get('/api/all-tasks/', tags=["GET Methods"])
async def get_all_tasks(db: Session = Depends(get_db)):
    return db.query(models.TaskDB).all()


@app.get('/api/task/{task_id}', tags=["GET Methods"])
async def get_task(task_id: int, db: Session = Depends(get_db)):
    return db.query(models.TaskDB).filter(models.TaskDB.id == task_id).first()


@app.post("/api/create-task", tags=["POST Methods"])
def create_book(task: Task, db: Session = Depends(get_db)):
    task_model = models.TaskDB()
    task_model.name = task.name
    task_model.description = task.description
    task_model.status = task.status
    task_model.created_at = task.created_at
    task_model.updated_at = task.updated_at

    db.add(task_model)
    db.commit()

    return task


@app.put("/api/task/{task_id}", tags=["PUT Methods"])
def update_book(task_id: int, task: Task, db: Session = Depends(get_db)):
    task_model = db.query(models.TaskDB).filter(models.TaskDB.id == task_id).first()

    if task_model is None:
        raise HTTPException(
            status_code=404,
            detail=f"ID {task_id} : Does not exist"
        )

    task_model.name = task.name
    task_model.description = task.description
    task_model.status = task.status
    task_model.created_at = task.created_at
    task_model.updated_at = task.updated_at

    db.add(task_model)
    db.commit()

    return task


@app.delete("/api/task/{task_id}", tags=["DELETE Methods"])
def delete_book(task_id: int, db: Session = Depends(get_db)):
    task_model = db.query(models.TaskDB).filter(models.TaskDB.id == task_id).first()

    if task_model is None:
        raise HTTPException(
            status_code=404,
            detail=f"ID {task_id} : Does not exist"
        )

    db.query(models.TaskDB).filter(models.TaskDB.id == task_id).delete()

    db.commit()



# Manager URL
# @app.get('/api/all-managers/', tags=["GET Methods"])
# async def get_all_tasks(db: Session = Depends(get_db)):
#     return db.query(models.TaskDB).all()
#
#
# @app.get('/api/manager/{manager_id}', tags=["GET Methods"])
# async def get_task(task_id: int, db: Session = Depends(get_db)):
#     return db.query(models.TaskDB).filter(models.TaskDB.id == task_id).first()
#
#
# @app.post("/api/create-manager", tags=["POST Methods"])
# def create_book(task: Task, db: Session = Depends(get_db)):
#     manager_model = models.TaskDB()
#     manager_model.name = task.name
#     manager_model.description = task.description
#     manager_model.created_at = task.created_at
#     manager_model.updated_at = task.updated_at
#
#     db.add(manager_model)
#     db.commit()
#
#     return task
#
#
# @app.put("/api/manager/{manager_id}", tags=["PUT Methods"])
# def update_book(task_id: int, task: Task, db: Session = Depends(get_db)):
#     task_model = db.query(models.TaskDB).filter(models.TaskDB.id == task_id).first()
#
#     if task_model is None:
#         raise HTTPException(
#             status_code=404,
#             detail=f"ID {task_id} : Does not exist"
#         )
#
#     task_model.name = task.name
#     task_model.description = task.description
#     task_model.created_at = task.created_at
#     task_model.updated_at = task.updated_at
#
#     db.add(task_model)
#     db.commit()
#
#     return task
#
#
# @app.delete("/api/manager/{manager_id}", tags=["DELETE Methods"])
# def delete_book(task_id: int, db: Session = Depends(get_db)):
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