import marimo

__generated_with = "0.14.17"
app = marimo.App(width="full")


@app.cell
def _():
    from pathlib import Path

    import numpy as np
    import pandas as pd
    import yfinance as yf
    import matplotlib.pyplot as plt

    # from src import models
    from src.services.etoro_data import (
        column_date_to_timestamp,
        extract_portfolio_evolution,
        _map_etoro_ticker_to_yahoo,
    )

    return extract_portfolio_evolution, plt, yf


@app.cell
def _():
    _map_etoro_ticker_to_yahoo("MHFI/USD", False)
    return


@app.cell
def _(extract_portfolio_evolution):
    def progress_callback(progress):
        pass

    evolution = extract_portfolio_evolution(
        "~/Downloads/etoro-account-statement-12-31-2014-8-7-2025.xlsx", progress_callback
    )
    return (evolution,)


@app.cell
def _(evolution):
    evolution["SNOW/USD"]
    return


@app.cell
def _(evolution, period, yf):
    hist = yf.Tickers(evolution).history(period=period)
    return (hist,)


@app.cell
def _(hist):
    hist[["Close"]].columns
    return


@app.cell
def _(evolution, plt):
    plt.figure(figsize=(19.2, 10.8))
    plt.plot(evolution, label=evolution.columns)
    plt.xlabel("Time", fontsize=12)
    plt.ylabel("Value", fontsize=12)
    plt.title("Portfolio evolution breakdown", fontsize=14)
    plt.legend(fontsize=10)
    plt.gca()
    return


if __name__ == "__main__":
    app.run()
