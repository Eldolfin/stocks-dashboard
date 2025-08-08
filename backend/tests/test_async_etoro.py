"""Test the new async eToro endpoints with progress tracking."""
import time
from unittest.mock import Mock, patch

import pytest

from src import models
from src.services import stocks_service
from src.services.task_manager import task_manager


def test_async_etoro_analysis_file_not_found():
    """Test async analysis with non-existent file."""
    query = models.EtoroAnalysisByNameQuery(filename="nonexistent.xlsx", precision="m")
    
    with pytest.raises(FileNotFoundError):
        stocks_service.analyze_etoro_excel_by_name_async(query, "test@example.com")


def test_async_etoro_evolution_file_not_found():
    """Test async evolution with non-existent file."""
    query = models.EtoroAnalysisByNameQuery(filename="nonexistent.xlsx", precision="m")
    
    with pytest.raises(FileNotFoundError):
        stocks_service.analyze_etoro_evolution_by_name_async(query, "test@example.com")


@patch("src.services.stocks_service.current_app")
@patch("src.services.stocks_service.Path")
@patch("src.services.stocks_service.extract_closed_position")
def test_async_etoro_analysis_success(mock_extract, mock_path, mock_app):
    """Test successful async analysis."""
    # Setup mocks
    mock_app.config = {"UPLOAD_FOLDER": "/tmp"}
    mock_path.exists.return_value = True
    mock_extract.return_value = {"test": ["data"]}
    
    query = models.EtoroAnalysisByNameQuery(filename="test.xlsx", precision="m")
    
    # Call async function
    task_id = stocks_service.analyze_etoro_excel_by_name_async(query, "test@example.com")
    
    # Verify task was created
    assert task_id is not None
    task = task_manager.get_task(task_id)
    assert task is not None
    
    # Wait for completion
    time.sleep(0.1)
    
    # Verify the function was called with progress callback
    mock_extract.assert_called_once()
    args, kwargs = mock_extract.call_args
    assert "progress_callback" in kwargs
    assert callable(kwargs["progress_callback"])


@patch("src.services.stocks_service.current_app")
@patch("src.services.stocks_service.Path")
@patch("src.services.stocks_service.extract_portfolio_evolution")
def test_async_etoro_evolution_success(mock_extract, mock_path, mock_app):
    """Test successful async evolution."""
    # Setup mocks
    mock_app.config = {"UPLOAD_FOLDER": "/tmp"}
    mock_path.exists.return_value = True
    mock_evolution = models.EtoroEvolutionInner(dates=["2023-01-01"], parts={"test": [1.0]})
    mock_extract.return_value = mock_evolution
    
    query = models.EtoroAnalysisByNameQuery(filename="test.xlsx", precision="m")
    
    # Call async function
    task_id = stocks_service.analyze_etoro_evolution_by_name_async(query, "test@example.com")
    
    # Verify task was created
    assert task_id is not None
    task = task_manager.get_task(task_id)
    assert task is not None
    
    # Wait for completion
    time.sleep(0.1)
    
    # Verify the function was called with progress callback
    mock_extract.assert_called_once()
    args, kwargs = mock_extract.call_args
    assert "progress_callback" in kwargs
    assert callable(kwargs["progress_callback"])


def test_progress_callback_functionality():
    """Test that progress callback actually updates task progress."""
    from src.services.etoro_data import extract_closed_position
    
    # Create a task manually
    task_id = task_manager.create_task()
    
    def mock_progress_callback(step_name: str, step_number: int, step_count: int):
        task_manager.update_progress(task_id, step_name, step_number, step_count)
    
    # Test that the callback updates progress
    mock_progress_callback("Test step", 2, 4)
    
    task = task_manager.get_task(task_id)
    assert task is not None
    assert task.progress is not None
    assert task.progress.step_name == "Test step"
    assert task.progress.step_number == 2
    assert task.progress.step_count == 4