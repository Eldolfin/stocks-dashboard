from pathlib import Path

import pandas as pd  # type: ignore


def column_date_to_timestamp(column: pd.Series) -> pd.Series:
    return pd.to_datetime(column, format="%d/%m/%Y %H:%M:%S")


def extract_closed_position(etoro_statement_file: Path, time_unit: str = "m") -> dict[str, list[str]]:
    excel = pd.read_excel(etoro_statement_file, sheet_name=None)
    closed_positions_df = excel["Closed Positions"]
    closed_positions_df["Close Date"] = column_date_to_timestamp(
        closed_positions_df["Close Date"],
    )
    closed_positions_df["Open Date"] = column_date_to_timestamp(
        closed_positions_df["Open Date"],
    )
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

    return {column: gains[column].tolist() for column in gains.columns}
