from pymongo.errors import DuplicateKeyError, PyMongoError
from pymongo.database import Database

from app.core.constants import ErrorCode
from app.exceptions.custom_exceptions import AppException
from app.repositories import attendance_repo, employee_repo
from app.schemas.employee import EmployeeCreate


def create_employee(db: Database, payload: EmployeeCreate):
    if employee_repo.get_by_employee_id(db, payload.employeeId):
        raise AppException(409, "Employee already exists", ErrorCode.DUPLICATE_EMPLOYEE)
    if employee_repo.get_by_email(db, str(payload.email)):
        raise AppException(409, "Employee email already exists", ErrorCode.DUPLICATE_EMPLOYEE)

    employee_doc = {
        "employeeId": payload.employeeId,
        "fullName": payload.fullName,
        "email": str(payload.email),
        "department": payload.department,
    }

    try:
        return employee_repo.create(db, employee_doc)
    except DuplicateKeyError:
        raise AppException(409, "Employee already exists", ErrorCode.DUPLICATE_EMPLOYEE)
    except PyMongoError:
        raise AppException(500, "Database operation failed", ErrorCode.DATABASE_ERROR)


def list_employees(db: Database, page: int, limit: int):
    items = employee_repo.list_paginated(db, page, limit)
    total = employee_repo.count_all(db)
    return items, total


def delete_employee(db: Database, employee_id: str):
    employee = employee_repo.get_by_employee_id(db, employee_id)
    if not employee:
        raise AppException(404, "Employee not found", ErrorCode.NOT_FOUND)

    try:
        employee_repo.delete_by_employee_id(db, employee_id)
        attendance_repo.delete_by_employee_id(db, employee_id)
    except PyMongoError:
        raise AppException(500, "Database operation failed", ErrorCode.DATABASE_ERROR)
