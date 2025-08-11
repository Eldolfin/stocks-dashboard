import io
import time

import requests

BASE_URL = "http://localhost:5000/api"


def _register_and_login_session() -> requests.Session:
    unique_email = f"test_user_compare_{time.time_ns()}@example.com"
    password = "test_password"
    # Register
    reg = requests.post(f"{BASE_URL}/register", data={"email": unique_email, "password": password})
    assert reg.status_code == 201, f"Register failed: {reg.text}"
    # Login
    s = requests.Session()
    login = s.post(f"{BASE_URL}/login", json={"email": unique_email, "password": password})
    assert login.status_code == 200, f"Login failed: {login.text}"
    return s


def test_compare_to_index_works_end_to_end():
    session = _register_and_login_session()

    # Upload an eToro report first so the file exists in the user's folder
    with open("tests/data/etoro-account-statement-12-31-2014-7-5-2025_TEST.xlsx", "rb") as f:
        files = {
            "file": (
                "etoro-report.xlsx",
                io.BytesIO(f.read()),
                "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            )
        }
    resp = session.post(f"{BASE_URL}/etoro/upload_report", files=files, data={"precision": "D"})
    assert resp.status_code == 200, f"Upload failed: {resp.text}"

    # The backend stores uploaded file under the original filename returned in list
    reports = session.get(f"{BASE_URL}/etoro/reports")
    assert reports.status_code == 200, f"List reports failed: {reports.text}"
    filenames = reports.json().get("reports", [])
    assert len(filenames) > 0
    filename = filenames[-1]

    # Call compare_to_index
    payload = {"filename": filename, "index_ticker": "^GSPC"}
    cmp = session.post(f"{BASE_URL}/etoro/compare_to_index", json=payload)
    assert cmp.status_code == 200, f"Compare failed: {cmp.text}"
    data = cmp.json()
    assert "dates" in data and "index_values" in data
    assert len(data["dates"]) == len(data["index_values"]) > 10
    assert any(v > 0 for v in data["index_values"])  # some value accumulated
