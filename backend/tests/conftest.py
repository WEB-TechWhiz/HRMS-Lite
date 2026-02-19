import mongomock
import pytest
from fastapi.testclient import TestClient

import app.main as main_module
from app.database.connection import ensure_indexes, get_db
from app.main import app

mock_client = mongomock.MongoClient()
mock_db = mock_client["hrms_test"]


def override_get_db():
    yield mock_db


app.dependency_overrides[get_db] = override_get_db
main_module.ping_database = lambda: None
main_module.ensure_indexes = lambda: None


@pytest.fixture()
def client():
    return TestClient(app)


@pytest.fixture(autouse=True)
def reset_db():
    mock_db["employees"].delete_many({})
    mock_db["attendance"].delete_many({})
    ensure_indexes(mock_db)
