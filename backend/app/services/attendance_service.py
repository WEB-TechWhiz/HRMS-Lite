from sqlalchemy.orm import Session

from app.core.constants import ErrorCode
from app.exceptions.custom_exceptions import AppException
from app.repositories import attendance_repo, employee_repo
from app.schemas.attendance import AttendanceCreate


def mark_attendance(db: Session, payload: AttendanceCreate):
    employee = employee_repo.get_by_employee_id(db, payload.employeeId)
    if not employee:
        raise AppException(404, "Employee not found", ErrorCode.NOT_FOUND)

    existing = attendance_repo.get_by_employee_and_date(db, employee.id, payload.date)
    if existing:
        raise AppException(409, "Attendance already marked for this date", ErrorCode.DUPLICATE_ATTENDANCE)

    return attendance_repo.create(db, employee.id, payload.date, payload.status)


def get_employee_attendance(db: Session, employee_id: str):
    employee = employee_repo.get_by_employee_id(db, employee_id)
    if not employee:
        raise AppException(404, "Employee not found", ErrorCode.NOT_FOUND)

    return attendance_repo.list_by_employee(db, employee.id)
