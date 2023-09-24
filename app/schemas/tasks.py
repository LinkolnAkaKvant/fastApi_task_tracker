from datetime import datetime
from typing import Optional

from pydantic import BaseModel

from app.models.tasks import TaskStatus
from app.schemas.employees import EmployeeBase


class TaskBase(BaseModel):
    task_name: str
    description: str
    parent_task_id: int
    employee_id: int
    deadline: datetime
    status: TaskStatus
    employee: Optional[EmployeeBase]


class TaskCreate(TaskBase):
    task_name: str
    description: str
    parent_task_id: int
    employee_id: int
    deadline: datetime
    status: TaskStatus


class ImportantTask(BaseModel):
    task_name: str
    deadline: datetime
    employee_full_name: Optional[str]