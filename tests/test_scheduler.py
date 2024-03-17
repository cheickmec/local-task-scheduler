import pytest

from local_task_scheduler.scheduler.scheduler_service import SchedulerService


@pytest.fixture
def scheduler_service():
    """Fixture to initialize the SchedulerService before each test."""
    return SchedulerService()


def test_schedule_task(scheduler_service):
    """Test scheduling a new task."""
    task_request = {"task_id": "1", "command": "echo Hello World", "parameters": {}}
    response = scheduler_service.schedule_task(task_request)
    assert response["success"] is True
    assert response["task_id"] == "1"


def test_list_tasks(scheduler_service):
    """Test listing all scheduled tasks."""
    # Assuming a task has been scheduled
    scheduler_service.schedule_task(
        {"task_id": "1", "command": "echo Hello World", "parameters": {}}
    )
    tasks = scheduler_service.list_tasks()
    assert len(tasks) > 0
    assert tasks[0]["task_id"] == "1"


def test_modify_task(scheduler_service):
    """Test modifying an existing scheduled task."""
    # Schedule a task and then modify it
    task_request = {"task_id": "1", "command": "echo Hello World", "parameters": {}}
    scheduler_service.schedule_task(task_request)

    modified_task_request = {
        "task_id": "1",
        "command": "echo Hello Python",
        "parameters": {"additional": "param"},
    }
    response = scheduler_service.modify_task(modified_task_request)
    assert response["success"] is True
    # Verify that the task was modified
    tasks = scheduler_service.list_tasks()
    assert tasks[0]["command"] == "echo Hello Python"


def test_delete_task(scheduler_service):
    """Test deleting an existing scheduled task."""
    # Schedule a task
    scheduler_service.schedule_task(
        {"task_id": "1", "command": "echo Hello World", "parameters": {}}
    )
    # Delete the task
    response = scheduler_service.delete_task("1")
    assert response["success"] is True
    # Verify that the task no longer exists
    tasks = scheduler_service.list_tasks()
    assert len(tasks) == 0
