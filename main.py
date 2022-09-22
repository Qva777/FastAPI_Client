from fastapi import FastAPI, HTTPException
from typing import Optional, List

from application.models import Task

app = FastAPI(title="FastAPI_Client")
all_task = []


# @app.get('/')
# async def home():
#     return {"Hello": "World"}
# return {
#         "item_id": item_id,
#         "start_datetime": start_datetime,
#         "end_datetime": end_datetime,
#         "repeat_at": repeat_at,
#         "process_after": process_after,
#         "start_process": start_process,
#         "duration": duration,
#     }


@app.post('/todo/')
async def create_todo(task: Task):
    all_task.append(task)
    return task


@app.get('/todo/', response_model=List[Task])
async def get_all_todos():
    return all_task


@app.get('/todo/{id}')
async def get_todo(id: int):
    try:
        return all_task[id]
    except:
        raise HTTPException(status_code=404, detail="Todo Not Found")


@app.put('/todo/{id}')
async def update_todo(id: int, task: Task):
    try:
        all_task[id] = task
        return all_task[id]

    except:
        raise HTTPException(status_code=404, detail="Task Not Found")


@app.delete('/todo/{id}')
async def delete_todo(id: int):
    try:
        obj = all_task[id]
        all_task.pop(id)
        return obj
    except:
        raise HTTPException(status_code=404, detail="Task Not Found")
