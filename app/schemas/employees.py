from pydantic import BaseModel


class EmployeeBase(BaseModel):
    full_name: str
    position: str


class EmployeeCreate(EmployeeBase):
    pass


class EmployeeUpdate(EmployeeBase):
    pass


class Employee(EmployeeBase):
    id: int

    class Config:
        orm_mode = True
