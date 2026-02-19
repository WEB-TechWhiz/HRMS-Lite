from pymongo import ASCENDING, MongoClient
from pymongo.database import Database

from app.core.config import settings

client = MongoClient(settings.database_url, serverSelectionTimeoutMS=5000)


def get_database() -> Database:
    return client[settings.database_name]


def get_db():
    yield get_database()


def ping_database() -> None:
    client.admin.command("ping")


def ensure_indexes(db: Database | None = None) -> None:
    database = db or get_database()

    employees = database["employees"]
    employees.create_index([("employeeId", ASCENDING)], unique=True, name="uq_employee_id")
    employees.create_index([("email", ASCENDING)], unique=True, name="uq_employee_email")

    attendance = database["attendance"]
    attendance.create_index([("employeeId", ASCENDING), ("date", ASCENDING)], unique=True, name="uq_employee_date")
    attendance.create_index([("employeeId", ASCENDING), ("date", ASCENDING)], name="idx_employee_date")
