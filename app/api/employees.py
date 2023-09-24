from typing import List, Optional
from sqlalchemy import and_, or_, func
from fastapi import APIRouter
from sqlalchemy.orm import joinedload

from app.db.base import get_session
from app.models.employees import Employee
from app.models.tasks import Task, TaskStatus
from app.schemas.employees import EmployeeBase, Employees
from app.schemas.tasks import ImportantTask

employee_router = APIRouter()


@employee_router.get("/employees", response_model=List[Employees])
def get_employees():
    with get_session() as session:
        employees = session.query(Employee).options(joinedload(Employee.tasks)).all()
    return employees


@employee_router.get("/employees/{employee_id}", response_model=Employees)
def get_employee(employee_id: int):
    with get_session() as session:
        employee = session.query(Employee).options(joinedload(Employee.tasks)).filter(
            Employee.id == employee_id).first()
    return employee


@employee_router.post("/employees", response_model=EmployeeBase)
def create_employee(employee: EmployeeBase):
    with get_session() as session:
        new_employee = Employee(**employee.dict())
        session.add(new_employee)
        session.commit()
        session.refresh(new_employee)
    return new_employee


@employee_router.put("/employees/{employee_id}", response_model=EmployeeBase)
def update_employee(employee_id: int, new_full_name: Optional[str] = None, new_position: Optional[str] = None):
    with get_session() as session:
        employee = session.query(Employee).filter(Employee.id == employee_id).first()
        if new_full_name is not None:
            employee.full_name = new_full_name
        if new_position is not None:
            employee.position = new_position
        session.commit()
        session.refresh(employee)
    return employee


@employee_router.delete("/employees/{employee_id}")
def delete_employee(employee_id: int):
    with get_session() as session:
        employee = session.query(Employee).filter(Employee.id == employee_id).first()
        session.delete(employee)
        session.commit()
        return {"message": "Employee deleted"}


@employee_router.get("/busy_employees", response_model=List[EmployeeBase])
def get_busy_employees():
    with get_session() as session:
        employees = session.query(Employee). \
            outerjoin(Task, Employee.id == Task.employee_id). \
            group_by(Employee.id). \
            order_by(func.count(Task.id).desc()). \
            options(joinedload(Employee.tasks)).all()
    return employees


@employee_router.get("/important_tasks", response_model=List[ImportantTask])
def get_important_tasks():
    with get_session() as session:
        important_tasks = session.query(Task). \
            filter(
            and_(Task.status == TaskStatus.not_started, Task.children.any(Task.status == TaskStatus.in_progress))). \
            options(joinedload(Task.employee)).all()

        important_tasks_list = []
        for task in important_tasks:
            suitable_employee = session.query(Employee). \
                outerjoin(Task, Employee.id == Task.employee_id). \
                group_by(Employee.id). \
                having(or_(Employee.id == task.employee_id, func.count(Task.id) <= 2)). \
                order_by(func.count(Task.id)). \
                first()

            important_task = ImportantTask(
                task_name=task.task_name,
                deadline=task.deadline,
                employee_full_name=suitable_employee.full_name if suitable_employee else None
            )
            important_tasks_list.append(important_task)

        return important_tasks_list
