import pandas as pd
from io import BytesIO


def column_date_to_timestamp(column: pd.Series) -> pd.Series:
    return (
        pd.to_datetime(column, format="%d/%m/%Y %H:%M:%S").astype("int64")
        // 10**9
    )


def extract_closed_position(etoro_statement: bytes):
    excel = pd.read_excel(BytesIO(etoro_statement), sheet_name=None)
    closed_positions_df = excel["Closed Positions"]
    closed_positions_df["Close Date"] = column_date_to_timestamp(
        closed_positions_df["Close Date"]
    )
    closed_positions_df["Open Date"] = column_date_to_timestamp(
        closed_positions_df["Open Date"]
    )
    closed_positions = {
        column: closed_positions_df[column].dropna().tolist()
        for column in closed_positions_df.columns
    }
    return closed_positions
