from datetime import datetime

from pydantic import BaseModel, ConfigDict, EmailStr, Field


class EmployeeCreate(BaseModel):
    employeeId: str = Field(min_length=3, max_length=50)
    fullName: str = Field(min_length=2, max_length=120)
    email: EmailStr
    department: str = Field(min_length=2, max_length=80)


class EmployeeRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    employeeId: str = Field(alias="employee_id")
    fullName: str = Field(alias="full_name")
    email: EmailStr
    department: str
    createdAt: datetime = Field(alias="created_at")
