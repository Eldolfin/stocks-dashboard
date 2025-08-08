from pathlib import Path

import pandas as pd
from flask import current_app
from werkzeug.utils import secure_filename

from src import models
from src.database import bloomberg_repository, stocks_repository

from .etoro_data import extract_closed_position, extract_portfolio_evolution
from .intervals import duration_to_interval, interval_to_duration, now


def get_ticker(query: models.TickerQuery) -> models.TickerResponse | None:
    n_points = 20
    history: pd.DataFrame
    if query.period == "max":
        dat = stocks_repository.get_ticker_history(query.ticker_name, "max", "3mo")
        history = pd.DataFrame(dat)
        duration = now() - history.iloc[0]["Date"].replace(tzinfo=None)
    else:
        duration = interval_to_duration(query.period)
    if query.interval is None or query.interval == "auto":
        query.interval = duration_to_interval(duration / n_points)

    start = now() - duration
    start = start.strftime("%Y-%m-%d")
    if query.period == "max":
        history = pd.DataFrame(stocks_repository.get_ticker_history(query.ticker_name, "max", query.interval))
    else:
        history = pd.DataFrame(
            stocks_repository.get_ticker_history_from_start(query.ticker_name, start, query.interval)
        )
    if history.empty:
        return None

    if "Datetime" in history:
        history["Date"] = history["Datetime"].dt.strftime("%Y-%m-%dT%H:%M:%S")
    else:
        history["Date"] = history["Date"].dt.strftime("%Y-%m-%d")
    if history.empty:
        return None

    first_row = history.iloc[0]
    last_row = history.iloc[-1]

    dates = history["Date"].tolist()
    candles = history["Close"].tolist()
    delta = (last_row["Close"] - first_row["Open"]) / first_row["Open"]
    smas_history = stocks_repository.get_ticker_history(query.ticker_name, "max", "1d")
    smas_sizes = [30, 100, 500]
    smas = {
        size: (smas_history["Close"].rolling(window=size).mean().fillna(0).tolist()[-len(candles) :])
        for size in smas_sizes
    }

    return models.TickerResponse(
        dates=dates,
        candles=candles,
        query=query,
        delta=delta,
        smas=smas,
    )


def get_compare_growth(query: models.CompareGrowthQuery) -> models.CompareGrowthResponse:
    if len(query.ticker_names) == 1:
        query.ticker_names = query.ticker_names[0].split(",")

    hist = stocks_repository.get_tickers_history(query.ticker_names, query.period)

    close_df = hist.xs("Close", level="Price", axis=1)
    base_prices = close_df.iloc[0]
    ratios_df = close_df.divide(base_prices)

    candles = {ticker: ratios_df.loc[:, ticker].tolist() for ticker in query.ticker_names}
    dates = [index.strftime("%Y-%m-%d") for index in ratios_df.index]

    return models.CompareGrowthResponse(query=query, candles=candles, dates=dates)


def get_kpis(query: models.KPIQuery) -> models.KPIResponse | None:
    info = stocks_repository.get_ticker_info(query.ticker_name)
    if not info or info.get("marketCap") is None:
        return None

    if "marketCap" in info:
        ratio_pe = None
        free_cashflow_yield = None
        if "editda" in info:
            ratio_pe = info["marketCap"] / info["ebitda"]
        if "freeCashflow" in info:
            free_cashflow_yield = info["freeCashflow"] / info["marketCap"]
        main = models.MainKPIs(
            ratioPE=ratio_pe,
            freeCashflowYield=free_cashflow_yield,
        )
    else:
        main = None

    analyst_price_targets = stocks_repository.get_ticker_analyst_price_targets(query.ticker_name)

    return models.KPIResponse(
        query=query,
        analyst_price_targets=analyst_price_targets,
        info=info,
        main=main,
    )


def get_historical_kpis(query: models.KPIQuery) -> models.HistoricalKPIs | None:
    return bloomberg_repository.load_historical_kpis(query.ticker_name)


def search_ticker(query: models.SearchQuery) -> models.SearchResponse:
    raw_quotes: list[models.RawQuote] = list(
        map(models.RawQuote.model_validate, stocks_repository.search(query.query)),
    )
    quotes_names = [quote.symbol for quote in raw_quotes]
    tickers = stocks_repository.get_tickers(quotes_names)
    infos: list[models.Info] = [models.Info.model_validate(t.info) for t in tickers.values()]
    deltas = [(((i.currentPrice - i.open) / i.currentPrice) if i.currentPrice and i.open else None) for i in infos]

    quotes = [
        models.Quote(
            raw=raw,
            info=info,
            icon_url=(None if info.website is None else f"https://logo.clearbit.com/{info.website}"),
            today_change=today_change,
        )
        for (raw, info, today_change) in zip(raw_quotes, infos, deltas, strict=True)
        if info.currentPrice is not None
    ]
    return models.SearchResponse(quotes=quotes, query=query)


def create_etoro_excel(form: models.EtoroForm, user_email: str) -> None:
    etoro_upload_folder = Path(current_app.config["UPLOAD_FOLDER"]) / user_email
    etoro_upload_folder.mkdir(exist_ok=True, parents=True)
    assert form.file.filename is not None
    filename = secure_filename(form.file.filename)
    file_path = Path(etoro_upload_folder) / filename
    form.file.save(str(file_path))


def list_etoro_reports(user_email: str) -> models.EtoroReportsResponse:
    user_etoro_folder = Path(current_app.config["UPLOAD_FOLDER"]) / user_email
    if not Path.exists(user_etoro_folder):
        return models.EtoroReportsResponse(reports=[])

    reports = [f.name for f in user_etoro_folder.iterdir() if (Path(user_etoro_folder) / f).exists()]
    return models.EtoroReportsResponse(reports=reports)


def analyze_etoro_excel_by_name(query: models.EtoroAnalysisByNameQuery, user_email: str) -> dict | None:
    user_etoro_folder = Path(current_app.config["UPLOAD_FOLDER"]) / user_email
    file_path = Path(user_etoro_folder) / query.filename

    if not Path.exists(file_path):
        return None

    return extract_closed_position(file_path, time_unit=query.precision)


def analyze_etoro_evolution_by_name(
    query: models.EtoroAnalysisByNameQuery, user_email: str
) -> models.EtoroEvolutionResponse | None:
    user_etoro_folder = Path(current_app.config["UPLOAD_FOLDER"]) / user_email
    file_path = Path(user_etoro_folder) / query.filename

    if not Path.exists(file_path):
        return None

    return models.EtoroEvolutionResponse(evolution=extract_portfolio_evolution(file_path))
