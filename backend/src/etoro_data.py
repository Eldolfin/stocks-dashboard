import pandas as pd
from io import BytesIO


def extract_closed_position(etoro_statement: bytes):
    excel = pd.read_excel(BytesIO(etoro_statement), sheet_name=None)
    return excel["Closed Positions"]
