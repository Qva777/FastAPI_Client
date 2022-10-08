""" Main file with URL/Methods  """

from application.auth import *
from application.schemas import *
from application import models

app = FastAPI(title="FastAPI_Client")


# Login token url
@app.post("/token", response_model=Token, tags=["Get Token"])
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    """ Login/Get JSON Web Token """
    return get_token_with_username(db, form_data)


# TASK URL
@app.get('/api/all-tasks/', response_model=Page[Task], tags=["GET Methods"])
async def get_all_tasks(db: Session = Depends(get_db)):
    """ GET all tasks in db """
    return paginate(db.query(models.TaskDB).all())


@app.get('/api/task/{name}', tags=["GET Methods"])
async def get_task(name: str, db: Session = Depends(get_db),
                   ilr: ItemListResource = Permission("view", ItemListResource)):
    """ GET task by name """
    return db.query(models.TaskDB).filter(models.TaskDB.name == name).first()


@app.post("/api/create-task", tags=["POST Methods"])
async def create_task(task: Task, db: Session = Depends(get_db)):
    """ Create task """
    task_model = models.TaskDB()
    save_info_task(task_model, task, db)
    return task


@app.put("/api/task/{name}", tags=["PUT Methods"])
def update_task(name: str, task: Task, db: Session = Depends(get_db),
                ilr: ItemListResource = Permission("view", ItemListResource)):
    """ Update task """
    save_info_task(search_task_by_name(name, db), task, db)
    return task


@app.delete("/api/task/{name}", tags=["DELETE Methods"])
def delete_task(name: str, db: Session = Depends(get_db),
                ilr: ItemListResource = Permission("view", ItemListResource)):
    """ Delete task by name """
    search_task_by_name(name, db)
    db.query(models.TaskDB).filter(models.TaskDB.name == name).delete()
    db.commit()
    return "Object removed"


# Manager URLS
@app.post("/api/create-manager", tags=["POST Methods"])
async def create_manager(manager: ManagerInDB, db: Session = Depends(get_db)):
    """ Create user """
    manager_model = models.ManagerDB()
    save_info_manager(manager_model, manager, db)
    return manager


@app.get("/me/", response_model=Manager, tags=["GET Methods"])
async def read_users_me(current_user: Manager = Depends(get_current_user)):
    """ Info about self """
    return current_user


@app.get('/api/manager/{username}', tags=["GET Methods"])
async def get_manager(username: str, db: Session = Depends(get_db),
                      lr: ItemListResource = Permission("view", ItemListResource)):
    """ Get info about user by username """
    return db.query(models.ManagerDB).filter(models.ManagerDB.username == username).first()


@app.put("/api/manager/{username}", tags=["PUT Methods"])
async def update_manager(username: str, manager: ManagerInDB, db: Session = Depends(get_db),
                         lr: ItemListResource = Permission("view", ItemListResource)):
    """ Update info user """
    save_info_manager(search_manager_by_username(username, db), manager, db)
    return manager


@app.delete("/api/manager/{username}", tags=["DELETE Methods"])
async def delete_manager(username: str, db: Session = Depends(get_db),
                         lr: ItemListResource = Permission("view", ItemListResource)):
    """ Delete user by username """
    search_manager_by_username(username, db)
    db.query(models.ManagerDB).filter(models.ManagerDB.username == username).delete()
    db.commit()
    return "Object removed"


@app.get('/api/all-managers/', response_model=Page[ManagerInDB], tags=["GET Methods"])
async def get_all_managers(db: Session = Depends(get_db)):
    """ Get info about all users """
    return paginate(db.query(models.ManagerDB).all())


add_pagination(app)
