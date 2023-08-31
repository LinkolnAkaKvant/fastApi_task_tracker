from sqlalchemy.orm import Session

from app.db.base import get_db
from app.schemas.employees import Employee, EmployeeCreate, EmployeeUpdate
from fastapi import APIRouter, Depends, HTTPException

router = APIRouter()


@router.post("/", response_model=Employee)
def create_employee(employee: EmployeeCreate, db: Session = Depends(get_db)):
    return create_employee(db=db, employee=employee)


@router.get("/{employee_id}", response_model=Employee)
def get_employee(employee_id: int, db: Session = Depends(get_db)):
    db_employee = get_employee(db=db, employee_id=employee_id)
    if db_employee is None:
        raise HTTPException(status_code=404, detail="Employee not found")
    return db_employee


@router.get("/", response_model=list[Employee])
def get_employees(db: Session = Depends(get_db), skip: int = 0, limit: int = 100):
    employees = get_employees(db=db, skip=skip, limit=limit)
    return employees


@router.put("/{employee_id}", response_model=Employee)
def update_employee(employee_id: int, employee: EmployeeUpdate, db: Session = Depends(get_db)):
    db_employee = update_employee(db=db, employee_id=employee_id, employee=employee)
    if db_employee is None:
        raise HTTPException(status_code=404, detail="Employee not found")
    return db_employee


@router.delete("/{employee_id}", response_model=Employee)
def delete_employee(employee_id: int, db: Session = Depends(get_db)):
    db_employee = delete_employee(db=db, employee_id=employee_id)
    if db_employee is None:
        raise HTTPException(status_code=404, detail="Employee not found")
    return db_employee
