""" File of models stored in the database """

from sqlalchemy import Column, ForeignKey, Integer, String, DateTime, sql, Table
# from sqlalchemy.orm import relationship

from application.database import Base, engine
from typing import List


# task_manager = Table("task_manager", Base.metadata,
#                      Column("task_name", ForeignKey("task.name"), primary_key=True),
#                      Column("manager_username", ForeignKey("manager.username"), primary_key=True))


class TaskDB(Base):
    """Таблица моделей задач в базе данных"""
    __tablename__ = 'task'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True)
    description = Column(String)
    status = Column(Integer, ForeignKey('task.status'))
    created_at = Column(DateTime(timezone=True), server_default=sql.func.now())
    updated_at = Column(DateTime(timezone=True), server_default=sql.func.now())

    # managers = relationship("Manager", secondary=task_manager, back_populates="manager")


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

    # tasks = relationship("Task", secondary=task_manager, back_populates="task")


Base.metadata.create_all(engine)
