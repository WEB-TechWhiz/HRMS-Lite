from datetime import date

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.attendance import Attendance, AttendanceStatus


def get_by_employee_and_date(db: Session, employee_pk: int, mark_date: date) -> Attendance | None:
    return db.scalar(
        select(Attendance).where(Attendance.employee_id == employee_pk, Attendance.date == mark_date)
    )


def list_by_employee(db: Session, employee_pk: int) -> list[Attendance]:
    return list(
        db.scalars(select(Attendance).where(Attendance.employee_id == employee_pk).order_by(Attendance.date.desc())).all()
    )


def create(db: Session, employee_pk: int, mark_date: date, status: AttendanceStatus) -> Attendance:
    record = Attendance(employee_id=employee_pk, date=mark_date, status=status)
    db.add(record)
    db.commit()
    db.refresh(record)
    return record
