from pathlib import Path

import pandas as pd
import yfinance as yf

from src.services import etoro_data


class CompareToIndexService:
    @staticmethod
    def extract_etoro_data(file_path: Path) -> tuple[list[str], list[float]]:
        """Extract portfolio evolution dates and deposits from eToro report."""
        evolution = etoro_data.extract_portfolio_evolution(file_path, lambda _progress: None)
        dates = evolution.dates
        deposits = evolution.parts.get("Deposits")
        if not deposits:
            msg = "No deposit data found"
            raise ValueError(msg)
        return dates, deposits

    @staticmethod
    def get_index_prices(index_ticker: str, dates: list[str]) -> pd.Series:
        # yfinance end is exclusive; extend by one day to cover the last date
        index_data = yf.download(
            index_ticker, start=dates[0], end=pd.to_datetime(dates[-1]) + pd.Timedelta(days=1)
        )
        if getattr(index_data, "empty", True):
            msg = "No index data found"
            raise ValueError(msg)
        if isinstance(index_data, pd.Series):
            index_prices = index_data
        elif isinstance(index_data, pd.DataFrame):
            cols = index_data.columns
            if isinstance(cols, pd.MultiIndex):
                try:
                    sub = index_data.xs("Adj Close", axis=1, level=0)
                except Exception:
                    try:
                        sub = index_data.xs("Close", axis=1, level=0)
                    except Exception as e:
                        msg = "No close price column in index data (multiindex)"
                        raise ValueError(msg) from e
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
        index_prices.index = pd.to_datetime(index_prices.index).tz_localize(None).strftime("%Y-%m-%d")
        index_prices = index_prices.groupby(index_prices.index).last()
        return index_prices.reindex(dates).ffill().bfill()

    @staticmethod
    def simulate_index_investment(
        dates: list[str], deposits: list[float], index_prices: pd.Series
    ) -> list[float]:
        units = 0.0
        units_history = []
        daily_deposits = [max(0.0, float(deposits[0]))]
        for i in range(1, len(deposits)):
            daily = float(deposits[i]) - float(deposits[i - 1])
            daily_deposits.append(max(0.0, daily))
        for i, date in enumerate(dates):
            deposit = daily_deposits[i]
            price = float(index_prices.loc[date]) if date in index_prices.index else None
            if price and deposit > 0:
                units += deposit / price
            units_history.append(units)
        return [
            float(u) * float(index_prices.loc[date]) if date in index_prices.index else 0.0
            for u, date in zip(units_history, dates, strict=False)
        ]
