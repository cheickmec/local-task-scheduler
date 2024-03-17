from unittest.mock import patch

import pytest
from click.testing import CliRunner

from local_task_scheduler.cli.command_line_interface import cli


@pytest.fixture
def mock_scheduler_service():
    with patch(
        "local_task_scheduler.cli.command_line_interface.scheduler_service"
    ) as mock:
        yield mock


@pytest.fixture
def runner():
    """Provides a Click CliRunner instance."""
    return CliRunner()


def test_cli_schedule_task(runner, mock_scheduler_service):
    """Test the CLI's ability to schedule a new task."""
    result = runner.invoke(
        cli,
        [
            "schedule",
            "--id",
            "1",
            "--command",
            "echo Hello World",
        ],
    )
    assert result.exit_code == 0
    mock_scheduler_service.schedule_task.assert_called_once_with(
        {
            "task_id": "1",
            "command": "echo Hello World",
            "parameters": {},
        }
    )


def test_cli_list_tasks(runner, mock_scheduler_service):
    """Test the CLI's ability to list scheduled tasks."""
    result = runner.invoke(cli, ["list"])
    assert result.exit_code == 0
    mock_scheduler_service.list_tasks.assert_called_once()


def test_cli_modify_task(runner, mock_scheduler_service):
    """Test the CLI's ability to modify an existing task."""
    result = runner.invoke(
        cli,
        [
            "modify",
            "--id",
            "1",
            "--command",
            "echo Hello Python",
            # Parameters handling
        ],
    )
    assert result.exit_code == 0
    mock_scheduler_service.modify_task.assert_called_once_with(
        {"task_id": "1", "command": "echo Hello Python", "parameters": {}}
    )


def test_cli_delete_task(runner, mock_scheduler_service):
    """Test the CLI's ability to delete a task."""
    result = runner.invoke(cli, ["delete", "--id", "1"])
    assert result.exit_code == 0
    mock_scheduler_service.delete_task.assert_called_once_with("1")
