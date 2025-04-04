from flask_cors import CORS
from flask import Flask
import yfinance as yf
from flask_openapi3 import Info, Tag
from flask_openapi3 import OpenAPI
from src import models
from src.models import (
    TickerResponse,
    TickerQuery,
    SearchResponse,
    SearchQuery,
    KPIResponse,
    KPIQuery,
    Quote,
    RawQuote,
    NotFoundResponse,
)


info = Info(title="stocks API", version="1.0.0")
app = OpenAPI(__name__, info=info)
CORS(app, origins=["http://localhost:5173"])


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
    "/api/kpis/",
    summary="get a ticker's kpis",
    responses={200: KPIResponse, 404: NotFoundResponse},
)
def get_kpis(query: KPIQuery):
    try:
        dat = yf.Ticker(query.ticker_name)
    except Exception:
        return NotFoundResponse().dict(), 404

    return (
        KPIResponse(
            query=query,
            analyst_price_targets=dat.analyst_price_targets,
            info=dat.info,
        ).dict(),
        200,
    )


@app.get(
    "/api/search/",
    summary="full-text search for ticker's",
    responses={200: SearchResponse},
)
def search_ticker(query: SearchQuery):
    quotes: List[RawQuote] = list(
        map(RawQuote.model_validate, yf.Search(query.query).quotes)
    )
    quotes_names = list(quote.symbol for quote in quotes)
    tickers = yf.Tickers(quotes_names).tickers
    infos: List[models.Info] = [
        models.Info.model_validate(t.info) for t in tickers.values()
    ]

    quotes = [
        Quote(
            raw=raw,
            info=info,
            icon_url=f"https://logo.clearbit.com/{info.website}",
        )
        for (raw, info) in zip(quotes, infos)
    ]

    return SearchResponse(quotes=quotes, query=query).dict(), 200
