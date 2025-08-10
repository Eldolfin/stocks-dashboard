import marimo

__generated_with = "0.14.16"
app = marimo.App(width="full")


@app.cell
def _():
    from pathlib import Path

    import numpy as np
    import pandas as pd
    import yfinance as yf
    import yfinance_cache as yfc
    import matplotlib.pyplot as plt

    from src import models
    from src.services.etoro_data import column_date_to_timestamp

    return Path, column_date_to_timestamp, models, np, pd, plt, yf


@app.cell
def _(yf):
    yf.Search
    return


@app.cell
def _(Path, column_date_to_timestamp, models, np, pd, yf):
    def compare_portfolio_to_simulation(etoro_statement_file: Path, reference: str) -> models.EtoroEvolutionInner:  # noqa: C901, PLR0912, PLR0915
        excel = pd.read_excel(etoro_statement_file, sheet_name=None)
        closed = excel["Closed Positions"]
        closed["Close Date"] = column_date_to_timestamp(closed["Close Date"])
        closed = closed.sort_values(by="Close Date")
        closed = closed.set_index(closed["Close Date"])
        closed["Profit(USD)"] = closed["Profit(USD)"].astype(np.float32)
        closed = closed.resample("D").agg({"Profit(USD)": "sum"}).fillna(0)
        closed["Cumulative Profit"] = closed["Profit(USD)"].cumsum()

        activity = excel["Account Activity"]
        activity["Date"] = column_date_to_timestamp(activity["Date"])
        activity = activity.set_index("Date")

        daily_deposits = activity[activity["Type"] == "Deposit"]["Amount"].astype(
            np.float32
        )  # .resample("D").sum().fillna(0)
        daily_deposits.index = pd.to_datetime(daily_deposits.index.date)

        cumulative_deposits = pd.DataFrame(daily_deposits)
        start_date = daily_deposits.index.min()
        end_date = pd.Timestamp.today()
        date_range = pd.date_range(start=start_date, end=end_date, freq="D")
        index_price = yf.Ticker(reference).history(start=start_date, end=end_date)[["Close"]]
        index_price.index = pd.to_datetime(index_price.index.date)
        full_range = pd.date_range(start=start_date, end=end_date, freq="D")
        index_price = index_price.reindex(full_range).ffill()
        cumulative_deposits = cumulative_deposits.reindex(full_range).fillna(0)
        virtual_portfolio = cumulative_deposits.join(index_price).ffill()
        virtual_portfolio["Units"] = virtual_portfolio["Amount"] / virtual_portfolio["Close"]
        virtual_portfolio["UnitsCum"] = virtual_portfolio["Units"].cumsum()
        virtual_portfolio["UnitsCumWorth"] = virtual_portfolio["UnitsCum"] * virtual_portfolio["Close"]
        return virtual_portfolio

        parts = {
            str(k): [float(x) for x in v]
            for k, v in _all_data.reset_index().drop(columns=["index"]).to_dict("list").items()
        }
        return models.EtoroEvolutionInner(
            dates=_all_data.index.astype(str).to_list(),
            parts=parts,
        )

    return (compare_portfolio_to_simulation,)


@app.cell
def _(compare_portfolio_to_simulation):
    if_i_bought_only_sp500 = compare_portfolio_to_simulation(
        "~/Downloads/etoro-account-statement-12-31-2014-8-7-2025.xlsx", "^GSPC"
    )
    if_i_bought_only_sp500
    return (if_i_bought_only_sp500,)


@app.cell
def _(if_i_bought_only_sp500, plt):
    plt.figure(figsize=(12, 8))
    plt.plot(if_i_bought_only_sp500, label=if_i_bought_only_sp500.columns)
    plt.xlabel("Time", fontsize=12)
    plt.ylabel("Value", fontsize=12)
    plt.title("SP500 Investment Over Time", fontsize=14)
    plt.legend(fontsize=10)
    plt.gca()
    return


if __name__ == "__main__":
    app.run()
