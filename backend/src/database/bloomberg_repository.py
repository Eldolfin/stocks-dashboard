from pathlib import Path

import pandas as pd

from src.models import HistoricalKPI, HistoricalKPIs


def load_historical_kpis(ticker: str) -> HistoricalKPIs | None:
    file = Path(f"./historical-data/cleaned/{ticker}.csv")
    if not file.is_file():
        return None
    df = pd.read_csv(file, header=0)
    cols = df.columns.to_numpy().reshape(-1, 2)

    res = {}
    for sub_cols in cols:
        kpi = sub_cols[1]
        date_value = df[sub_cols].rename(
            columns={
                sub_cols[0]: "dates",
                sub_cols[1]: "values",
            }
        )

        date_value = date_value.dropna()
        res[kpi] = HistoricalKPI(dates=date_value["dates"].to_list(), values=date_value["values"].to_list())
    return HistoricalKPIs(kpis=res)
