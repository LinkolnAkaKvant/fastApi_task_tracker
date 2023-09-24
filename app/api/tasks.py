from datetime import datetime
from typing import List, Optional

from fastapi import APIRouter
from sqlalchemy.orm import joinedload

from app.db.base import get_session
from app.models.tasks import Task, TaskStatus
from app.schemas.tasks import TaskBase, TaskCreate

task_router = APIRouter()


@task_router.get("/tasks", response_model=List[TaskBase])
def get_tasks():
    with get_session() as session:
        tasks = session.query(Task).options(joinedload(Task.employee)).all()
    return tasks


@task_router.get("/tasks/{task_id}", response_model=TaskBase)
def get_task(task_id: int):
    with get_session() as session:
        task = session.query(Task).filter(Task.id == task_id).first()
    return task


@task_router.post("/tasks", response_model=TaskCreate)
def create_task(task: TaskCreate):
    with get_session() as session:
        new_task = Task(**task.dict())
        session.add(new_task)
        session.commit()
        session.refresh(new_task)
    return new_task


@task_router.put("/tasks/{task_id}")
def update_task(task_id: int, description: Optional[str] = None, employee_id: Optional[int] = None,
                deadline: Optional[datetime] = None, status: Optional[TaskStatus] = None):
    with get_session() as session:
        task = session.query(Task).filter(Task.id == task_id).first()
        if description is not None:
            task.description = description
        if employee_id is not None:
            task.employee_id = employee_id
        if deadline is not None:
            task.deadline = deadline
        if status is not None:
            task.status = status
        session.commit()
        session.refresh(task)
    return {"message": "Task updated", "task": task}


@task_router.delete("/tasks/{task_id}")
def delete_task(task_id: int):
    with get_session() as session:
        task = session.query(Task).filter(Task.id == task_id).first()
        session.delete(task)
        session.commit()
        return {"message": "Task deleted"}
