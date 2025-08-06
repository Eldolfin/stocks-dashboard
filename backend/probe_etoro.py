# /// script
# [tool.marimo.runtime]
# auto_instantiate = false
# ///

import marimo

__generated_with = "0.14.16"
app = marimo.App(width="medium")

with app.setup:
    # Initialization code that runs before all other cells
    import pandas as pd
    import src.services.etoro_data as etoro
    import matplotlib.pyplot as plt
    import numpy as np
    import marimo as mo
    import yfinance as yf
    import logging as log
    import src.models as models


@app.cell(hide_code=True)
def _():
    mo.md("""# Etoro networth analysis""")
    return


@app.cell(hide_code=True)
def _():
    mo.md("""## Data Import and Preparation""")
    return


@app.cell
def _():
    excel = pd.read_excel(
        "~/Downloads/etoro-account-statement-12-31-2014-7-5-2025.xlsx",
        sheet_name=None,
    )
    return (excel,)


@app.cell
def _(excel):
    closed = excel["Closed Positions"]
    # Convert 'Close Date' to datetime objects
    closed["Close Date"] = etoro.column_date_to_timestamp(closed["Close Date"])

    # Sort the DataFrame by 'Close Date'
    closed = closed.sort_values(by="Close Date")
    closed = closed.set_index(closed["Close Date"])
    closed["Profit(USD)"] = closed["Profit(USD)"].astype(np.float32)
    closed = (
        closed.resample("D")
        .agg({"Profit(USD)": "sum"})
        .fillna(0)
    )
    closed
    return (closed,)


@app.cell(hide_code=True)
def _():
    mo.md("""## Cumulative profit of closed trades""")
    return


@app.cell
def _(closed):


    # Calculate cumulative profit
    closed["Cumulative Profit"] = closed["Profit(USD)"].cumsum()



    # Plotting
    plt.plot(closed.index, closed["Cumulative Profit"])
    plt.xlabel("Close Date")
    plt.ylabel("Cumulative Profit (USD)")
    plt.title("Cumulative Profit of Closed Trades Over Time")
    plt.grid(True)
    plt.xticks(rotation=45)  # Rotate x-axis labels for better readability
    plt.tight_layout()  # Adjust layout to prevent labels from overlapping
    plt.gca()
    return


@app.cell(hide_code=True)
def _():
    mo.md("""## Cumulative deposits""")
    return


@app.cell
def _(excel):
    activity = excel["Account Activity"]

    activity = activity[activity["Asset type"] != "Crypto"].copy()
    # Ensure 'Date' is datetime objects
    activity["Date"] = etoro.column_date_to_timestamp(activity["Date"])

    # Set 'Date' as index for resampling
    activity = activity.set_index("Date")

    # Resample to daily frequency, filling missing values with 0
    daily_deposits = (
        activity[activity["Type"] == "Deposit"]["Amount"]
        .astype(np.float32)
        .resample("D")
        .sum()
        .fillna(0)
    )

    # Calculate cumulative deposits
    cumulative_deposits = daily_deposits.cumsum()

    # Create a date range for the x-axis
    start_date = daily_deposits.index.min()
    end_date = daily_deposits.index.max()
    date_range = pd.date_range(start=start_date, end=end_date, freq="D")

    # Reindex the cumulative deposits to ensure all dates are present
    cumulative_deposits = cumulative_deposits.reindex(date_range, fill_value=0)

    # Plotting
    plt.plot(cumulative_deposits.index, cumulative_deposits)
    plt.xlabel("Date")
    plt.ylabel("Cumulative Deposits (USD)")
    plt.title("Cumulative Deposits Over Time (Daily)")
    plt.grid(True)
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.gca()
    return (activity,)


@app.cell(hide_code=True)
def _():
    mo.md("""## Open positions price estimation""")
    return


