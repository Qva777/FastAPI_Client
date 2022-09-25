from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, DateTime, Enum
from sqlalchemy.orm import relationship

from application.database import Base


class TaskDB(Base):
    """Таблица моделей задач в базе данных"""
    __tablename__ = 'task'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True)
    description = Column(String)
    status = Column(Integer, ForeignKey('task.status'))
    created_at = Column(DateTime)
    updated_at = Column(DateTime)


class ManagerDB(Base):
    """Таблица моделей менеджеров в базе данных"""
    __tablename__ = 'manager'

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True)
    first_name = Column(String)
    last_name = Column(String)
    # email = Column(String, unique=True)
    password = Column(String)
    created_at = Column(DateTime)
    updated_at = Column(DateTime)

# from datetime import datetime
# from time import sleep
#
# from fastapi import Query, Form
# from pydantic import BaseModel, Field, root_validator, validator
# from typing import Union
#
# from enum import Enum
# class Status(str, Enum):
#     eu = "eu"
#     us = "us"
#     cn = "cn"
#     ru = "ru"
# # async def get_countries(_q: str = Query("eu", enum=["eu", "us", "cn", "ru"])):
# #     return {"selected": _q}
#
# class Task(BaseModel):
#     name: Union[str, None] = Field(..., title="The name of the task", max_length=64)
#     description: Union[str, None] = Field(..., title="The description of the item", max_length=250)
#     q: str = Query("eu", enum=["eu", "us", "cn", "ru"])
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
#
#     @validator('q')
#     async def get_countries(cls, q: str = Query("eu", enum=["eu", "us", "cn", "ru"])):
#         return {"selected": q}
#
#
# class Manager(BaseModel):
#     username: Union[str, None] = Field(..., title="The name of the task", max_length=64)
#     first_name: Union[str, None] = Field(..., title="The description of the item", max_length=250)
# #     last_name:
# #     email:
# #     password:
# #     created_at: datetime = datetime.now()
# #     updated_at: datetime = datetime.now()
# #
# #     class Config:
# #         validate_assignment = True
# #
# #     @root_validator
# #     def number_validator(cls, values):
# #         values["updated_at"] = datetime.now()
# #         return values
