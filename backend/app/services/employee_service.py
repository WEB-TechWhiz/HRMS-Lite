from sqlalchemy.orm import Session

from app.core.constants import ErrorCode
from app.exceptions.custom_exceptions import AppException
from app.repositories import employee_repo
from app.schemas.employee import EmployeeCreate


def create_employee(db: Session, payload: EmployeeCreate):
    if employee_repo.get_by_employee_id(db, payload.employeeId):
        raise AppException(409, "Employee already exists", ErrorCode.DUPLICATE_EMPLOYEE)
    if employee_repo.get_by_email(db, payload.email):
        raise AppException(409, "Employee email already exists", ErrorCode.DUPLICATE_EMPLOYEE)

    return employee_repo.create(
        db,
        employee_id=payload.employeeId,
        full_name=payload.fullName,
        email=str(payload.email),
        department=payload.department,
    )


def list_employees(db: Session):
    return employee_repo.list_all(db)


def delete_employee(db: Session, employee_id: str):
    employee = employee_repo.get_by_employee_id(db, employee_id)
    if not employee:
        raise AppException(404, "Employee not found", ErrorCode.NOT_FOUND)

    employee_repo.delete(db, employee)
