from fastapi import HTTPException
from application import models


def search_task_by_name(name, db):
    """ Search task by name """
    task_model = db.query(models.TaskDB).filter(models.TaskDB.name == name).first()

    if task_model is None:
        raise HTTPException(
            status_code=404,
            detail=f"Task {name} : Does not exist"
        )
    return task_model


def save_info_task(task_model, task, db):
    """ Fields that are stored in the task table in the database """
    task_model.name = task.name
    task_model.description = task.description
    task_model.status = task.status
    task_model.created_at = task.created_at
    task_model.updated_at = task.updated_at

    db.add(task_model)
    db.commit()
