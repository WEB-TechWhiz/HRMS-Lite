from datetime import date

from pydantic import BaseModel, ConfigDict, Field

from app.models.attendance import AttendanceStatus


class AttendanceCreate(BaseModel):
    employeeId: str = Field(min_length=3, max_length=50)
    date: date
    status: AttendanceStatus


class AttendanceRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    employeeId: int = Field(alias="employee_id")
    date: date
    status: AttendanceStatus
