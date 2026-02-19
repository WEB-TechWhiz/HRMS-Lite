from calendar import monthrange
from datetime import date

from pymongo.errors import DuplicateKeyError, PyMongoError
from pymongo.database import Database

from app.core.constants import ErrorCode
from app.exceptions.custom_exceptions import AppException
from app.models.attendance import AttendanceStatus
from app.repositories import attendance_repo, employee_repo
from app.schemas.attendance import AttendanceCreate


def mark_attendance(db: Database, payload: AttendanceCreate):
    employee = employee_repo.get_by_employee_id(db, payload.employeeId)
    if not employee:
        raise AppException(404, "Employee not found", ErrorCode.NOT_FOUND)

    mark_date = payload.date.isoformat()
    if attendance_repo.get_by_employee_and_date(db, payload.employeeId, mark_date):
        raise AppException(409, "Attendance already marked for this date", ErrorCode.DUPLICATE_ATTENDANCE)

    attendance_doc = {
        "employeeId": payload.employeeId,
        "date": mark_date,
        "status": payload.status.value,
        "punchInTime": payload.punchInTime.isoformat() if payload.punchInTime else None,
        "punchOutTime": payload.punchOutTime.isoformat() if payload.punchOutTime else None,
    }

    try:
        record = attendance_repo.create(db, attendance_doc)
        return payload.employeeId, record
    except DuplicateKeyError:
        raise AppException(409, "Attendance already marked for this date", ErrorCode.DUPLICATE_ATTENDANCE)
    except PyMongoError:
        raise AppException(500, "Database operation failed", ErrorCode.DATABASE_ERROR)


def get_employee_attendance(db: Database, employee_id: str):
    employee = employee_repo.get_by_employee_id(db, employee_id)
    if not employee:
        raise AppException(404, "Employee not found", ErrorCode.NOT_FOUND)

    return employee_id, attendance_repo.list_by_employee(db, employee_id)


def get_employee_monthly_attendance(db: Database, employee_id: str, year: int, month: int):
    employee = employee_repo.get_by_employee_id(db, employee_id)
    if not employee:
        raise AppException(404, "Employee not found", ErrorCode.NOT_FOUND)

    month_records = attendance_repo.list_by_employee_month(db, employee_id, year, month)
    record_map = {item["date"]: item for item in month_records}

    days_in_month = monthrange(year, month)[1]
    result = []
    marked_count = 0

    for day in range(1, days_in_month + 1):
        current_date = date(year, month, day).isoformat()
        existing = record_map.get(current_date)
        if existing:
            marked_count += 1
            result.append(existing)
        else:
            result.append(
                {
                    "id": None,
                    "employeeId": employee_id,
                    "date": current_date,
                    "status": AttendanceStatus.absent.value,
                    "punchInTime": None,
                    "punchOutTime": None,
                }
            )

    return employee_id, result, marked_count
