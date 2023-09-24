from datetime import datetime
from typing import Optional, List

from pydantic import BaseModel


class EmployeeBase(BaseModel):
    full_name: str
    position: str


class TaskName(BaseModel):
    task_name: str


class Employees(EmployeeBase):
    tasks: Optional[List[TaskName]]


class ImportantTask(BaseModel):
    task_name: str
    deadline: datetime
    employee_full_name: Optional[str]
