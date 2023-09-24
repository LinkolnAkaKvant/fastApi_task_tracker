import enum

from sqlalchemy import Column, Integer, String, ForeignKey, Enum, DateTime
from sqlalchemy.orm import relationship

from app.db.base import Base


class TaskStatus(enum.Enum):
    not_started = 1
    in_progress = 2
    completed = 3


class Task(Base):
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    task_name = Column(String(100), nullable=False)
    description = Column(String(200), nullable=False)
    parent_task_id = Column(Integer, ForeignKey("tasks.id"))
    employee_id = Column(Integer, ForeignKey("employees.id"))
    deadline = Column(DateTime, nullable=False)
    status = Column(Enum(TaskStatus), default=TaskStatus.not_started)
    employee = relationship("Employee", back_populates="tasks")
    parent_task = relationship("Task", remote_side=id, backref="children")
