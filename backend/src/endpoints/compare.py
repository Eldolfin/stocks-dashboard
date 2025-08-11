from pathlib import Path
from typing import Any

import pandas as pd
import yfinance as yf
from flask import current_app, request
from flask_login import current_user, login_required
from flask_openapi3 import APIBlueprint

from src.services import etoro_data

compare_bp = APIBlueprint("compare", __name__, url_prefix="/api/etoro")


def _extract_etoro_data(file_path: Path) -> tuple[list[str], list[float]]:
    """Extract portfolio evolution dates and deposits from eToro report."""
    evolution = etoro_data.extract_portfolio_evolution(file_path, lambda _progress: None)
    dates = evolution.dates
    deposits = evolution.parts.get("Deposits")
    if not deposits:
        msg = "No deposit data found"
        raise ValueError(msg)
    return dates, deposits


def _get_index_prices(index_ticker: str, dates: list[str]) -> pd.Series:
    """Fetch and process index historical prices."""
    # yfinance end is exclusive; extend by one day to cover the last date
    index_data = yf.download(
        index_ticker, start=dates[0], end=pd.to_datetime(dates[-1]) + pd.Timedelta(days=1)
    )
    if getattr(index_data, "empty", True):
        msg = "No index data found"
        raise ValueError(msg)

    # Select a suitable price series
    if isinstance(index_data, pd.Series):
        index_prices = index_data
    elif isinstance(index_data, pd.DataFrame):
        # Handle MultiIndex columns (e.g., multi-ticker) or regular DataFrame
        cols = index_data.columns
        if isinstance(cols, pd.MultiIndex):
            # Try to get the 'Adj Close' slice across tickers
            try:
                sub = index_data.xs("Adj Close", axis=1, level=0)
            except Exception:
                try:
                    sub = index_data.xs("Close", axis=1, level=0)
                except Exception as e:
                    msg = "No close price column in index data (multiindex)"
                    raise ValueError(msg) from e
            # If multiple columns, pick the first
            index_prices = sub.iloc[:, 0] if isinstance(sub, pd.DataFrame) else sub
        else:
            price_col = None
            for col in ["Adj Close", "Close", "adjclose", "close", "AdjClose"]:
                if col in cols:
                    price_col = col
                    break
            if price_col is None:
                msg = "No close price column in index data"
                raise ValueError(msg)
            index_prices = index_data[price_col]
    else:
        msg = "Unexpected index data format"
        raise TypeError(msg)

    index_prices = pd.to_numeric(index_prices, errors="coerce")
    # Normalize index to string dates and forward/back-fill to align with portfolio dates (includes weekends)
    index_prices.index = pd.to_datetime(index_prices.index).tz_localize(None).strftime("%Y-%m-%d")
    # Ensure uniqueness by taking last if duplicates (e.g., intraday)
    index_prices = index_prices.groupby(index_prices.index).last()
    return index_prices.reindex(dates).ffill().bfill()


def _simulate_index_investment(
    dates: list[str], deposits: list[float], index_prices: pd.Series
) -> list[float]:
    """Simulate index investment strategy based on deposit history."""
    units = 0.0
    units_history = []
    # deposits from evolution are cumulative; derive daily deposits
    daily_deposits = [max(0.0, float(deposits[0]))]
    for i in range(1, len(deposits))
        daily = float(deposits[i]) - float(deposits[i - 1])
        daily_deposits.append(max(0.0, daily))

    for i, date in enumerate(dates):
        deposit = daily_deposits[i]
        price = float(index_prices.loc[date]) if date in index_prices.index else None
        if price and deposit > 0:
            units += deposit / price
        units_history.append(units)

    # Calculate cumulative value
    return [
        float(u) * float(index_prices.loc[date]) if date in index_prices.index else 0.0
        for u, date in zip(units_history, dates, strict=False)
    ]


@compare_bp.post("/compare_to_index")
@login_required
def compare_to_index() -> tuple[dict[str, Any] | dict[str, str], int]:
    """
    Compare eToro portfolio performance to a selected index.
    Expects JSON: {"filename": str, "index_ticker": str}
    Returns: {"dates": [...], "index_values": [...]}
    """
    data = request.get_json()
    filename = data.get("filename")
    index_ticker = data.get("index_ticker")
    if not filename or not index_ticker:
        return {"error": "Missing filename or index_ticker"}, 400

    # Locate user upload folder
    user_email = current_user.email
    upload_folder = Path(current_app.config["UPLOAD_FOLDER"]) / user_email
    file_path = upload_folder / filename
    if not file_path.exists():
        return {"error": "File not found"}, 404

    # Extract deposit history
    try:
        dates, deposits = _extract_etoro_data(file_path)
    except Exception as e:
        return {"error": f"Failed to parse eToro report: {e!s}"}, 500

    # Fetch index historical prices
    try:
        index_prices = _get_index_prices(index_ticker, dates)
    except Exception as e:
        return {"error": f"Failed to fetch index data: {e!s}"}, 500

    # Simulate index investment at each deposit date
    try:
        index_values = _simulate_index_investment(dates, deposits, index_prices)
    except Exception as e:
        return {"error": f"Simulation error: {e!s}"}, 500

    return {"dates": dates, "index_values": index_values}, 200
