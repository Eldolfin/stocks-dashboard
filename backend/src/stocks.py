# ruff: noqa: ANN201,BLE001

from pathlib import Path

import yfinance as yf
from flask import current_app
from flask_caching import Cache
from flask_login import current_user, login_required
from flask_openapi3 import APIBlueprint, Tag
from werkzeug.utils import secure_filename

from etoro_data import extract_closed_position
from intervals import duration_to_interval, interval_to_duration, now
from models import (
    CompareGrowthQuery,
    CompareGrowthResponse,
    EtoroForm,
    EtoroReportsResponse,
    Info,
    KPIQuery,
    KPIResponse,
    MainKPIs,
    NotFoundResponse,
    Quote,
    RawQuote,
    SearchQuery,
    SearchResponse,
    TickerQuery,
    TickerResponse,
)

from . import models

stocks_bp = APIBlueprint("stocks", __name__, url_prefix="/api")
cache = Cache()

stocks_tag = Tag(name="stocks", description="Stocks data endpoints")


@stocks_bp.get("/ticker/", tags=[stocks_tag], responses={200: models.TickerResponse, 404: models.NotFoundResponse})
@login_required
def get_ticker(query: TickerQuery):
    n_points = 20
    if query.period == "max":
        dat = yf.Ticker(query.ticker_name)
        history = dat.history(period="max", interval="3mo").reset_index()
        duration = now() - history.iloc[0]["Date"].replace(tzinfo=None)
    else:
        duration = interval_to_duration(query.period)
    if query.interval is None or query.interval == "auto":
        query.interval = duration_to_interval(duration / n_points)

    start = now() - duration
    start = start.strftime("%Y-%m-%d")
    try:
        dat = yf.Ticker(query.ticker_name)
        if query.period == "max":
            history = dat.history(
                period="max",
                interval=query.interval,
            ).reset_index()
        else:
            history = dat.history(
                start=start,
                interval=query.interval,
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
    smas_history = dat.history(period="max", interval="1d").reset_index()
    smas_sizes = [30, 100, 500]
    smas = {
        size: (smas_history["Close"].rolling(window=size).mean().fillna(0).tolist()[-len(candles) :])
        for size in smas_sizes
    }

    return (
        TickerResponse(
            dates=dates,
            candles=candles,
            query=query,
            delta=delta,
            smas=smas,
        ).dict(),
        200,
    )


@stocks_bp.get("/compare_growth/", tags=[stocks_tag], responses={200: models.CompareGrowthResponse})
@login_required
def get_compare_growth(query: CompareGrowthQuery):
    if len(query.ticker_names) == 1:
        query.ticker_names = query.ticker_names[0].split(",")

    dat = yf.Tickers(query.ticker_names)
    hist = dat.history(period=query.period)

    close_df = hist.xs("Close", level="Price", axis=1)
    base_prices = close_df.iloc[0]
    ratios_df = close_df.divide(base_prices)

    candles = {ticker: ratios_df[ticker].tolist() for ticker in query.ticker_names}
    dates = [index.strftime("%Y-%m-%d") for index in ratios_df.index]

    return (
        CompareGrowthResponse(query=query, candles=candles, dates=dates).dict(),
        200,
    )


@stocks_bp.get("/kpis/", tags=[stocks_tag], responses={200: KPIResponse, 404: NotFoundResponse})
@login_required
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
        ),
        200,
    )


@stocks_bp.get("/search/", tags=[stocks_tag], responses={200: SearchResponse})
@login_required
@cache.memoize()
def search_ticker(query: SearchQuery):
    raw_quotes: list[RawQuote] = list(
        map(RawQuote.model_validate, yf.Search(query.query).quotes),
    )
    quotes_names = [quote.symbol for quote in raw_quotes]
    tickers = yf.Tickers(quotes_names).tickers
    infos: list[Info] = [Info.model_validate(t.info) for t in tickers.values()]
    deltas = [(((i.currentPrice - i.open) / i.currentPrice) if i.currentPrice and i.open else None) for i in infos]

    quotes = [
        Quote(
            raw=raw,
            info=info,
            icon_url=(None if info.website is None else f"https://logo.clearbit.com/{info.website}"),
            today_change=today_change,
        )
        for (raw, info, today_change) in zip(raw_quotes, infos, deltas)
        if info.currentPrice is not None
    ]
    return SearchResponse(quotes=quotes, query=query).dict(), 200


@stocks_bp.post("/etoro_analysis", tags=[stocks_tag], responses={200: models.EtoroAnalysisResponse})
@login_required
def analyze_etoro_excel(form: EtoroForm):
    etoro_upload_folder = Path(current_app.config["UPLOAD_FOLDER"]) / current_user.email
    etoro_upload_folder.makedirs(exist_ok=True)
    filename = secure_filename(form.file.filename)
    file_path = Path(etoro_upload_folder) / filename
    form.file.save(file_path)

    return extract_closed_position(file_path, time_unit=form.precision)


@stocks_bp.get("/etoro/reports", tags=[stocks_tag], responses={200: models.EtoroReportsResponse})
@login_required
def list_etoro_reports():
    user_etoro_folder = Path(current_app.config["UPLOAD_FOLDER"]) / current_user.email
    if not Path.exists(user_etoro_folder):
        return EtoroReportsResponse(reports=[]).dict(), 200

    reports = [f for f in user_etoro_folder.iterdir() if (Path(user_etoro_folder) / f).exists()]
    return EtoroReportsResponse(reports=reports).dict(), 200


@stocks_bp.get(
    "/etoro_analysis_by_name",
    tags=[stocks_tag],
    responses={200: models.EtoroAnalysisResponse, 404: models.NotFoundResponse},
)
@login_required
def analyze_etoro_excel_by_name(query: models.EtoroAnalysisByNameQuery):
    user_etoro_folder = Path(current_app.config["UPLOAD_FOLDER"]) / current_user.email
    file_path = Path(user_etoro_folder) / query.filename

    if not Path.exists(file_path):
        return NotFoundResponse().dict(), 404

    return extract_closed_position(file_path, time_unit=query.precision)
