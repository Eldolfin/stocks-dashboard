"""Task management system for long-running operations with progress tracking."""

import threading
import uuid
from collections.abc import Callable
from dataclasses import dataclass
from enum import Enum
from typing import Any, Self


class TaskStatus(Enum):
    """Task execution status."""

    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"


@dataclass
class TaskProgress:
    """Progress information for a task."""

    step_name: str
    step_number: int
    step_count: int
    sub_task: Self | None = None


@dataclass
class Task:
    """Task information and state."""

    id: str
    status: TaskStatus
    progress: TaskProgress | None = None
    result: Any | None = None
    error: str | None = None


class TaskManager:
    """Manages long-running tasks with progress tracking."""

    def __init__(self) -> None:
        self._tasks: dict[str, Task] = {}
        self._lock = threading.Lock()

    def create_task(self) -> str:
        """Create a new task and return its ID."""
        task_id = str(uuid.uuid4())
        with self._lock:
            self._tasks[task_id] = Task(id=task_id, status=TaskStatus.PENDING)
        return task_id

    def get_task(self, task_id: str) -> Task | None:
        """Get task information by ID."""
        with self._lock:
            return self._tasks.get(task_id)

    def update_progress(self, task_id: str, new_progress: TaskProgress) -> None:
        """Update task progress."""
        with self._lock:
            if task_id in self._tasks:
                self._tasks[task_id].progress = new_progress
                if self._tasks[task_id].status == TaskStatus.PENDING:
                    self._tasks[task_id].status = TaskStatus.RUNNING

    def complete_task(self, task_id: str, result: Any) -> None:  # noqa: ANN401
        """Mark task as completed with result."""
        with self._lock:
            if task_id in self._tasks:
                self._tasks[task_id].status = TaskStatus.COMPLETED
                self._tasks[task_id].result = result

    def fail_task(self, task_id: str, error: str) -> None:
        """Mark task as failed with error message."""
        with self._lock:
            if task_id in self._tasks:
                self._tasks[task_id].status = TaskStatus.FAILED
                self._tasks[task_id].error = error

    def run_task(self, task_id: str, func: Callable[..., Any], *args: Any, **kwargs: Any) -> None:  # noqa: ANN401
        """Run a function as a background task."""

        def _run() -> None:
            try:
                result = func(task_id, *args, **kwargs)
                self.complete_task(task_id, result)
            except Exception as e:
                self.fail_task(task_id, str(e))

        thread = threading.Thread(target=_run)
        thread.start()


# Global task manager instance
task_manager = TaskManager()
