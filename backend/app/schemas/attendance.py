from datetime import date, time

from pydantic import BaseModel, Field, model_validator

from app.models.attendance import AttendanceStatus


class AttendanceCreate(BaseModel):
    employeeId: str = Field(min_length=3, max_length=50)
    date: date
    status: AttendanceStatus
    punchInTime: time | None = None
    punchOutTime: time | None = None

    @model_validator(mode="after")
    def validate_business_rules(self):
        self.employeeId = self.employeeId.strip().upper()

        if self.date > date.today():
            raise ValueError("Attendance date cannot be in the future")

        if self.punchOutTime and not self.punchInTime:
            raise ValueError("Punch-out time requires punch-in time")

        if self.punchInTime and self.punchOutTime and self.punchOutTime < self.punchInTime:
            raise ValueError("Punch-out time cannot be earlier than punch-in time")

        if self.status == AttendanceStatus.absent and (self.punchInTime or self.punchOutTime):
            raise ValueError("Absent status cannot include punch times")

        return self


class AttendanceRead(BaseModel):
    id: str | None
    employeeId: str
    date: str
    status: AttendanceStatus
    punchInTime: str | None = None
    punchOutTime: str | None = None
