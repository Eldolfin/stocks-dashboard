import marimo

__generated_with = "0.14.16"
app = marimo.App(width="full")


@app.cell
def _():
    import pandas as pd
    import yfinance as yf
    from src.models import SearchQuery
    from src import models

    return SearchQuery, models, pd


@app.cell
def _(pd):
    STATIC_CRYPTO = pd.read_csv("data/search/top_cryptos.csv")
    STATIC_INDEX = pd.read_csv("data/search/top_indexes.csv")

    return STATIC_CRYPTO, STATIC_INDEX


@app.cell
def _(STATIC_CRYPTO, STATIC_INDEX, SearchQuery, models):
    query = SearchQuery(query="us")

    cryptos_filtered = STATIC_CRYPTO[
        STATIC_CRYPTO.apply(lambda row: row.astype(str).str.contains(query.query, case=False, na=False)).any(axis=1)
    ]
    index_filtered = STATIC_INDEX[
        STATIC_INDEX.apply(lambda row: row.astype(str).str.contains(query.query, case=False, na=False)).any(axis=1)
    ]

    quotes_cryptos = [
        models.Quote(
            symbol=row["Ticker"],
            long_name=row["Name"],
            icon_url=(f"https://financialmodelingprep.com/image-stock/{row['Ticker'].removesuffix('-USD')}.png"),
            today_change=None,
        )
        for (_, row) in cryptos_filtered.iterrows()
    ]
    quotes_indexes = [
        models.Quote(
            symbol=row["Ticker"],
            long_name=row["Name"],
            icon_url=f"https://flagcdn.com/160x120/{row['CountryCode']}.png",
            today_change=None,
        )
        for (_, row) in index_filtered.iterrows()
    ]
    quotes_cryptos + quotes_indexes
    return


if __name__ == "__main__":
    app.run()
