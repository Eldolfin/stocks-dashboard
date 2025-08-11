"""Test the new async eToro endpoints with progress tracking."""

import time
from pathlib import Path
from unittest.mock import Mock, patch

import pytest
from flask import Flask

from src import models
from src.services import stocks_service
from src.services.task_manager import task_manager


@pytest.fixture
def fake_app():
    """Return a minimal Flask app with fake config."""
    app = Flask(__name__)
    app.config["UPLOAD_FOLDER"] = "/tmp"
    return app


def test_async_etoro_analysis_file_not_found(fake_app):
    query = models.EtoroAnalysisByNameQuery(filename="nonexistent.xlsx", precision="M")

    with fake_app.app_context():
        with pytest.raises(FileNotFoundError):
            stocks_service.analyze_etoro_excel_by_name_async(query, "test@example.com")


def test_async_etoro_evolution_file_not_found(fake_app):
    query = models.EtoroAnalysisByNameQuery(filename="nonexistent.xlsx", precision="M")

    with fake_app.app_context():
        with pytest.raises(FileNotFoundError):
            stocks_service.analyze_etoro_evolution_by_name_async(query, "test@example.com")


@patch("src.services.stocks_service.Path")
@patch("src.services.stocks_service.extract_closed_position")
def test_async_etoro_analysis_success(mock_extract, mock_path, fake_app):
    mock_path.exists.return_value = True
    mock_extract.return_value = {"test": ["data"]}

    query = models.EtoroAnalysisByNameQuery(filename="test.xlsx", precision="M")

    with fake_app.app_context():
        task_id = stocks_service.analyze_etoro_excel_by_name_async(query, "test@example.com")

    assert task_id is not None
    task = task_manager.get_task(task_id)
    assert task is not None

    time.sleep(0.1)

    mock_extract.assert_called_once()
    args, kwargs = mock_extract.call_args
    assert "progress_callback" in kwargs
    assert callable(kwargs["progress_callback"])


@patch("src.services.stocks_service.Path")
@patch("src.services.stocks_service.extract_portfolio_evolution")
def test_async_etoro_evolution_success(mock_extract, mock_path, fake_app):
    mock_path.exists.return_value = True
    mock_evolution = models.EtoroEvolutionInner(dates=["2023-01-01"], parts={"test": [1.0]})
    mock_extract.return_value = mock_evolution

    query = models.EtoroAnalysisByNameQuery(filename="test.xlsx", precision="M")

    with fake_app.app_context():
        task_id = stocks_service.analyze_etoro_evolution_by_name_async(query, "test@example.com")

    assert task_id is not None
    task = task_manager.get_task(task_id)
    assert task is not None

    time.sleep(0.1)

    mock_extract.assert_called_once()
    args, kwargs = mock_extract.call_args
    assert "progress_callback" in kwargs
    assert callable(kwargs["progress_callback"])


def test_progress_callback_functionality():
    from src.services.etoro_data import extract_closed_position

    task_id = task_manager.create_task()

    def mock_progress_callback(step_name: str, step_number: int, step_count: int):
        task_manager.update_progress(task_id, step_name, step_number, step_count)

    mock_progress_callback("Test step", 2, 4)

    task = task_manager.get_task(task_id)
    assert task is not None
    assert task.progress is not None
    assert task.progress.step_name == "Test step"
    assert task.progress.step_number == 2
    assert task.progress.step_count == 4
