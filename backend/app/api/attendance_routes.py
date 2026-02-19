from fastapi import APIRouter, Depends, Query
from pymongo.database import Database

from app.database.connection import get_db
from app.schemas.attendance import AttendanceCreate, AttendanceRead
from app.services import attendance_service
from app.utils.response import success_response

router = APIRouter(prefix="/attendance", tags=["Attendance"])


@router.post("", status_code=201)
def create_attendance(payload: AttendanceCreate, db: Database = Depends(get_db)):
    employee_id, record = attendance_service.mark_attendance(db, payload)
    data = AttendanceRead(
        id=record["id"],
        employeeId=employee_id,
        date=record["date"],
        status=record["status"],
        punchInTime=record.get("punchInTime"),
        punchOutTime=record.get("punchOutTime"),
    ).model_dump(mode="json")
    return success_response(data=data, message="Attendance marked successfully")


@router.get("/monthly/{employee_id}")
def get_monthly_attendance(
    employee_id: str,
    year: int = Query(ge=2000, le=2100),
    month: int = Query(ge=1, le=12),
    db: Database = Depends(get_db),
):
    normalized_employee_id = employee_id.upper().strip()
    employee_business_id, records, marked_count = attendance_service.get_employee_monthly_attendance(
        db,
        normalized_employee_id,
        year,
        month,
    )
    data = [
        AttendanceRead(
            id=item.get("id"),
            employeeId=employee_business_id,
            date=item["date"],
            status=item["status"],
            punchInTime=item.get("punchInTime"),
            punchOutTime=item.get("punchOutTime"),
        ).model_dump(mode="json")
        for item in records
    ]

    return success_response(
        data=data,
        message="Monthly attendance fetched successfully",
        meta={
            "year": year,
            "month": month,
            "totalDays": len(data),
            "totalMarked": marked_count,
        },
    )


@router.get("/{employee_id}")
def get_attendance(employee_id: str, db: Database = Depends(get_db)):
    normalized_employee_id = employee_id.upper().strip()
    employee_business_id, records = attendance_service.get_employee_attendance(db, normalized_employee_id)
    data = [
        AttendanceRead(
            id=item.get("id"),
            employeeId=employee_business_id,
            date=item["date"],
            status=item["status"],
            punchInTime=item.get("punchInTime"),
            punchOutTime=item.get("punchOutTime"),
        ).model_dump(mode="json")
        for item in records
    ]
    return success_response(data=data, message="Attendance fetched successfully", meta={"total": len(data)})
