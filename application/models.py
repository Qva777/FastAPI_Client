from datetime import datetime
from time import sleep

from fastapi import Query, Form
from pydantic import BaseModel, Field, root_validator
from typing import Union

from enum import Enum
class Status(str, Enum):
    eu = "eu"
    us = "us"
    cn = "cn"
    ru = "ru"
async def get_countries(_q: str = Query("eu", enum=["eu", "us", "cn", "ru"])):
    return {"selected": _q}

class Task(BaseModel):
    name: Union[str, None] = Field(..., title="The name of the task", max_length=64)
    description: Union[str, None] = Field(..., title="The description of the item", max_length=250)
    q: str = Query("eu", enum=["eu", "us", "cn", "ru"])
    created_at: datetime = datetime.now()
    updated_at: datetime = datetime.now()

    class Config:
        validate_assignment = True

    @root_validator
    def number_validator(cls, values):
        values["updated_at"] = datetime.now()
        return values


class Manager(BaseModel):
    username: Union[str, None] = Field(..., title="The name of the task", max_length=64)
    first_name: Union[str, None] = Field(..., title="The description of the item", max_length=250)
#     last_name:
#     email:
#     password:
#     created_at: datetime = datetime.now()
#     updated_at: datetime = datetime.now()
#
#     class Config:
#         validate_assignment = True
#
#     @root_validator
#     def number_validator(cls, values):
#         values["updated_at"] = datetime.now()
#         return values