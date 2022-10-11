""" Schema json file """

from enum import Enum
from typing import Union, List
from datetime import datetime

from pydantic import BaseModel, root_validator, Field, EmailStr
from fastapi_permissions import Allow, Authenticated
from passlib.context import CryptContext


class Status(int, Enum):
    """ Task statuses """
    CREATED = 1
    IN_PROGRESS = 2
    COMPLETED = 3


class Manager(BaseModel):
    """ manager model schema """
    username: Union[str, None] = Field(..., title="Username", max_length=64)
    first_name: Union[str, None] = Field(..., title="First name", max_length=250)
    last_name: Union[str, None] = Field(..., title="Last name", max_length=250)
    email: Union[EmailStr, None] = Field(..., title="Email", )  ############
    created_at: datetime = datetime.now()
    updated_at: datetime = datetime.now()

    # tasks: List[int] = []#####

    class Config:
        """Providing configurations"""
        validate_assignment = True
        orm_mode = True

    @root_validator
    def number_validator(cls, values):
        """Update Validation"""
        values["updated_at"] = datetime.now()
        return values


class ManagerInDB(Manager):
    """  manager's hashed password """
    hashed_password: str


class Task(BaseModel):
    """task model schema"""
    name: Union[str, None] = Field(..., title="The name of the task", max_length=64)
    description: Union[str, None] = Field(..., title="The description of the task", max_length=250)
    status: Union[Status] = Field(..., title="The description of the task")
    # managers: List[ta]
    created_at: datetime = datetime.now()
    updated_at: datetime = datetime.now()

    # managers: List[int] = []#####

    class Config:
        """Providing configurations"""
        validate_assignment = True
        orm_mode = True

    @root_validator
    def number_validator(cls, values):
        if values["updated_at"]:
            values["updated_at"] = datetime.now()
        else:
            values["updated_at"] = values["created_at"]
        return values


class Token(BaseModel):
    """ token class """
    access_token: str
    token_type: str


class TokenData(BaseModel):
    """ token class """
    username: str = None


class ItemListResource:
    """ Permissions """
    __acl__ = [(Allow, Authenticated, "view")]

# class ManagerOut(ManagerInDB):
#     tasks: List[Task]
#
#
# class TaskOut(Task):
#     managers: List[Manager]

# class TaskRead(HeroBase):
#     id: int
#
# class ManageroRead(Manager):
#     team: Optional[TeamRead] = None
#
# class TaskRead(HeroBase):
#     id: int
# class TaskReadWith(TaskRead):
#     heroes: List[HeroRead] = []


