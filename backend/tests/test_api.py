def _create_employee(client, employee_id="EMP001", email="john@example.com"):
    payload = {
        "employeeId": employee_id,
        "fullName": "John Doe",
        "email": email,
        "department": "Engineering",
    }
    return client.post("/employees", json=payload)


def test_employee_crud_and_pagination_meta(client):
    response = _create_employee(client, employee_id="emp001", email="john1@example.com")
    assert response.status_code == 201
    body = response.json()
    assert body["success"] is True
    assert body["data"]["employeeId"] == "EMP001"
    assert isinstance(body["data"]["id"], str)
    assert body["meta"].get("requestId")

    duplicate = _create_employee(client, employee_id="emp001", email="john1@example.com")
    assert duplicate.status_code == 409
    assert duplicate.json()["error"]["code"] == "DUPLICATE_EMPLOYEE"

    list_response = client.get("/employees?page=1&limit=10")
    assert list_response.status_code == 200
    list_body = list_response.json()
    assert list_body["meta"]["total"] == 1
    assert list_body["meta"]["page"] == 1
    assert list_body["meta"]["limit"] == 10

    delete_response = client.delete("/employees/emp001")
    assert delete_response.status_code == 200
    assert delete_response.json()["success"] is True


def test_attendance_with_punch_times_and_monthly_page(client):
    _create_employee(client, employee_id="emp007", email="john7@example.com")

    mark_payload = {
        "employeeId": "emp007",
        "date": "2026-02-19",
        "status": "Present",
        "punchInTime": "09:00:00",
        "punchOutTime": "18:00:00",
    }
    mark = client.post("/attendance", json=mark_payload)
    assert mark.status_code == 201
    mark_data = mark.json()["data"]
    assert mark_data["employeeId"] == "EMP007"
    assert mark_data["punchInTime"] == "09:00:00"
    assert mark_data["punchOutTime"] == "18:00:00"

    monthly = client.get("/attendance/monthly/emp007?year=2026&month=2")
    assert monthly.status_code == 200
    monthly_body = monthly.json()
    assert monthly_body["meta"]["totalDays"] == 28
    assert monthly_body["meta"]["totalMarked"] == 1

    day_record = next(item for item in monthly_body["data"] if item["date"] == "2026-02-19")
    assert day_record["status"] == "Present"
    assert day_record["punchInTime"] == "09:00:00"
    assert day_record["punchOutTime"] == "18:00:00"


def test_attendance_duplicate_and_time_validation(client):
    _create_employee(client, employee_id="emp010", email="john10@example.com")

    payload = {
        "employeeId": "emp010",
        "date": "2026-02-19",
        "status": "Present",
        "punchInTime": "10:00:00",
        "punchOutTime": "17:00:00",
    }

    first = client.post("/attendance", json=payload)
    assert first.status_code == 201

    duplicate = client.post("/attendance", json=payload)
    assert duplicate.status_code == 409
    assert duplicate.json()["error"]["code"] == "DUPLICATE_ATTENDANCE"

    invalid_time = {
        "employeeId": "emp010",
        "date": "2026-02-20",
        "status": "Present",
        "punchInTime": "17:00:00",
        "punchOutTime": "10:00:00",
    }
    invalid_time_response = client.post("/attendance", json=invalid_time)
    assert invalid_time_response.status_code == 400
    assert invalid_time_response.json()["error"]["code"] == "VALIDATION_ERROR"


def test_validation_error_contract(client):
    _create_employee(client, employee_id="EMP020", email="alice@example.com")

    invalid_payload = {
        "employeeId": "EMP020",
        "date": "2099-01-01",
        "status": "Absent",
    }

    response = client.post("/attendance", json=invalid_payload)
    assert response.status_code == 400

    body = response.json()
    assert body["success"] is False
    assert body["message"] == "Validation failed"
    assert body["error"]["code"] == "VALIDATION_ERROR"
    assert isinstance(body["error"]["details"]["errors"], list)
    assert body["meta"].get("requestId")


def test_invalid_email_validation(client):
    response = _create_employee(client, employee_id="EMP030", email="not-an-email")
    assert response.status_code == 400

    body = response.json()
    assert body["success"] is False
    assert body["error"]["code"] == "VALIDATION_ERROR"


def test_health_response_contract(client):
    response = client.get("/health")
    assert response.status_code == 200
    body = response.json()
    assert body["success"] is True
    assert body["data"]["status"] == "ok"
    assert body["meta"].get("requestId")
