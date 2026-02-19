from datetime import datetime, timezone

from bson import ObjectId
from pymongo import DESCENDING
from pymongo.database import Database


COLLECTION = "employees"


def _serialize(document: dict | None):
    if not document:
        return None

    return {
        "id": str(document.get("_id")),
        "employeeId": document.get("employeeId"),
        "fullName": document.get("fullName"),
        "email": document.get("email"),
        "department": document.get("department"),
        "createdAt": document.get("createdAt"),
    }


def get_by_employee_id(db: Database, employee_id: str):
    return _serialize(db[COLLECTION].find_one({"employeeId": employee_id}))


def get_by_email(db: Database, email: str):
    return _serialize(db[COLLECTION].find_one({"email": email}))


def list_paginated(db: Database, page: int, limit: int):
    offset = (page - 1) * limit
    cursor = db[COLLECTION].find().sort("createdAt", DESCENDING).skip(offset).limit(limit)
    return [_serialize(item) for item in cursor]


def count_all(db: Database) -> int:
    return db[COLLECTION].count_documents({})


def create(db: Database, employee_doc: dict):
    payload = {
        "employeeId": employee_doc["employeeId"],
        "fullName": employee_doc["fullName"],
        "email": employee_doc["email"],
        "department": employee_doc["department"],
        "createdAt": employee_doc.get("createdAt") or datetime.now(timezone.utc),
    }
    result = db[COLLECTION].insert_one(payload)
    inserted = db[COLLECTION].find_one({"_id": ObjectId(result.inserted_id)})
    return _serialize(inserted)


def delete_by_employee_id(db: Database, employee_id: str) -> int:
    result = db[COLLECTION].delete_one({"employeeId": employee_id})
    return result.deleted_count
