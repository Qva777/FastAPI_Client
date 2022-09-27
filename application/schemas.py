from datetime import datetime
from enum import Enum
from typing import Union, List

from uuid import UUID
from pydantic import BaseModel, root_validator, Field, EmailStr


class Status(int, Enum):
    """Стытусы задач"""
    CREATED = 1
    IN_PROGRESS = 2
    COMPLETED = 3

class Manager(BaseModel):
    """Шаблон модели менеджера"""
    # id: int
    username: Union[str, None] = Field(..., title="Username", max_length=64)
    first_name: Union[str, None] = Field(..., title="First name", max_length=250)
    last_name: Union[str, None] = Field(..., title="Last name", max_length=250)
    email: Union[EmailStr, None] = Field(..., title="Email", )  #############
    password: Union[str, None] = Field(..., title="Password", max_length=250)
    created_at: datetime = datetime.now()
    updated_at: datetime = datetime.now()


    class Config:
        """Предоставления конфигураций"""
        validate_assignment = True
        orm_mode = True

    @root_validator
    def number_validator(cls, values):
        """Валидация обновлений"""
        values["updated_at"] = datetime.now()
        return values


class Task(BaseModel):
    """Шаблон модели задач"""
    # id: int
    name: Union[str, None] = Field(..., title="The name of the task", max_length=64)
    description: Union[str, None] = Field(..., title="The description of the task", max_length=250)
    status: Union[Status] = Field(..., title="The description of the task")
    created_at: datetime = datetime.now()
    updated_at: datetime = datetime.now()
    # manager: List[Manager]
    class Config:
        """Предоставления конфигураций"""
        validate_assignment = True
        orm_mode = True

    @root_validator
    def number_validator(cls, values):
        if values["updated_at"]:
            values["updated_at"] = datetime.now()
        else:
            values["updated_at"] = values["created_at"]
        return values

    # @root_validator
    # def number_validator(cls, values):
    #     values["updated_at"] = datetime.now()
    #     return values



#
# class TaskOut(BaseModel):
#     manager_id: Manager
#
#
# class TaskOut11(BaseModel):
#     manager_info: List[Manager]
#
#
# class ManagerOut(Manager):
#     task_info: List[Task]
