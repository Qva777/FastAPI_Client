"""File that stores functions for working with the manager """

from fastapi import HTTPException
from application import models
from application.auth import pwd_context
from application.models import ManagerDB


def search_manager_by_username(username, db):
    """ Search manager by username """
    manager_model = db.query(models.ManagerDB).filter(models.ManagerDB.username == username).first()

    if manager_model is None:
        raise HTTPException(
            status_code=404,
            detail=f"{username} : Does not exist"
        )
    return manager_model


def save_info_manager(manager_model, manager, db):
    """ Fields that are stored in the manager table in the database """

    manager_model.username = manager.username
    if db.query(models.ManagerDB).filter(models.ManagerDB.username == manager_model.username).first():
        raise HTTPException(
            status_code=500,
            detail=f"This username is already in use"
        )
    manager_model.hashed_password = pwd_context.hash(manager.hashed_password)
    manager_model.first_name = manager.first_name
    manager_model.last_name = manager.last_name
    manager_model.email = manager.email
    manager_model.created_at = manager.created_at
    manager_model.updated_at = manager.updated_at
    # manager_model.tasks = manager.tasks

    db.add(manager_model)
    db.commit()
