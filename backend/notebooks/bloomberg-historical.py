import marimo

__generated_with = "0.14.16"
app = marimo.App(width="full")


@app.cell
def _():
    import pandas as pd
    import numpy as np
    from glob import glob
    import marimo as mo
    from pydantic import BaseModel

    return BaseModel, glob, mo, pd


@app.cell
def _(mo):
    mo.md(r"""## Clean data (split into one csv file per ticker)""")
    return


@app.cell
def _(glob):
    all_files = glob("./historical-data/history*.xlsx")
    files_multi = glob("./historical-data/history*10 stocks*.xlsx")
    files_single = list(set(all_files) - set(files_multi))
    return (files_multi,)


@app.cell
def _(files_multi, mo, pd):
    for file in mo.status.progress_bar(files_multi, title="reading multi file"):
        multi = pd.read_excel(
            file,
            header=1,
        )
        reshaped_columns = multi.columns[1:-27].to_numpy().reshape(-1, 29)

        for sub_cols in reshaped_columns:
            sub_df = multi[sub_cols]
            ticker = sub_df.columns[0].split(" ")[0].replace("/", "-")
            sub_df = sub_df.iloc[:, 1:]
            _cols = sub_df.columns[:-1].to_numpy().reshape(-1, 3)
            selected_cols = []
            rename = {}

            for i in range(_cols.shape[0]):
                col1, col2 = _cols[i][0], _cols[i][1]
                selected_cols.extend([col1, col2])
                if i == _cols.shape[0] - 1:
                    rename[col1] = f"date_{col1}"
                    rename[col2] = col1
                else:
                    rename[col1] = f"date_{col2}"
                sub_df[col2] = pd.to_numeric(sub_df[col2], errors="coerce")

            # Select the columns
            sub_df_cleaned = sub_df[selected_cols].rename(columns=rename)
            sub_df_cleaned = sub_df_cleaned.rename(columns=lambda x: x.split(".")[0])

            sub_df_cleaned.to_csv(f"./historical-data/cleaned/{ticker}.csv")
    return (ticker,)


@app.cell
def _(ticker):
    ticker
    return


@app.cell
def _(mo):
    mo.md(r"""## Retrieve a ticker historical KPIs""")
    return


@app.cell
def _(BaseModel, pd):
    class HistoricalKPI(BaseModel):
        dates: list[str]
        values: list[float]

    class HistoricalKPIs(BaseModel):
        kpis: dict[str, HistoricalKPI]

    def load_historical_kpis(ticker: str) -> HistoricalKPIs:
        df = pd.read_csv(f"./historical-data/cleaned/{ticker}.csv", header=0)
        cols = df.columns[1:].to_numpy().reshape(-1, 2)

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
            date_value = date_value.to_dict("list")
            res[kpi] = HistoricalKPI(dates=date_value["dates"], values=date_value["values"])
        return HistoricalKPIs(kpis=res)

    # load_historical_kpis("DUOL")
    # load_historical_kpis("GOOG")
    load_historical_kpis("BAS")
    return


if __name__ == "__main__":
    app.run()
