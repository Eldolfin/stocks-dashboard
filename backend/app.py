from flask_cors import CORS
from flask import Flask, request
import yfinance as yf
from flask_openapi3 import Info, Tag
from flask_openapi3 import OpenAPI
from src import models
from typing import List
from src.models import (
    TickerResponse,
    TickerQuery,
    SearchResponse,
    SearchQuery,
    KPIResponse,
    KPIQuery,
    Quote,
    RawQuote,
    MainKPIs,
    NotFoundResponse,
    CompareGrowthQuery,
    CompareGrowthResponse,
    EtoroForm,
    EtoroAnalysisResponse,
)
from src.intervals import interval_to_duration, duration_to_interval
from datetime import datetime
from pydantic import BaseModel
from flask_openapi3.models import RequestBody
from src.etoro_data import extract_closed_position
import numpy as np

info = Info(title="stocks API", version="1.0.0")
app = OpenAPI(__name__, info=info)
CORS(app, origins=["http://localhost:3000", "http://localhost:5173"])
app.config["UPLOAD_FOLDER"] = "./etoro_sheets"


@app.get(
    "/api/ticker/",
    summary="get a ticker's price history",
    # responses={200: TickerResponse, 404: NotFoundResponse},
)
def get_ticker(query: TickerQuery):
    N_POINTS = 20
    if query.period == "max":
        dat = yf.Ticker(query.ticker_name)
        history = dat.history(period="max", interval="3mo").reset_index()
        duration = datetime.now() - history.iloc[0]["Date"].replace(tzinfo=None)
    else:
        duration = interval_to_duration(query.period)
    if query.interval is None or query.interval == "auto":
        query.interval = duration_to_interval(duration / N_POINTS)

    start = datetime.now() - duration
    start = start.strftime("%Y-%m-%d")
    try:
        dat = yf.Ticker(query.ticker_name)
        if query.period == "max":
            history = dat.history(
                period="max", interval=query.interval
            ).reset_index()
        else:
            history = dat.history(
                start=start, interval=query.interval
            ).reset_index()
    except Exception:
        return NotFoundResponse().dict(), 404

    if "Datetime" in history:
        history["Date"] = history["Datetime"].dt.strftime("%Y-%m-%dT%H:%M:%S")
    else:
        history["Date"] = history["Date"].dt.strftime("%Y-%m-%d")
    if history.empty:
        return NotFoundResponse().dict(), 404

    first_row = history.iloc[0]
    last_row = history.iloc[-1]

    dates = history["Date"].tolist()
    candles = history["Close"].tolist()
    delta = (last_row["Close"] - first_row["Open"]) / first_row["Open"]
    sma30 = (
        history["Close"]
        .rolling(window=30)
        .mean()
        .fillna(history["Close"])
        .tolist()
    )

    return (
        TickerResponse(
            dates=dates, candles=candles, query=query, delta=delta, sma30=sma30
        ).dict(),
        200,
    )


@app.get(
    "/api/compare_growth/",
    summary="compare a list of tickers growth",
    responses={200: CompareGrowthResponse, 404: NotFoundResponse},
)
def get_compare_growth(query: CompareGrowthQuery):
    if len(query.ticker_names) == 1:
        query.ticker_names = query.ticker_names[0].split(",")

    dat = yf.Tickers(query.ticker_names)
    hist = dat.history(period=query.period)

    close_df = hist.xs("Close", level="Price", axis=1)
    base_prices = close_df.iloc[0]
    ratios_df = close_df.divide(base_prices)

    candles = {
        ticker: ratios_df[ticker].tolist() for ticker in query.ticker_names
    }
    dates = [index.strftime("%Y-%m-%d") for index in ratios_df.index]

    return (
        CompareGrowthResponse(query=query, candles=candles, dates=dates).dict(),
        200,
    )


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

    if "marketCap" in dat.info:
        main = MainKPIs(
            ratioPE=dat.info["marketCap"] / dat.info["ebitda"],
            freeCashflowYield=dat.info["freeCashflow"] / dat.info["marketCap"],
        )
    else:
        main = None
    return (
        KPIResponse(
            query=query,
            analyst_price_targets=dat.analyst_price_targets,
            info=dat.info,
            main=main,
        ).dict(),
        200,
    )


@app.get(
    "/api/search/",
    summary="full-text search for ticker's",
    responses={200: SearchResponse},
)
def search_ticker(query: SearchQuery):
    raw_quotes: List[RawQuote] = list(
        map(RawQuote.model_validate, yf.Search(query.query).quotes)
    )
    quotes_names = list(quote.symbol for quote in raw_quotes)
    tickers = yf.Tickers(quotes_names).tickers
    infos: List[models.Info] = [
        models.Info.model_validate(t.info) for t in tickers.values()
    ]
    deltas = [
        (
            ((i.currentPrice - i.open) / i.currentPrice)
            if i.currentPrice and i.open
            else None
        )
        for i in infos
    ]

    quotes = [
        Quote(
            raw=raw,
            info=info,
            icon_url=(
                None
                if info.website is None
                else f"https://logo.clearbit.com/{info.website}"
            ),
            today_change=today_change,
        )
        for (raw, info, today_change) in zip(raw_quotes, infos, deltas)
        if info.currentPrice is not None
    ]
    return SearchResponse(quotes=quotes, query=query).dict(), 200


@app.post(
    "/api/etoro_analysis",
    summary="analyse etoro excel sheet",
    responses={200: EtoroAnalysisResponse},
)
def analyze_etoro_excel(form: EtoroForm):
    read = form.file.read()
    closed_position = extract_closed_position(read, time_unit=form.precision)
    return closed_position


def create_app():
    return app
