from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.crud.tasks import get_task, get_tasks
from app.db.base import get_db
from app.schemas.tasks import Task, TaskCreate, TaskUpdate

router = APIRouter()


@router.post("/", response_model=TaskCreate)
def create_task(task: TaskCreate, db: Session = Depends(get_db)):
    return create_task(db=db, task=task)


@router.get("/{task_id}", response_model=Task)
def get_task(task_id: int, db: Session = Depends(get_db)):
    db_task = get_task(db, task_id=task_id)
    if db_task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    return db_task


@router.get("/", response_model=List[Task])
def get_tasks(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    tasks = get_tasks(db, skip=skip, limit=limit)
    return tasks


@router.put("/{task_id}", response_model=TaskUpdate)
def update_task(task_id: int, task: TaskCreate, db: Session = Depends(get_db)):
    db_task = update_task(db=db, task_id=task_id, task=task)
    if db_task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    return db_task


@router.delete("/{task_id}", response_model=Task)
def delete_task(task_id: int, db: Session = Depends(get_db)):
    db_task = delete_task(db=db, task_id=task_id)
    if db_task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    return db_task
