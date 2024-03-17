import pytest
from local_task_scheduler.executor.executor_service import ExecutorService
from local_task_scheduler.grpc_services.grpc_types import executor_pb2


@pytest.fixture(scope="module")
def executor_service():
    service = ExecutorService()
    # In a real scenario, you'd launch the server in a separate thread/process:
    # serve()
    return service


def test_execute_task_success(executor_service):
    request = executor_pb2.TaskRequest(
        task_id="1", command="echo Hello, Executor!", parameters={}
    )
    response = executor_service.ExecuteTask(
        request, None
    )  # Passing 'None' for the gRPC context
    assert response.status == 0
    assert response.output.strip() == "Hello, Executor!"
    assert response.task_id == "1"


def test_ls_command(executor_service):
    request = executor_pb2.TaskRequest(task_id="2", command="ls", parameters={})
    response = executor_service.ExecuteTask(request, None)
    assert response.status == 0
    assert __name__.split(".")[-1] in response.output.lower()


def test_execute_task_failure(executor_service):
    request = executor_pb2.TaskRequest(
        task_id="2", command="invalidcommand", parameters={}
    )
    response = executor_service.ExecuteTask(request, None)
    assert response.status != 0
    assert "invalidcommand" in response.error.lower()
    assert response.task_id == "2"
