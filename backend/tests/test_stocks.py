import io
import time

import pytest
import requests
from openpyxl import Workbook

BASE_URL = "http://localhost:5000/api"


@pytest.fixture
def registered_user():
    unique_email = f"test_user_stocks_{time.time_ns()}@example.com"
    password = "test_password"
    data = {"email": unique_email, "password": password}
    response = requests.post(f"{BASE_URL}/register", data=data)
    assert response.status_code == 201
    return {"email": unique_email, "password": password}


@pytest.fixture
def logged_in_session(registered_user):
    session = requests.Session()
    data = {"email": registered_user["email"], "password": registered_user["password"]}
    response = session.post(f"{BASE_URL}/login", json=data)
    assert response.status_code == 200, f"Login failed: {response.text}"
    return session


def create_dummy_etoro_excel():
    workbook = Workbook()
    sheet = workbook.active
    sheet.title = "Closed Positions"
    header = [
        "Position ID",
        "Action",
        "Amount",
        "Units",
        "Open Rate",
        "Close Rate",
        "Spread",
        "Profit(USD)",
        "Open Date",
        "Close Date",
        "Leverage",
        "ISIN",
        "Notes",
    ]
    sheet.append(header)
    sample_row = [
        "12345",
        "Buy",
        "100",
        "1",
        "100",
        "110",
        "0.01",
        "10",
        "01/01/2023 10:00:00",
        "02/01/2023 10:00:00",
        "1",
        "US0378331005",
        "",
    ]
    sheet.append(sample_row)

    file_io = io.BytesIO()
    workbook.save(file_io)
    file_io.seek(0)
    return file_io


def test_get_ticker_success() -> None:
    response = requests.get(f"{BASE_URL}/ticker/", params={"ticker_name": "AAPL", "period": "1y"})
    assert response.status_code == 200
    data = response.json()
    assert data["query"]["ticker_name"] == "AAPL"
    assert "dates" in data
    assert "candles" in data
    assert "delta" in data


def test_get_ticker_not_found() -> None:
    response = requests.get(f"{BASE_URL}/ticker/", params={"ticker_name": "INVALIDTICKER", "period": "1y"})
    assert response.status_code == 404


def test_compare_growth() -> None:
    response = requests.get(f"{BASE_URL}/compare_growth/", params={"ticker_names": "AAPL,GOOG", "period": "1y"})
    assert response.status_code == 200
    data = response.json()
    assert "AAPL" in data["candles"]
    assert "GOOG" in data["candles"]
    assert "dates" in data


def test_get_kpis_success() -> None:
    response = requests.get(f"{BASE_URL}/kpis/", params={"ticker_name": "AAPL"})
    assert response.status_code == 200
    data = response.json()
    assert data["query"]["ticker_name"] == "AAPL"
    assert "info" in data
    assert "analyst_price_targets" in data


def test_get_kpis_not_found() -> None:
    response = requests.get(f"{BASE_URL}/kpis/", params={"ticker_name": "INVALIDTICKER"})
    assert response.status_code == 404


def test_search_ticker() -> None:
    response = requests.get(f"{BASE_URL}/search/", params={"query": "Apple"})
    assert response.status_code == 200
    data = response.json()
    assert data["query"]["query"] == "Apple"
    assert "quotes" in data
    assert len(data["quotes"]) > 0
    assert any(q["raw"]["symbol"] == "AAPL" for q in data["quotes"])


def test_analyze_etoro_excel(logged_in_session) -> None:
    dummy_excel = create_dummy_etoro_excel()
    files = {
        "file": (
            "eToro_account_statement.xlsx",
            dummy_excel,
            "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        )
    }
    data = {"precision": "D"}
    response = logged_in_session.post(f"{BASE_URL}/etoro_analysis", files=files, data=data)
    assert response.status_code == 200
    response_data = response.json()
    assert "close_date" in response_data
    assert "closed_trades" in response_data
    assert "profit_usd" in response_data
    assert len(response_data["close_date"]) > 0


def test_list_etoro_reports(logged_in_session) -> None:
    dummy_excel = create_dummy_etoro_excel()
    filename = "my_report_for_listing.xlsx"
    files = {"file": (filename, dummy_excel, "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")}
    data = {"precision": "D"}
    response = logged_in_session.post(f"{BASE_URL}/etoro_analysis", files=files, data=data)
    assert response.status_code == 200

    response = logged_in_session.get(f"{BASE_URL}/etoro/reports")
    assert response.status_code == 200
    assert filename in response.json()["reports"]


def test_analyze_etoro_excel_by_name(logged_in_session) -> None:
    dummy_excel = create_dummy_etoro_excel()
    filename = "my_named_report.xlsx"
    files = {"file": (filename, dummy_excel, "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")}
    data = {"precision": "D"}
    response = logged_in_session.post(f"{BASE_URL}/etoro_analysis", files=files, data=data)
    assert response.status_code == 200

    params = {"filename": filename, "precision": "D"}
    response = logged_in_session.get(f"{BASE_URL}/etoro_analysis_by_name", params=params)
    assert response.status_code == 200
    response_data = response.json()
    assert "close_date" in response_data
    assert "closed_trades" in response_data
    assert "profit_usd" in response_data
    assert len(response_data["close_date"]) > 0


def test_analyze_etoro_excel_by_name_not_found(logged_in_session) -> None:
    params = {"filename": "non_existent_report.xlsx", "precision": "D"}
    response = logged_in_session.get(f"{BASE_URL}/etoro_analysis_by_name", params=params)
    assert response.status_code == 404
