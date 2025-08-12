from pathlib import Path

from flask import current_app
from flask_login import current_user
from flask_openapi3 import APIBlueprint, Tag

from src.models import BadRequestResponse, CompareToIndexQuery, CompareToIndexResponse, NotFoundResponse
from src.services.compare_to_index_service import CompareToIndexService

compare_bp = APIBlueprint(
    "compare",
    __name__,
    url_prefix="/api/etoro",
    abp_tags=[Tag(name="Compare", description="Portfolio vs Index comparison endpoints")],
)


@compare_bp.post(
    "/compare_to_index",
    summary="Compare eToro portfolio to index",
    responses={
        200: CompareToIndexResponse,
        400: BadRequestResponse,
        404: NotFoundResponse,
    },
)
def compare_to_index(query: CompareToIndexQuery) -> CompareToIndexResponse:
    """
    Compare eToro portfolio performance to a selected index.
    """
    filename = query.filename
    index_ticker = query.index_ticker
    if not filename or not index_ticker:
        error_message = "Missing filename or index_ticker"
        raise ValueError(error_message)

    user_email = current_user.email
    upload_folder = Path(current_app.config["UPLOAD_FOLDER"]) / user_email
    file_path = upload_folder / filename
    if not file_path.exists():
        error_message = "File not found"
        raise FileNotFoundError(error_message)

    try:
        dates, deposits = CompareToIndexService.extract_etoro_data(file_path)
        index_prices = CompareToIndexService.get_index_prices(index_ticker, dates)
        index_values = CompareToIndexService.simulate_index_investment(dates, deposits, index_prices)
    except Exception as e:
        error_message = f"Processing error: {e!s}"
        raise ValueError(error_message) from e

    return CompareToIndexResponse(dates=dates, index_values=index_values).dict()
