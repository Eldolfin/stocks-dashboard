from flask import Flask
import yfinance as yf
from flask_openapi3 import Info, Tag
from flask_openapi3 import OpenAPI
from pydantic import BaseModel, Field
from typing import List


info = Info(title="book API", version="1.0.0")
app = OpenAPI(__name__, info=info)


class TickerQuery(BaseModel):
    ticker_name: str
    period: str = "1mo"  # FIXME: this is not specific enough


class TickerCandle(BaseModel):
    Close: float
    Date: str
    Dividends: int
    High: float
    Low: float
    Open: float
    Stock_Splits: int = Field(..., alias="Stock Splits")
    Volume: int


class TickerResponse(BaseModel):
    candles: List[TickerCandle]
    query: TickerQuery


class NotFoundResponse(BaseModel):
    code: int = Field(-1, description="Status Code")
    message: str = Field(
        "Resource not found!", description="Exception Information"
    )


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


class SearchQuery(BaseModel):
    query: str


@app.get("/api/search/<query>", summary="full-text search for ticker's")
def search_ticker(query: SearchQuery):
    return yf.Search(query.query).all
