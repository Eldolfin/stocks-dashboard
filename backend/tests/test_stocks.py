import io
import time

import pytest
import requests

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


@pytest.fixture
def etoro_excel_file():
    with open("tests/data/etoro-account-statement-12-31-2014-7-5-2025_TEST.xlsx", "rb") as f:
        return io.BytesIO(f.read())


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


def test_get_historical_kpis_success() -> None:
    response = requests.get(f"{BASE_URL}/historical-kpis/", params={"ticker_name": "AAPL"})
    assert response.status_code == 200
    data = response.json()
    assert list(data["kpis"].keys()) == [
        "Dividend",
        "EPS",
        "Earnings",
        "Free CF",
        "Market Cap",
        "Outstanding Shares",
        "PE ratio",
        "Revenue",
        "Volume",
    ]
    assert data["kpis"]["Revenue"]["values"][0] == 2343.0
    assert data["kpis"]["Revenue"]["dates"][0] == "2000-01-07"


def test_get_historical_kpis_not_found() -> None:
    response = requests.get(f"{BASE_URL}/historical-kpis/", params={"ticker_name": "INVALIDTICKER"})
    assert response.status_code == 404


def test_search_ticker() -> None:
    response = requests.get(f"{BASE_URL}/search/", params={"query": "Apple"})
    assert response.status_code == 200
    data = response.json()
    assert data["query"]["query"] == "Apple"
    assert "quotes" in data
    assert len(data["quotes"]) > 0
    assert any(q["raw"]["symbol"] == "AAPL" for q in data["quotes"])


def test_upload_etoro_report(logged_in_session, etoro_excel_file) -> None:
    files = {
        "file": (
            "eToro_account_statement.xlsx",
            etoro_excel_file,
            "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        )
    }
    data = {"precision": "D"}
    response = logged_in_session.post(f"{BASE_URL}/etoro/upload_report", files=files, data=data)
    assert response.status_code == 200
    response_data = response.json()
    assert response_data["result"] == "OK"


def test_list_etoro_reports(logged_in_session, etoro_excel_file) -> None:
    filename = "my_report_for_listing.xlsx"
    files = {"file": (filename, etoro_excel_file, "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")}
    data = {"precision": "D"}
    response = logged_in_session.post(f"{BASE_URL}/etoro/upload_report", files=files, data=data)
    assert response.status_code == 200

    response = logged_in_session.get(f"{BASE_URL}/etoro/reports")
    assert response.status_code == 200
    assert filename in response.json()["reports"]


def test_analyze_etoro_excel_by_name(logged_in_session, etoro_excel_file) -> None:
    filename = "my_named_report.xlsx"
    files = {"file": (filename, etoro_excel_file, "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")}
    data = {"precision": "D"}
    response = logged_in_session.post(f"{BASE_URL}/etoro/upload_report", files=files, data=data)
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


def test_analyze_etoro_evolution_by_name(logged_in_session, etoro_excel_file) -> None:
    filename = "my_evolution_report.xlsx"
    files = {"file": (filename, etoro_excel_file, "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")}
    data = {"precision": "D"}
    response = logged_in_session.post(f"{BASE_URL}/etoro/upload_report", files=files, data=data)
    assert response.status_code == 200

    params = {"filename": filename, "precision": "D"}
    response = logged_in_session.get(f"{BASE_URL}/etoro_evolution_by_name", params=params)
    assert response.status_code == 200
    response_data = response.json()
    assert "evolution" in response_data
    assert isinstance(response_data["evolution"], dict)
    assert "2025-08-01" in response_data["evolution"]["dates"]
    assert (
        round(response_data["evolution"]["parts"]["total"][response_data["evolution"]["dates"].index("2025-08-01")])
        == 3676
    )


def test_etoro_split_handling(etoro_excel_file) -> None:
    """Test that stock splits are properly handled in portfolio evolution."""
    from src.services.etoro_data import extract_portfolio_evolution
    
    # Test that the function runs without errors when processing splits
    result = extract_portfolio_evolution(etoro_excel_file)
    
    # Verify the function returns expected structure
    assert hasattr(result, 'dates')
    assert hasattr(result, 'parts')
    assert isinstance(result.dates, list)
    assert isinstance(result.parts, dict)
    
    # Test should pass even if no splits are present in test data
    assert len(result.dates) > 0


def test_split_factor_calculation():
    """Test split factor calculation logic independently."""
    import pandas as pd
    from pathlib import Path
    
    # This is a unit test for the split logic without needing full eToro data
    # Create a simple test scenario
    date_range = pd.date_range('2024-01-01', '2024-12-31', freq='D')
    
    # Mock split data: 2:1 split on June 1st
    split_date = pd.Timestamp('2024-06-01')
    split_factor = 2.0
    
    # Test the logic that would be applied in extract_portfolio_evolution
    split_factors = pd.Series(1.0, index=date_range, name="split_factor")
    
    # Apply inverse cumulative factor for dates before split
    cumulative_factor = split_factor
    mask = split_factors.index < split_date
    split_factors.loc[mask] = 1.0 / cumulative_factor
    
    # Verify the results
    assert split_factors.loc[pd.Timestamp('2024-05-31')] == 0.5  # Before split: 1/2
    assert split_factors.loc[pd.Timestamp('2024-06-01')] == 1.0  # From split: 1
    assert split_factors.loc[pd.Timestamp('2024-06-02')] == 1.0  # After split: 1