@app.cell
def _(activity):
    open_positions = activity[activity["Type"] == "Open Position"]
    closed_positions = activity[activity["Type"] == "Position closed"]

    open_position_ids = open_positions["Position ID"].dropna().astype(str)
    closed_position_ids = closed_positions["Position ID"].dropna().astype(str)

    still_open = open_positions[
        ~open_positions["Position ID"].isin(closed_position_ids)
    ].copy()
    # still_open["Details"] = still_open["Details"].str.replace(
    #     r"/(.+)$", "", regex=True
    # )
    still_open
    return (still_open,)


@app.cell
def _(still_open):
    shares_per_ticker = {}
    for tick in still_open["Details"].unique():
        _ticker_positions = still_open[still_open["Details"] == tick].copy()
        _ticker_positions = _ticker_positions.sort_values(by="Date")
        _ticker_positions["Units / Contracts"] = _ticker_positions[
            "Units / Contracts"
        ].astype(np.float32)
        _ticker_positions = (
            _ticker_positions.resample("D")
            .agg({"Units / Contracts": "sum"})
            .fillna(0)
        )
        _ticker_positions = _ticker_positions.reindex(
            pd.date_range(_ticker_positions.index.min(), pd.Timestamp.today()),
            fill_value=0,
        )
        try:
            _ticker_positions["shares_sum"] = _ticker_positions[
                "Units / Contracts"
            ].cumsum()
        except Exception as e:
            print(f"FAILED FOR {tick}: {e}")
            continue
        shares_per_ticker[tick] = _ticker_positions
    # shares_per_ticker
    return (shares_per_ticker,)


@app.cell
def _(shares_per_ticker):
    reel = shares_per_ticker

    # Plotting the cumulative sum for all tickers on the same plot
    fig, ax = plt.subplots(figsize=(12, 6))

    for name, table in list(shares_per_ticker.items()):
        ax.plot(table.index, table["shares_sum"], label=name)

    ax.set_xlabel("Date")
    ax.set_ylabel("Cumulative Shares")
    ax.set_title("Cumulative Shares of All Tickers Over Time")
    ax.grid(True)
    ax.tick_params(axis="x", rotation=45)
    ax.set_ylim(bottom=0, top=15)
    # ax.set_xlim(table.index.min(), table.index.max())
    ax.legend()  # Add a legend to distinguish the tickers
    plt.tight_layout()
    plt.gca()
    return ax, name, table


@app.cell(hide_code=True)
def _():
    mo.md("""## Yahoo Finance Data Retrieval""")
    return


@app.cell
def _(still_open):
    yahoo_data = {}
    for _details in still_open["Details"].unique():
        try:
            # Find the first open date for the ticker
            first_open_date = still_open[
                still_open["Details"] == _details
            ].index.min()

            [ticker, market] = _details.split("/")
            if market != "USD":
                log.warning("SKIPPING {ticker} because market={market} != \"USD\"")
                continue
            ticker_data = yf.Ticker(ticker)
            # Fetch historical data since the company's IPO or listing date
            history = ticker_data.history(
                start=first_open_date.strftime("%Y-%m-%d"),
                end=pd.Timestamp.now().strftime("%Y-%m-%d"),
            )
            if not history.empty:
                yahoo_data[_details] = history
            else:
                print(f"No data found for {ticker}")
        except Exception as e:
            print(f"Could not fetch data for {ticker}: {e}")
        print(ticker, "OK!")
    return (yahoo_data,)


@app.cell(hide_code=True)
def _():
    mo.md(
        """
    ## Combine yahoo data with etoro data

    *(this is where it starts to get weird)*
    """
    )
    return


