from datetime import date
from enum import Enum

from sqlalchemy import Date, Enum as SqlEnum, ForeignKey, Integer, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.base import Base


class AttendanceStatus(str, Enum):
    present = "Present"
    absent = "Absent"


class Attendance(Base):
    __tablename__ = "attendance"
    __table_args__ = (UniqueConstraint("employee_id", "date", name="uq_employee_date"),)

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    employee_id: Mapped[int] = mapped_column(ForeignKey("employees.id", ondelete="CASCADE"), index=True)
    date: Mapped[date] = mapped_column(Date)
    status: Mapped[AttendanceStatus] = mapped_column(SqlEnum(AttendanceStatus))

    employee = relationship("Employee", back_populates="attendance_records")
