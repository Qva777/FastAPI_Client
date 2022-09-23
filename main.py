from fastapi import FastAPI, HTTPException, Query
from typing import Optional, List

from application.models import Task, Manager

app = FastAPI(title="FastAPI_Client")
all_task = []
all_managers = []

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


@app.post('/api/{items}')
async def get_countries(task: Task, manager: Manager, items):
    if items == task:
        all_task.append(task)
        return task
    elif items == manager:
        all_managers.append(manager)
        return manager






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
