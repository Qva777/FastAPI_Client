"""File that stores functions for working with the task """

from fastapi import HTTPException
from application import models
# from application.models import ManagerDB, TaskDB


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
    if db.query(models.TaskDB).filter(models.TaskDB.name == task_model.name).first():
        raise HTTPException(
            status_code=500,
            detail=f"This name is already in use"
        )
    task_model.description = task.description
    task_model.status = task.status
    task_model.created_at = task.created_at
    task_model.updated_at = task.updated_at

    # task_model.managers = task.managers

    db.add(task_model)
    db.commit()


def put_info_task(task_model, task, db):
    """ Добавит к таску менеджера """
    # task_model = TaskDB
    # task = schemas
    # manager_model = models.task_manager

    task_model.name = task.name
    task_model.description = task.description
    task_model.status = task.status
    task_model.created_at = task.created_at
    task_model.updated_at = task.updated_at
    # *
    # manager_model.manager_id = task.managers


    db.add(task_model)
    db.commit()


# def save_info_task_manager(task_manager, task, db):
#     """ Fields that are stored in the task table in the database """
#     for manager in task.managers:
#         task_manager.name = task.name
#         task_manager.username = manager
#         db.add(task_manager)
#         db.commit()

    # task_model.managers = task.managers
