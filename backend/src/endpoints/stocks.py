# ruff: noqa: ANN201

from flask_caching import Cache
from flask_login import current_user, login_required
from flask_openapi3 import APIBlueprint, Tag

from src import models
from src.services import stocks_service
from src.services.task_manager import task_manager

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


@stocks_bp.post("/etoro/upload_report", tags=[stocks_tag])
@login_required
def upload_etoro_report(form: models.EtoroForm) -> tuple[dict, int]:
    if isinstance(form.file, str) or form.file.filename is None:
        return {"error": "Invalid file"}, 400
    stocks_service.create_etoro_excel(form, current_user.email)
    return {"result": "OK"}, 200


@stocks_bp.get("/etoro/reports", tags=[stocks_tag], responses={200: models.EtoroReportsResponse})
@login_required
def list_etoro_reports():
    result = stocks_service.list_etoro_reports(current_user.email)
    return result.dict(), 200


@stocks_bp.get(
    "/etoro_analysis_by_name",
    tags=[stocks_tag],
    responses={200: models.TaskStartResponse, 404: models.NotFoundResponse},
)
@login_required
def analyze_etoro_excel_by_name(query: models.EtoroAnalysisByNameQuery):
    try:
        task_id = stocks_service.analyze_etoro_excel_by_name_async(query, current_user.email)
        return models.TaskStartResponse(task_id=task_id).dict(), 200
    except FileNotFoundError:
        return models.NotFoundResponse().dict(), 404


@stocks_bp.get(
    "/etoro_evolution_by_name",
    tags=[stocks_tag],
    responses={200: models.TaskStartResponse, 404: models.NotFoundResponse},
)
@login_required
def analyze_etoro_evolution_by_name(query: models.EtoroAnalysisByNameQuery):
    try:
        task_id = stocks_service.analyze_etoro_evolution_by_name_async(query, current_user.email)
        return models.TaskStartResponse(task_id=task_id).dict(), 200
    except FileNotFoundError:
        return models.NotFoundResponse().dict(), 404


@stocks_bp.get(
    "/task_status/<task_id>",
    tags=[stocks_tag],
    responses={200: models.TaskStatusResponse, 404: models.NotFoundResponse},
)
@login_required
def get_task_status(path: models.TaskIdPath):
    task = task_manager.get_task(path.task_id)
    if task is None:
        return models.NotFoundResponse().dict(), 404

    progress = None
    if task.progress:
        progress = models.TaskProgressResponse(
            step_name=task.progress.step_name,
            step_number=task.progress.step_number,
            step_count=task.progress.step_count
        )

    status_response = models.TaskStatusResponse(
        status=task.status.value,
        progress=progress,
        error=task.error
    )
    return status_response.dict(), 200


@stocks_bp.get(
    "/task_result/<task_id>",
    tags=[stocks_tag],
    responses={200: dict, 404: models.NotFoundResponse},
)
@login_required
def get_task_result(path: models.TaskIdPath):
    task = task_manager.get_task(path.task_id)
    if task is None:
        return models.NotFoundResponse().dict(), 404

    if task.status.value != "completed":
        return {"error": "Task not completed"}, 400

    if isinstance(task.result, models.EtoroEvolutionResponse):
        return task.result.dict(), 200
    return task.result, 200
