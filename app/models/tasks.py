import enum

from sqlalchemy import Column, Integer, String, ForeignKey, Date, Enum, DateTime
from sqlalchemy.orm import relationship

from app.db.base import Base


class TaskStatus(enum.Enum):
    not_started = "Not started"
    in_progress = "In progress"
    completed = "Completed"


class Task(Base):
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True, index=True)
    task_name = Column(String, nullable=False)
    parent_task_id = Column(Integer, ForeignKey("tasks.id"))
    employee_id = Column(Integer, ForeignKey("employees.id"))
    deadline = Column(DateTime, nullable=False)
    status = Column(Enum(TaskStatus), nullable=False, default=TaskStatus.not_started)
    employee = relationship("Employee", back_populates="tasks")
