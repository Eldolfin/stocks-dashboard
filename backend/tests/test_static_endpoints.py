import requests

BASE_URL = "http://localhost:5000/api"


def test_static_top_indexes_served():
    resp = requests.get(f"{BASE_URL}/static/top_indexes.csv")
    assert resp.status_code == 200, resp.text
    text = resp.text.strip()
    # Basic shape check: header and a known symbol
    assert text.splitlines()[0].startswith("Ticker,Name"), "CSV header missing"
    assert "^GSPC,S&P 500" in text


def test_static_top_cryptos_served():
    resp = requests.get(f"{BASE_URL}/static/top_cryptos.csv")
    assert resp.status_code == 200, resp.text
    text = resp.text.strip()
    assert text.splitlines()[0].startswith("Ticker,Name"), "CSV header missing"
    assert "BTC-USD,Bitcoin" in text
