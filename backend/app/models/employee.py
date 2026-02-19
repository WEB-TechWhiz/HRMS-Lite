from dataclasses import dataclass
from datetime import datetime


@dataclass
class Employee:
    id: str
    employee_id: str
    full_name: str
    email: str
    department: str
    created_at: datetime
