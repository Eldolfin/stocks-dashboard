# ruff: noqa: ANN001, FBT003, ERA001

import marimo as mo
import matplotlib.pyplot as plt
import pandas as pd

import src.etoro_data as etoro

app = mo.App()


@app.cell
def _():
    return etoro, pd, plt


@app.cell
def _(pd):
    excel = pd.read_excel("~/Downloads/etoro-account-statement-12-31-2014-7-5-2025.xlsx", sheet_name=None)
    return (excel,)


@app.cell
def _() -> None:
    # cumulative_profit = closed["Profit(USD)"].cumsum()

    # plt.plot(cumulative_profit)
    # plt.xlabel("Trade Number")
    # plt.ylabel("Cumulative Profit")
    # plt.title("Cumulative Profit of Closed Trades")
    # plt.grid(True)
    # plt.gca()
    return


@app.cell
def _(etoro, excel, plt) -> None:
    closed = excel["Closed Positions"]
    # Convert 'Close Date' to datetime objects
    closed["Close Date"] = etoro.column_date_to_timestamp(closed["Close Date"])

    # Calculate daily profit
    daily_profit = closed.groupby(closed["Close Date"].dt.date)["Profit(USD)"].sum()

    # Calculate cumulative profit
    cumulative_profit = daily_profit.cumsum()

    # Plotting
    plt.figure(figsize=(12, 6))
    plt.plot(cumulative_profit.index, cumulative_profit.values, marker="o", linestyle="-")
    plt.xlabel("Date")
    plt.ylabel("Cumulative Profit (USD)")
    plt.title("Cumulative Profit of Closed Trades Over Time")
    plt.grid(True)
    plt.xticks(rotation=45)  # Rotate x-axis labels for better readability
    plt.tight_layout()  # Adjust layout to prevent labels from overlapping
    plt.show()


@app.cell
def _(excel, pd, plt) -> None:
    activity = excel["Account Activity"]
    # Ensure 'Date' is datetime objects
    activity["Date"] = pd.to_datetime(activity["Date"])

    # Filter for 'Deposit' operations
    deposits = activity[deposits["Type"] == "Deposit"]

    # Group by date and sum the amounts
    daily_deposits = deposits.groupby(deposits["Date"].dt.date)["Amount"].sum()

    # Calculate cumulative deposits
    cumulative_deposits = daily_deposits.cumsum()

    # Plotting
    plt.figure(figsize=(12, 6))
    plt.plot(cumulative_deposits.index, cumulative_deposits.values, marker="o", linestyle="-", color="green")
    plt.xlabel("Date")
    plt.ylabel("Cumulative Deposits (USD)")
    plt.title("Cumulative Deposits Over Time (Daily)")
    plt.grid(True)
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()
