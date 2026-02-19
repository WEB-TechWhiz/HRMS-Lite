from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database.connection import get_db
from app.schemas.employee import EmployeeCreate, EmployeeRead
from app.services import employee_service
from app.utils.response import success_response

router = APIRouter(prefix="/employees", tags=["Employees"])


@router.post("", status_code=201)
def create_employee(payload: EmployeeCreate, db: Session = Depends(get_db)):
    employee = employee_service.create_employee(db, payload)
    data = EmployeeRead.model_validate(employee).model_dump(by_alias=False)
    return success_response(data=data, message="Employee created successfully")


@router.get("")
def get_employees(db: Session = Depends(get_db)):
    employees = employee_service.list_employees(db)
    data = [EmployeeRead.model_validate(item).model_dump(by_alias=False) for item in employees]
    return success_response(data=data, message="Employees fetched successfully")


@router.delete("/{employee_id}")
def delete_employee(employee_id: str, db: Session = Depends(get_db)):
    employee_service.delete_employee(db, employee_id)
    return success_response(data=None, message="Employee deleted successfully")
