from enum import Enum


class AttendanceStatus(str, Enum):
    present = "Present"
    absent = "Absent"
