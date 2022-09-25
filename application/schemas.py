from datetime import datetime
from enum import Enum
from typing import Union

from pydantic import BaseModel, root_validator, Field, EmailStr
from uuid import UUID


class Status(str, Enum):
    CREATED = "1"
    IN_PROGRESS = "2"
    COMPLETED = "3"


class Task(BaseModel):
    name: Union[str, None] = Field(..., title="The name of the task", max_length=64)
    description: Union[str, None] = Field(..., title="The description of the item", max_length=250)
    status: Status
    created_at: datetime = datetime.now()
    updated_at: datetime = datetime.now()

    class Config:
        validate_assignment = True

    @root_validator
    def number_validator(cls, values):
        values["updated_at"] = datetime.now()
        return values


class Manager(BaseModel):
    username:Union[str, None] = Field(..., title="The description of the item", max_length=250)
    first_name: Union[str, None] = Field(..., title="The description of the item", max_length=250)
    last_name: Union[str, None] = Field(..., title="The description of the item", max_length=250)
    # email: EmailStr
    password: Union[str, None] = Field(..., title="The description of the item", max_length=250)
    created_at: datetime = datetime.now()
    updated_at: datetime = datetime.now()
    # is_staff =
    # tasks =

    class Config:
        validate_assignment = True

    # @root_validator
    # def number_validator(cls, values):
    #     values["updated_at"] = datetime.now()
    #     return values