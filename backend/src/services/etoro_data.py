from collections.abc import Callable
from pathlib import Path

import numpy as np
import pandas as pd
import yfinance as yf

from src import models


def column_date_to_timestamp(column: pd.Series) -> pd.Series:
    return pd.to_datetime(column, format="%d/%m/%Y %H:%M:%S")


def extract_closed_position(
    etoro_statement_file: Path,
    time_unit: str = "m",
    progress_callback: Callable[[str, int, int], None] | None = None
) -> dict[str, list[str]]:
    """Extract closed positions with optional progress reporting."""
    total_steps = 4

    if progress_callback:
        progress_callback("Reading Excel file", 1, total_steps)

    excel = pd.read_excel(etoro_statement_file, sheet_name=None)
    closed_positions_df = excel["Closed Positions"]

    if progress_callback:
        progress_callback("Processing dates", 2, total_steps)

    closed_positions_df["Close Date"] = column_date_to_timestamp(
        closed_positions_df["Close Date"],
    )
    closed_positions_df["Open Date"] = column_date_to_timestamp(
        closed_positions_df["Open Date"],
    )

    if progress_callback:
        progress_callback("Calculating gains", 3, total_steps)

    gains_graphs_columns = {
        "Close Date": "close_date",
        "Profit(USD)": "profit_usd",
    }
    gains = closed_positions_df[gains_graphs_columns.keys()].reset_index()
    gains = gains.rename(columns=gains_graphs_columns)
    gains = (
        gains.groupby(gains["close_date"].dt.to_period(time_unit))
        .agg(
            profit_usd=("profit_usd", "sum"),
            closed_trades=("profit_usd", "count"),
        )
        .reset_index()
    )
    gains["close_date"] = gains["close_date"].dt.to_timestamp()
    gains["close_date"] = gains["close_date"].dt.strftime("%Y-%m-%dT%H:%M:%S")

    if progress_callback:
        progress_callback("Finalizing results", 4, total_steps)

    return {column: gains[column].tolist() for column in gains.columns}


def extract_portfolio_evolution(  # noqa: C901, PLR0912, PLR0915
    etoro_statement_file: Path,
    progress_callback: Callable[[str, int, int], None] | None = None
) -> models.EtoroEvolutionInner:
    """Extract portfolio evolution with optional progress reporting."""
    total_steps = 6

    if progress_callback:
        progress_callback("Reading Excel file", 1, total_steps)

    excel = pd.read_excel(etoro_statement_file, sheet_name=None)

    if progress_callback:
        progress_callback("Processing closed positions", 2, total_steps)

    closed = excel["Closed Positions"]
    closed["Close Date"] = column_date_to_timestamp(closed["Close Date"])
    closed = closed.sort_values(by="Close Date")
    closed = closed.set_index(closed["Close Date"])
    closed["Profit(USD)"] = closed["Profit(USD)"].astype(np.float32)
    closed = closed.resample("D").agg({"Profit(USD)": "sum"}).fillna(0)
    closed["Cumulative Profit"] = closed["Profit(USD)"].cumsum()

    if progress_callback:
        progress_callback("Processing open positions", 3, total_steps)

    activity = excel["Account Activity"]
    activity = activity[activity["Asset type"] != "Crypto"].copy()
    activity["Date"] = column_date_to_timestamp(activity["Date"])
    activity = activity.set_index("Date")

    open_positions = activity[activity["Type"] == "Open Position"]
    closed_positions = activity[activity["Type"] == "Position closed"]
    closed_position_ids = closed_positions["Position ID"].dropna().astype(str)
    still_open = open_positions[~open_positions["Position ID"].isin(closed_position_ids)].copy()

    shares_per_ticker = {}
    for tick in still_open["Details"].unique():
        _ticker_positions = still_open[still_open["Details"] == tick].copy()
        _ticker_positions = _ticker_positions.sort_values(by="Date")
        _ticker_positions["Units / Contracts"] = _ticker_positions["Units / Contracts"].astype(np.float32)
        _ticker_positions = _ticker_positions.resample("D").agg({"Units / Contracts": "sum"}).fillna(0)
        _ticker_positions = _ticker_positions.reindex(
            pd.date_range(_ticker_positions.index.min(), pd.Timestamp.today()),
            fill_value=0,
        )
        _ticker_positions["shares_sum"] = _ticker_positions["Units / Contracts"].cumsum()
        shares_per_ticker[tick] = _ticker_positions

    if progress_callback:
        progress_callback("Fetching market data", 4, total_steps)

    yahoo_data = {}
    for _details in still_open["Details"].unique():
        first_open_date = still_open[still_open["Details"] == _details].index.min()
        [ticker, market] = _details.split("/")
        if market != "USD":
            continue
        ticker_data = yf.Ticker(ticker)
        history = ticker_data.history(
            start=first_open_date.strftime("%Y-%m-%d"),
            end=pd.Timestamp.now().strftime("%Y-%m-%d"),
        )
        yahoo_data[_details] = history

    if progress_callback:
        progress_callback("Combining portfolio data", 5, total_steps)

    all_combined_data = {}
    for _ticker_name, _ticker in shares_per_ticker.items():
        if _ticker_name in yahoo_data:
            _yahoo_data = yahoo_data[_ticker_name]
            _ticker.index = pd.to_datetime(_ticker.index).tz_localize(None)
            _yahoo_data.index = pd.to_datetime(_yahoo_data.index).tz_localize(None)
            combined = _ticker.join(_yahoo_data, how="left")
            combined["net_value"] = combined["Close"] * combined["shares_sum"]
            all_combined_data[_ticker_name] = combined

    all_combined_data_filled = {}
    for _stock, _df in all_combined_data.items():
        all_combined_data_filled[_stock] = _df.ffill()

    if progress_callback:
        progress_callback("Finalizing evolution", 6, total_steps)

    _all_data = pd.DataFrame()
    all_profits = dict(all_combined_data_filled)
    all_profits["Closed Positions"] = closed.rename(columns={"Cumulative Profit": "net_value"})
    for _stock, _df in all_profits.items():
        _all_data = _all_data.join(
            _df[["net_value"]].rename(columns={"net_value": _stock}),
            how="outer",
        )
    _all_data = _all_data.ffill().fillna(0)
    _all_data["total"] = _all_data.sum(axis=1)
    _all_data.index = pd.to_datetime(_all_data.index).strftime("%Y-%m-%d")
    parts = {
        str(k): [float(x) for x in v]
        for k, v in _all_data.reset_index().drop(columns=["index"]).to_dict("list").items()
    }
    return models.EtoroEvolutionInner(
        dates=_all_data.index.astype(str).to_list(),
        parts=parts,
    )
