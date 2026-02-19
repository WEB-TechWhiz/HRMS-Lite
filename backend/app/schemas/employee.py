from datetime import datetime

from email_validator import EmailNotValidError, validate_email
from pydantic import BaseModel, EmailStr, Field, field_validator


class EmployeeCreate(BaseModel):
    employeeId: str = Field(min_length=3, max_length=50)
    fullName: str = Field(min_length=2, max_length=120)
    email: EmailStr
    department: str = Field(min_length=2, max_length=80)

    @field_validator("employeeId")
    @classmethod
    def normalize_employee_id(cls, value: str) -> str:
        return value.strip().upper()

    @field_validator("fullName", "department")
    @classmethod
    def normalize_text(cls, value: str) -> str:
        return value.strip()

    @field_validator("email", mode="before")
    @classmethod
    def normalize_email(cls, value):
        if isinstance(value, str):
            value = value.strip().lower()
        return value

    @field_validator("email")
    @classmethod
    def verify_email_format(cls, value: EmailStr) -> str:
        try:
            validated = validate_email(str(value), check_deliverability=False)
            return validated.normalized
        except EmailNotValidError as exc:
            raise ValueError("Invalid email address format") from exc


class EmployeeRead(BaseModel):
    id: str
    employeeId: str
    fullName: str
    email: EmailStr
    department: str
    createdAt: datetime


class EmployeeListParams(BaseModel):
    page: int = Field(default=1, ge=1)
    limit: int = Field(default=20, ge=1, le=100)
