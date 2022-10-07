""" File of models stored in the database """

from sqlalchemy import Column, ForeignKey, Integer, String, DateTime, sql
from application.database import Base, engine
from typing import List

# task_manager = Table("task_manager", Base.metadata,
#                        Column("task_id", ForeignKey("task.id"), primary_key=True),
#                        Column("manager_id", ForeignKey("manager.id"), primary_key=True))
from application.schemas import Manager


class TaskDB(Base):
    """Таблица моделей задач в базе данных"""
    __tablename__ = 'task'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True)
    description = Column(String)
    status = Column(Integer, ForeignKey('task.status'))
    created_at = Column(DateTime(timezone=True), server_default=sql.func.now())
    updated_at = Column(DateTime(timezone=True), server_default=sql.func.now())

    # managers = relationship("ManagerDB", secondary=task_manager, back_populates="tasks")


class ManagerDB(Base):
    """Таблица моделей менеджеров в базе данных"""
    __tablename__ = 'manager'

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True)
    first_name = Column(String)
    last_name = Column(String)
    email = Column(String)
    hashed_password = Column(String)
    principals: List[str] = []
    created_at = Column(DateTime(timezone=True), server_default=sql.func.now())
    updated_at = Column(DateTime(timezone=True), server_default=sql.func.now())
    # is_active = Column(Boolean, default=False)
    # tasks = relationship("TaskDB", secondary=task_manager, back_populates="managers")


Base.metadata.create_all(engine)
