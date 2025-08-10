import marimo

__generated_with = "0.14.16"
app = marimo.App(width="full")


@app.cell
def _():
    import pandas as pd
    import yfinance as yf

    return pd, yf


@app.cell
def _(pd, yf):
    static_indexes = pd.read_csv("data/search/top_cryptos.csv")
    for index_index, index_row in static_indexes.iterrows():
        yahoo_ticker = yf.Ticker(f"{index_row['Ticker']}-USD")
        print(index_row["Ticker"], yahoo_ticker.fast_info.currency)
    return


@app.cell
def _(yf):
    res = yf.Search("Apple")

    return


@app.cell
def _(yf):
    yf.Tickers(["AAPL"]).tickers["AAPL"].fast_info.market_cap
    return


if __name__ == "__main__":
    app.run()
