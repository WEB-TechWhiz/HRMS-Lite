from fastapi import APIRouter, Depends, Query
from pymongo.database import Database

from app.database.connection import get_db
from app.schemas.employee import EmployeeCreate, EmployeeRead
from app.services import employee_service
from app.utils.response import success_response

router = APIRouter(prefix="/employees", tags=["Employees"])


@router.post("", status_code=201)
def create_employee(payload: EmployeeCreate, db: Database = Depends(get_db)):
    employee = employee_service.create_employee(db, payload)
    data = EmployeeRead.model_validate(employee).model_dump(mode="json")
    return success_response(data=data, message="Employee created successfully")


@router.get("")
def get_employees(
    page: int = Query(default=1, ge=1),
    limit: int = Query(default=20, ge=1, le=100),
    db: Database = Depends(get_db),
):
    employees, total = employee_service.list_employees(db, page, limit)
    data = [EmployeeRead.model_validate(item).model_dump(mode="json") for item in employees]
    return success_response(
        data=data,
        message="Employees fetched successfully",
        meta={"total": total, "page": page, "limit": limit},
    )


@router.delete("/{employee_id}")
def delete_employee(employee_id: str, db: Database = Depends(get_db)):
    employee_service.delete_employee(db, employee_id.upper().strip())
    return success_response(data=None, message="Employee deleted successfully")
