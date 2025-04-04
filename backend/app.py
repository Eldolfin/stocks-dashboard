from flask import Flask
import yfinance as yf
from flask_openapi3 import Info, Tag
from flask_openapi3 import OpenAPI
from src.models import TickerResponse, TickerQuery, SearchResponse, SearchQuery


info = Info(title="book API", version="1.0.0")
app = OpenAPI(__name__, info=info)


@app.get(
    "/api/ticker/",
    summary="get a ticker's price history",
    responses={200: TickerResponse, 404: NotFoundResponse},
)
def get_ticker(query: TickerQuery):
    try:
        dat = yf.Ticker(query.ticker_name)
        history = dat.history(period=query.period).reset_index()

        # Convert the Date field to string
        history["Date"] = history["Date"].dt.strftime("%Y-%m-%d")

        data = history.to_dict(orient="records")
    except Exception:
        return NotFoundResponse().dict(), 404
    return TickerResponse(candles=data, query=query).dict(), 200


@app.get(
    "/api/search/",
    summary="full-text search for ticker's",
    responses={200: SearchResponse},
)
def search_ticker(query: SearchQuery):
    return yf.Search(query.query).all, 200
