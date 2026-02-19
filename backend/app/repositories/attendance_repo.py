from calendar import monthrange
from datetime import date

from bson import ObjectId
from pymongo import ASCENDING, DESCENDING
from pymongo.database import Database


COLLECTION = "attendance"


def _serialize(document: dict | None):
    if not document:
        return None

    return {
        "id": str(document.get("_id")),
        "employeeId": document.get("employeeId"),
        "date": document.get("date"),
        "status": document.get("status"),
        "punchInTime": document.get("punchInTime"),
        "punchOutTime": document.get("punchOutTime"),
    }


def get_by_employee_and_date(db: Database, employee_id: str, mark_date: str):
    return _serialize(db[COLLECTION].find_one({"employeeId": employee_id, "date": mark_date}))


def list_by_employee(db: Database, employee_id: str):
    cursor = db[COLLECTION].find({"employeeId": employee_id}).sort("date", DESCENDING)
    return [_serialize(item) for item in cursor]


def list_by_employee_month(db: Database, employee_id: str, year: int, month: int):
    last_day = monthrange(year, month)[1]
    start_date = date(year, month, 1).isoformat()
    end_date = date(year, month, last_day).isoformat()

    cursor = db[COLLECTION].find(
        {
            "employeeId": employee_id,
            "date": {"$gte": start_date, "$lte": end_date},
        }
    ).sort("date", ASCENDING)

    return [_serialize(item) for item in cursor]


def create(db: Database, attendance_doc: dict):
    payload = {
        "employeeId": attendance_doc["employeeId"],
        "date": attendance_doc["date"],
        "status": attendance_doc["status"],
        "punchInTime": attendance_doc.get("punchInTime"),
        "punchOutTime": attendance_doc.get("punchOutTime"),
    }
    result = db[COLLECTION].insert_one(payload)
    inserted = db[COLLECTION].find_one({"_id": ObjectId(result.inserted_id)})
    return _serialize(inserted)


def delete_by_employee_id(db: Database, employee_id: str) -> int:
    result = db[COLLECTION].delete_many({"employeeId": employee_id})
    return result.deleted_count
