from sqlalchemy.orm import Session

from app.models.employees import Employee
from app.schemas.employees import EmployeeCreate, EmployeeUpdate


def get_employee(db: Session, employee_id: int):
    return db.query(Employee).filter(Employee.id == employee_id).first()


def get_employees(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Employee).offset(skip).limit(limit).all()


def create_employee(db: Session, employee: EmployeeCreate):
    db_employee = Employee(**employee.dict())
    db.add(db_employee)
    db.commit()
    db.refresh(db_employee)
    return db_employee


def update_employee(db: Session, employee_id: int, employee: EmployeeUpdate):
    db_employee = db.query(Employee).filter(Employee.id == employee_id).first()
    if db_employee is None:
        return None
    for key, value in employee.dict().items():
        setattr(db_employee, key, value)
    db.commit()
    return db_employee


def delete_employee(db: Session, employee_id: int):
    db_employee = db.query(Employee).filter(Employee.id == employee_id).first()
    if db_employee is None:
        return None
    db.delete(db_employee)
    db.commit()
    return db_employee
