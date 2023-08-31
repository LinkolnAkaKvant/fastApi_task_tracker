from datetime import date
from typing import Optional

from pydantic import BaseModel


class TaskBase(BaseModel):
    task_name: str
    parent_task_id: Optional[int]
    employee_id: Optional[int]
    deadline: Optional[date]
    status: Optional[str]


class TaskCreate(TaskBase):
    pass


class TaskUpdate(TaskBase):
    pass


class Task(TaskBase):
    id: int

    class Config:
        orm_mode = True
