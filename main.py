from datetime import datetime
from enum import Enum

from fastapi import FastAPI, HTTPException, Query
from typing import Optional, List, Union

# from application.models import Task, Manager
from pydantic import root_validator, BaseModel, Field, validator

app = FastAPI(title="FastAPI_Client")
all_task = []
all_managers = []


class Status(str, Enum):
    CREATED = "1"
    IN_PROGRESS = "2"
    COMPLETED = "3"


class Task(BaseModel):
    name: Union[str, None] = Field(..., title="The name of the task", max_length=64)
    description: Union[str, None] = Field(..., title="The description of the item", max_length=250)
    status: str = Query(Status.CREATED, enum=[Status.CREATED, Status.IN_PROGRESS, Status.COMPLETED])
    created_at: datetime = datetime.now()
    updated_at: datetime = datetime.now()

    class Config:
        validate_assignment = True

    @root_validator
    def number_validator(cls, values):
        values["updated_at"] = datetime.now()
        return values


@app.post('/api')
async def get_countries(task: Task, ):
    # if q1 == task.q:
    all_task.append(task)
    return task


# else:
#     return {"Status doesn't exist"}


@app.get('/all-tasks/', response_model=List[Task])
async def get_all_tasks():
    return all_task


@app.get('/task/{id}')
async def get_task(id: int):
    try:
        return all_task[id]
    except:
        raise HTTPException(status_code=404, detail="Todo Not Found")


@app.put('/task/{id}')
async def update_task(id: int, task: Task):
    try:
        all_task[id] = task
        return all_task[id]
    except:
        raise HTTPException(status_code=404, detail="Task Not Found")


@app.delete('/task/{id}')
async def delete_task(id: int):
    try:
        obj = all_task[id]
        all_task.pop(id)
        return obj
    except:
        raise HTTPException(status_code=404, detail="Task Not Found")
