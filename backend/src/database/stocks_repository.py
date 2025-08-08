import pandas as pd
import yfinance as yf


def get_ticker_history(ticker_name: str, period: str, interval: str) -> pd.DataFrame:
    dat = yf.Ticker(ticker_name)
    return dat.history(period=period, interval=interval).reset_index()


def get_ticker_history_from_start(ticker_name: str, start: str, interval: str) -> pd.DataFrame:
    dat = yf.Ticker(ticker_name)
    return dat.history(start=start, interval=interval).reset_index()


def get_tickers_history(ticker_names: list[str], period: str) -> pd.DataFrame:
    dat = yf.Tickers(ticker_names)
    return dat.history(period=period)


def get_ticker_info(ticker_name: str) -> pd.DataFrame:
    dat = yf.Ticker(ticker_name)
    return dat.info


def get_ticker_analyst_price_targets(ticker_name: str) -> pd.DataFrame:
    dat = yf.Ticker(ticker_name)
    return dat.analyst_price_targets


def search(query: str) -> list:
    return yf.Search(query).quotes


def get_tickers(ticker_names: list[str]) -> dict[str, pd.DataFrame]:
    return yf.Tickers(ticker_names).tickers
