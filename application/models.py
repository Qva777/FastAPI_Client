""" File of models stored in the database """

from sqlalchemy import Column, ForeignKey, Integer, String, DateTime, sql, Table
from sqlalchemy.orm import relationship

from application.database import Base, engine

Base.metadata.create_all(engine)

# # class BookAuthor(Base):
# #     __tablename__ = 'task_manager'
# #     task_id = Column(ForeignKey('task.id'), primary_key=True)
# #     manager_id = Column(ForeignKey('manager.id'), primary_key=True)
#
#
# class ManagerDB(Base):
#     """Таблица моделей менеджеров в базе данных"""
#     __tablename__ = 'manager'
#     id = Column(Integer, primary_key=True, index=True)
#     username = Column(String, unique=True)
#     first_name = Column(String)
#     last_name = Column(String)
#     email = Column(String)
#     hashed_password = Column(String)
#     created_at = Column(DateTime(timezone=True), server_default=sql.func.now())
#     updated_at = Column(DateTime(timezone=True), server_default=sql.func.now())
#
#     # tasks = relationship("TaskDB", secondary="task_manager", back_populates="manager")  # подключение задачам
#
#
# class TaskDB(Base):
#     """Таблица моделей задач в базе данных"""
#     __tablename__ = 'task'
#     id = Column(Integer, primary_key=True, index=True)
#     name = Column(String, unique=True)
#     description = Column(String)
#     status = Column(Integer, ForeignKey('task.status'))
#     created_at = Column(DateTime(timezone=True), server_default=sql.func.now())
#     updated_at = Column(DateTime(timezone=True), server_default=sql.func.now())
#
#     # manager = Column(Integer, ForeignKey('manager.id'))
#     # managers = relationship("ManagerDB", secondary="task_manager", back_populates="task")  # подключение менеджерам
#


task_manager = Table("task_manager", Base.metadata,  #
                     Column("task_id", ForeignKey("task.id")),
                     Column("manager_id", ForeignKey("manager.id")))  # Промнжуточная таблица


class ManagerDB(Base):
    """Таблица моделей менеджеров в базе данных"""
    __tablename__ = 'manager'
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True)
    first_name = Column(String)
    last_name = Column(String)
    email = Column(String)
    hashed_password = Column(String)
    created_at = Column(DateTime(timezone=True), server_default=sql.func.now())
    updated_at = Column(DateTime(timezone=True), server_default=sql.func.now())

    # tasks = relationship("TaskDB", secondary="task_manager")# подключение задачам


class TaskDB(Base):
    """Таблица моделей задач в базе данных"""
    __tablename__ = 'task'
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True)
    description = Column(String)
    status = Column(Integer, ForeignKey('task.status'))
    created_at = Column(DateTime(timezone=True), server_default=sql.func.now())
    updated_at = Column(DateTime(timezone=True), server_default=sql.func.now())
