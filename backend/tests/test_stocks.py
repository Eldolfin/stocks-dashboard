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
        == 2986
    )


def test_search_caching_integration() -> None:
    """Test that search results are properly cached."""
    # First search - should populate cache
    response1 = requests.get(f"{BASE_URL}/search/", params={"query": "Apple"})
    assert response1.status_code == 200
    data1 = response1.json()
    
    # Second identical search - should use cache (faster response)
    start_time = time.time()
    response2 = requests.get(f"{BASE_URL}/search/", params={"query": "Apple"})
    response_time = time.time() - start_time
    
    assert response2.status_code == 200
    data2 = response2.json()
    
    # Results should be identical
    assert data1 == data2
    
    # Cached response should be fast (less than 100ms)
    assert response_time < 0.1


def test_cache_stats_endpoint() -> None:
    """Test the cache statistics endpoint."""
    # Clear any existing cache by making a unique search
    unique_query = f"test_query_{time.time_ns()}"
    response = requests.get(f"{BASE_URL}/search/", params={"query": unique_query})
    assert response.status_code == 200
    
    # Get cache stats
    response = requests.get(f"{BASE_URL}/cache/stats")
    assert response.status_code == 200
    
    data = response.json()
    assert "search_cache" in data
    
    cache_stats = data["search_cache"]
    assert "exact_cache_size" in cache_stats
    assert "ticker_cache_size" in cache_stats
    assert "query_patterns" in cache_stats
    
    # All values should be non-negative integers
    assert isinstance(cache_stats["exact_cache_size"], int)
    assert isinstance(cache_stats["ticker_cache_size"], int)
    assert isinstance(cache_stats["query_patterns"], int)
    assert cache_stats["exact_cache_size"] >= 0
    assert cache_stats["ticker_cache_size"] >= 0
    assert cache_stats["query_patterns"] >= 0


def test_search_partial_matching() -> None:
    """Test that cached ticker data enables partial matching."""
    # Search for a broad term that will cache multiple tickers
    response1 = requests.get(f"{BASE_URL}/search/", params={"query": "technology"})
    assert response1.status_code == 200
    data1 = response1.json()
    
    # Assume Apple might be in technology results
    has_apple = any(q["raw"]["symbol"] == "AAPL" for q in data1["quotes"])
    
    if has_apple:
        # Now search for just "apple" - should find it from cache
        response2 = requests.get(f"{BASE_URL}/search/", params={"query": "apple"})
        assert response2.status_code == 200
        data2 = response2.json()
        
        # Should find Apple from partial matching
        assert any(q["raw"]["symbol"] == "AAPL" for q in data2["quotes"])
