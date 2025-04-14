import pandas as pd
from io import BytesIO


def extract_closed_position(etoro_statement: bytes):
    excel = pd.read_excel(BytesIO(etoro_statement), sheet_name=None)
    closed_positions_df = excel["Closed Positions"]
    closed_positions = {
        column: closed_positions_df[column].dropna().tolist()
        for column in closed_positions_df.columns
    }
    return closed_positions
