from datetime import datetime
from enum import Enum
from typing import Union

from pydantic import BaseModel, root_validator, Field, EmailStr


class Status(str, Enum):
    CREATED = "1"
    IN_PROGRESS = "2"
    COMPLETED = "3"


class Task(BaseModel):
    name: Union[str, None] = Field(..., title="The name of the task", max_length=64)
    description: Union[str, None] = Field(..., title="The description of the task", max_length=250)
    status: Union[Status, None] = Field(..., title="The description of the task", max_length=250)
    created_at: datetime = datetime.now()
    updated_at: datetime = datetime.now()

    class Config:
        # validate_assignment = True
        orm_mode = True

    @root_validator
    def number_validator(cls, values):
        values["updated_at"] = datetime.now()
        return values


class Manager(BaseModel):
    username: Union[str, None] = Field(..., title="Username", max_length=64)
    first_name: Union[str, None] = Field(..., title="First name", max_length=250)
    last_name: Union[str, None] = Field(..., title="Last name", max_length=250)
    email: Union[EmailStr, None] = Field(title="Email")
    password: Union[str, None] = Field(..., title="Password", max_length=250)
    created_at: datetime = datetime.now()
    updated_at: datetime = datetime.now()

    # tasks =

    class Config:
        validate_assignment = True

    @root_validator
    def number_validator(cls, values):
        values["updated_at"] = datetime.now()
        return values