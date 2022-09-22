from datetime import datetime
from time import sleep

from pydantic import BaseModel, Field, root_validator
from typing import Union


class Task(BaseModel):
    name: Union[str, None] = Field(..., title="The name of the task", max_length=64)
    description: Union[str, None] = Field(..., title="The description of the item", max_length=250)
    # status:
    created_at: datetime = datetime.now()
    updated_at: datetime = datetime.now()

    class Config:
        validate_assignment = True

    @root_validator
    def number_validator(cls, values):
        values["updated_at"] = datetime.now()
        return values
