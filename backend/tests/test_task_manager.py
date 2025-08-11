"""Tests for task manager functionality."""

import time
from unittest.mock import patch

from src.services.task_manager import TaskManager, TaskStatus


def test_task_creation() -> None:
    """Test task creation."""
    manager = TaskManager()
    task_id = manager.create_task()
    assert task_id is not None

    task = manager.get_task(task_id)
    assert task is not None
    assert task.status == TaskStatus.PENDING


def test_task_progress_update() -> None:
    """Test progress updates."""
    manager = TaskManager()
    task_id = manager.create_task()

    manager.update_progress(task_id, "Test step", 1, 3)

    task = manager.get_task(task_id)
    assert task is not None
    assert task.status == TaskStatus.RUNNING
    assert task.progress is not None
    assert task.progress.step_name == "Test step"
    assert task.progress.step_number == 1
    assert task.progress.step_count == 3


def test_task_completion() -> None:
    """Test task completion."""
    manager = TaskManager()
    task_id = manager.create_task()

    result = {"test": "data"}
    manager.complete_task(task_id, result)

    task = manager.get_task(task_id)
    assert task is not None
    assert task.status == TaskStatus.COMPLETED
    assert task.result == result


def test_task_failure() -> None:
    """Test task failure."""
    manager = TaskManager()
    task_id = manager.create_task()

    error_msg = "Test error"
    manager.fail_task(task_id, error_msg)

    task = manager.get_task(task_id)
    assert task is not None
    assert task.status == TaskStatus.FAILED
    assert task.error == error_msg


def test_run_task_success() -> None:
    """Test running a successful task."""
    manager = TaskManager()
    task_id = manager.create_task()

    def test_func(task_id: str) -> str:
        return "success"

    manager.run_task(task_id, test_func)

    # Wait a bit for the task to complete
    time.sleep(0.1)

    task = manager.get_task(task_id)
    assert task is not None
    assert task.status == TaskStatus.COMPLETED
    assert task.result == "success"


def test_run_task_with_exception() -> None:
    """Test running a task that raises an exception."""
    manager = TaskManager()
    task_id = manager.create_task()

    def test_func(task_id: str) -> str:
        raise ValueError("Test exception")

    manager.run_task(task_id, test_func)

    # Wait a bit for the task to complete
    time.sleep(0.1)

    task = manager.get_task(task_id)
    assert task is not None
    assert task.status == TaskStatus.FAILED
    assert "Test exception" in task.error


def test_nonexistent_task() -> None:
    """Test getting a non-existent task."""
    manager = TaskManager()
    task = manager.get_task("nonexistent")
    assert task is None
