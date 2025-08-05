# /// script
# [tool.marimo.runtime]
# auto_instantiate = false
# ///

import marimo

__generated_with = "0.14.16"
app = marimo.App(width="medium")


@app.cell
def _():
    import pandas as pd
    import src.etoro_data as etoro
    import matplotlib.pyplot as plt
    return etoro, pd, plt


@app.cell
def _(pd):
    excel = pd.read_excel(
        "~/Downloads/etoro-account-statement-12-31-2014-7-5-2025.xlsx",
        sheet_name=None,
    )
    return (excel,)


@app.cell
def _():
    # cumulative_profit = closed["Profit(USD)"].cumsum()

    # plt.plot(cumulative_profit)
    # plt.xlabel("Trade Number")
    # plt.ylabel("Cumulative Profit")
    # plt.title("Cumulative Profit of Closed Trades")
    # plt.grid(True)
    # plt.gca()
    return


@app.cell
def _(etoro, excel, plt):
    closed = excel["Closed Positions"]
    # Convert 'Close Date' to datetime objects
    closed["Close Date"] = etoro.column_date_to_timestamp(closed["Close Date"])

    # Sort the DataFrame by 'Close Date'
    closed = closed.sort_values(by="Close Date")

    # Calculate cumulative profit
    cumulative_profit = closed["Profit(USD)"].cumsum()

    # Plotting
    plt.plot(closed["Close Date"], cumulative_profit)
    plt.xlabel("Close Date")
    plt.ylabel("Cumulative Profit (USD)")
    plt.title("Cumulative Profit of Closed Trades Over Time")
    plt.grid(True)
    plt.xticks(rotation=45)  # Rotate x-axis labels for better readability
    plt.tight_layout()  # Adjust layout to prevent labels from overlapping
    plt.gca()
    return


@app.cell
def _(excel, pd, plt):
    activity = excel["Account Activity"]
    # Ensure 'Date' is datetime objects
    activity["Date"] = pd.to_datetime(activity["Date"])

    # Set 'Date' as index for resampling
    activity = activity.set_index("Date")

    # Resample to daily frequency, filling missing values with 0
    daily_deposits = (
        activity[activity["Type"] == "Deposit"]["Amount"]
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


@app.cell
def _(activity):
    activity
    return


@app.cell
def _(activity):
    open_positions = activity[activity["Type"] == "Open Position"]
    closed_positions = activity[activity["Type"] == "Position closed"]

    open_position_ids = open_positions["Position ID"].dropna().astype(str)
    closed_position_ids = closed_positions["Position ID"].dropna().astype(str)

    still_open_ids = open_positions[
        ~open_positions["Position ID"].isin(closed_position_ids)
    ]
    still_open_ids
    return (still_open_ids,)


@app.cell
def _(still_open_ids):
    still_open_ids["Details"] = still_open_ids["Details"].str.replace(
        r"/(.+)$", "", regex=True
    )
    still_open_ids
    return


if __name__ == "__main__":
    app.run()
