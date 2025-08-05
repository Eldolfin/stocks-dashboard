# ruff: noqa: ANN201

from flask_caching import Cache  # type: ignore
from flask_openapi3 import APIBlueprint, Tag  # type: ignore

from src import models
from src.services import stocks_service

stocks_bp = APIBlueprint("stocks", __name__, url_prefix="/api")
cache = Cache()

stocks_tag = Tag(name="stocks", description="Stocks data endpoints")


@stocks_bp.get("/ticker/", tags=[stocks_tag], responses={200: models.TickerResponse, 404: models.NotFoundResponse})
def get_ticker(query: models.TickerQuery):
    result = stocks_service.get_ticker(query)
    if result is None:
        return models.NotFoundResponse().dict(), 404
    return result.dict(), 200


@stocks_bp.get("/compare_growth/", tags=[stocks_tag], responses={200: models.CompareGrowthResponse})
def get_compare_growth(query: models.CompareGrowthQuery):
    result = stocks_service.get_compare_growth(query)
    return result.dict(), 200


@stocks_bp.get("/kpis/", tags=[stocks_tag], responses={200: models.KPIResponse, 404: models.NotFoundResponse})
def get_kpis(query: models.KPIQuery):
    result = stocks_service.get_kpis(query)
    if result is None:
        return models.NotFoundResponse().dict(), 404
    return result.dict(), 200


@stocks_bp.get("/search/", tags=[stocks_tag], responses={200: models.SearchResponse})
@cache.memoize()
def search_ticker(query: models.SearchQuery):
    result = stocks_service.search_ticker(query)
    return result.dict(), 200


@stocks_bp.post("/etoro_analysis", tags=[stocks_tag], responses={200: models.EtoroAnalysisResponse})
@login_required
def analyze_etoro_excel(form: models.EtoroForm):
    result = stocks_service.analyze_etoro_excel(form, current_user.email)
    if result is None:
        return {"error": "No selected file"}, 400
    return result, 200


@stocks_bp.get("/etoro/reports", tags=[stocks_tag], responses={200: models.EtoroReportsResponse})
@login_required
def list_etoro_reports():
    result = stocks_service.list_etoro_reports(current_user.email)
    return result.dict(), 200


@stocks_bp.get(
    "/etoro_analysis_by_name",
    tags=[stocks_tag],
    responses={200: models.EtoroAnalysisResponse, 404: models.NotFoundResponse},
)
@login_required
def analyze_etoro_excel_by_name(query: models.EtoroAnalysisByNameQuery):
    result = stocks_service.analyze_etoro_excel_by_name(query, current_user.email)
    if result is None:
        return models.NotFoundResponse().dict(), 404
    return result, 200
