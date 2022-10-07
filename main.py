""" some text....  """

from jwt import PyJWTError
from sqlalchemy.orm import Session

from fastapi import FastAPI, HTTPException
from fastapi_pagination import Page, paginate, add_pagination
from fastapi_permissions import configure_permissions
from fastapi.security import OAuth2PasswordRequestForm

from pydantic import ValidationError
from starlette.status import HTTP_401_UNAUTHORIZED

from application.task_methods import save_info_task, search_task_by_name
from application.manager_methods import save_info_manager, search_manager_by_username
from application.auth import *
from application.schemas import *
from application.database import engine, SessionLocal
from application import models

app = FastAPI(title="FastAPI_Client")
models.Base.metadata.create_all(bind=engine)


def get_db():
    """ Connecting to database """
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()


# ManagerDB = {
# "bob": {
#         "username": "bob",
#         "full_name": "Bobby Bob",
#         "email": "bob@example.com",
#         "hashed_password": pwd_context.hash("secret"),
#         "principals": ["user:bob", "role:admin"],
#     },
# }


async def get_current_user(db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
    except (PyJWTError, ValidationError):
        raise credentials_exception
    user = db.query(models.ManagerDB).filter(models.ManagerDB.username == username).first()
    if user is None:
        raise credentials_exception
    return user


Permission = configure_permissions(get_active_principals)


# Login token url
@app.post("/token", response_model=Token, tags=["Get Token"])
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    """ Login/Get JSON Web Token """
    success = authenticate_user(db, form_data.username, form_data.password)
    if not success:
        raise HTTPException(status_code=400, detail="Incorrect username or password")
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(data={"sub": form_data.username}, expires_delta=access_token_expires)
    return {"access_token": access_token, "token_type": "bearer"}


# TASK URL
@app.get('/api/all-tasks/', response_model=Page[Task], tags=["GET Methods"])
async def get_all_tasks(db: Session = Depends(get_db)):
    return paginate(db.query(models.TaskDB).all())


add_pagination(app)


@app.get('/api/task/{name}', tags=["GET Methods"])
async def get_task(name: str, db: Session = Depends(get_db),
                   ilr: ItemListResource = Permission("view", ItemListResource)):
    return db.query(models.TaskDB).filter(models.TaskDB.name == name).first()


@app.post("/api/create-task", tags=["POST Methods"])
async def create_task(task: Task, db: Session = Depends(get_db)):
    task_model = models.TaskDB()
    save_info_task(task_model, task, db)
    return task


@app.put("/api/task/{task_id}", tags=["PUT Methods"])
def update_task(name: str, task: Task, db: Session = Depends(get_db),
                ilr: ItemListResource = Permission("view", ItemListResource)):
    save_info_task(search_task_by_name(name, db), task, db)
    return task


@app.delete("/api/task/{task_id}", tags=["DELETE Methods"])
def delete_task(name: str, db: Session = Depends(get_db),
                ilr: ItemListResource = Permission("view", ItemListResource)):
    """ Delete task by name """
    search_task_by_name(name, db)
    db.query(models.TaskDB).filter(models.TaskDB.name == name).delete()
    db.commit()


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


@app.get('/api/manager/{manager_username}', tags=["GET Methods"])
async def get_manager(username: str, db: Session = Depends(get_db),
                      lr: ItemListResource = Permission("view", ItemListResource)):
    """ Get info about user by username """
    return db.query(models.ManagerDB).filter(models.ManagerDB.username == username).first()


@app.put("/api/manager/{manager_username}", tags=["PUT Methods"])
async def update_manager(username: str, manager: ManagerInDB, db: Session = Depends(get_db),
                         lr: ItemListResource = Permission("view", ItemListResource)):
    """ Update info user """
    save_info_manager(search_manager_by_username(username, db), manager, db)
    return manager


@app.delete("/api/manager/{manager_username}", tags=["DELETE Methods"])
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
# @app.patch("/update")
# async def update_profile(task_id: int, task: Task, db: Session = Depends(get_db)):
#     task_model = db.query(models.TaskDB).filter(models.TaskDB.id == task_id).first()
#
#     task_model.update(task.dict(exclude_unset=True))

# for key, value in TaskDB.items():
#     print("key ----", key)
#     print("value ----", value)
#
#     setattr(task, key, value)

# db.commit()
# return task_model
