from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database.connection import get_db
from app.schemas.attendance import AttendanceCreate, AttendanceRead
from app.services import attendance_service
from app.utils.response import success_response

router = APIRouter(prefix="/attendance", tags=["Attendance"])


@router.post("", status_code=201)
def create_attendance(payload: AttendanceCreate, db: Session = Depends(get_db)):
    record = attendance_service.mark_attendance(db, payload)
    data = AttendanceRead.model_validate(record).model_dump(by_alias=False)
    return success_response(data=data, message="Attendance marked successfully")


@router.get("/{employee_id}")
def get_attendance(employee_id: str, db: Session = Depends(get_db)):
    records = attendance_service.get_employee_attendance(db, employee_id)
    data = [AttendanceRead.model_validate(item).model_dump(by_alias=False) for item in records]
    return success_response(data=data, message="Attendance fetched successfully")