@app.cell
def _(shares_per_ticker, yahoo_data):
    all_combined_data = {}

    for _ticker in shares_per_ticker:
        if _ticker in shares_per_ticker and _ticker in yahoo_data:
            _shares_data = shares_per_ticker[_ticker]
            _yahoo_data = yahoo_data[_ticker]

            # Ensure both DataFrames have a datetime index and are timezone-naive
            _shares_data.index = pd.to_datetime(_shares_data.index).tz_localize(
                None
            )
            _yahoo_data.index = pd.to_datetime(_yahoo_data.index).tz_localize(None)

            # Join the DataFrames on their indices using a left join
            combined = _shares_data.join(_yahoo_data, how="left")

            # Calculate net value and add it to the combined DataFrame
            combined["net_value"] = combined["Close"] * combined["shares_sum"]

            all_combined_data[_ticker] = combined
        else:
            print(f"Data not available for {_ticker} in both datasets.")
    return (all_combined_data,)


@app.cell(hide_code=True)
def _():
    mo.md(
        r"""
    # **WTF** 🤯
    $12.5k de Rolls-Royce sur la dernière page...

    -> C'est parceque **RRL.l** est en fait **RRL.l/GBX** sur etoro donc les "Units/Contracts" sont peut être pas equivalents
    """
    )
    return


@app.cell
def _(all_combined_data):
    all_combined_data["GOOG/USD"]
    return


@app.cell
def _(all_combined_data):
    all_combined_data_filled = {}
    for _stock, _df in all_combined_data.items():
        all_combined_data_filled[_stock] = _df.ffill()
    return (all_combined_data_filled,)


@app.cell(hide_code=True)
def _():
    mo.md(
        r"""
    ## Test ici le poids le **RR.l**

    Les quelques premieres valeurs ont du sens, **GOOG** est bien premier avec 2x plus que **AMZN** etc...

    *Mais si on ajoute **RR.L** ☠️
    """
    )
    return


@app.cell
def _(all_combined_data_filled, ax, name, table):
    for stock in list(all_combined_data_filled)[:5]:
        # for stock in list(all_combined_data_filled)[:5] + ["RR.l"]:
        all_combined_data_filled[stock]["net_value"].plot(
            title=f"{stock} Net Value Over Time", label=stock
        )
        ax.plot(table.index, table["shares_sum"], label=name)

    plt.xlabel("Date")
    plt.ylabel("Net Value")
    plt.legend()
    plt.gca()
    return


@app.cell
def _(closed):
    closed.rename(columns={"Cumulative Profit":"net_value"})
    # closed.reindex(closed["Close Date"]).rename({"Cumulative Profit":"net_value"})
    # print(cumulative_deposits)
    return


@app.cell(hide_code=True)
def _():
    mo.md(r"""# Total net-value""")
    return


@app.cell
def _(all_combined_data_filled, closed):
    _all_data = pd.DataFrame()

    all_profits = dict(all_combined_data_filled)

    all_profits["Closed Positions"] = closed.rename(columns={"Cumulative Profit":"net_value"})
    # all_profits["Deposits"] = pd.DataFrame({"net_value": cumulative_deposits})
    print(all_profits["Closed Positions"])
    for _stock, _df in all_profits.items():
        _all_data = _all_data.join(
            _df[["net_value"]].rename(columns={"net_value": _stock}), how="outer"
        )

    _all_data = _all_data.ffill()
    _all_data["total"] = _all_data.sum(axis=1)

    _fig, _ax = plt.subplots(figsize=(16, 12))  # Double the default size

    _all_data["Closed Positions"].plot(
        title='Total net value of portfolio over time',
        xlabel="Date",
        ylabel="Total Net Value",
        label="Closed Positions",
        ax=_ax
    )
    _all_data["total"].plot(ax=_ax, label="Total")

    for col in _all_data.columns:
        if col not in ["Closed Positions", "total"]:
            _all_data[col].plot(ax=_ax, label=col)

    _ax.legend(loc='best')  # Let matplotlib decide the best location
    plt.gca()
    print(_all_data)

    all_data = _all_data
    return (all_data,)


@app.cell
def _(all_data):
    res = models.EtoroEvolutionInner(dates=all_data.index.astype(str).to_list(), parts=all_data.reset_index().drop(columns=['index']).to_dict('list'))
    return (res,)


@app.cell
def _(res):
    res
    return


if __name__ == "__main__":
    app.run()
