import grpc
from local_task_scheduler.grpc_services.grpc_types import executor_pb2
from local_task_scheduler.grpc_services.grpc_types import executor_pb2_grpc


class SchedulerService:
    def __init__(self, executor_address="localhost:50051"):
        """Initializes the scheduler service with an empty tasks dictionary
        and a gRPC channel to the Executor Service."""
        self.tasks = {}  # Stores tasks by their ID
        self.channel = grpc.insecure_channel(executor_address)
        self.executor_client = executor_pb2_grpc.ExecutorServiceStub(self.channel)

    def schedule_task(self, task_request):
        """
        Schedules a new task and triggers its execution via the Executor Service.

        Args:
            task_request (dict): Task information including 'task_id', 'command', and 'parameters'.

        Returns:
            dict: A result dictionary containing 'success', 'task_id', and optionally 'error'.
        """
        task_id = task_request.get("task_id")
        if task_id in self.tasks:
            return {
                "success": False,
                "error": "Task ID already exists",
                "task_id": task_id,
            }

        # Store the task
        self.tasks[task_id] = task_request

        # Convert parameters dict to the format expected by gRPC
        grpc_parameters = {
            key: str(value) for key, value in task_request["parameters"].items()
        }

        # Trigger task execution via Executor Service
        grpc_request = executor_pb2.TaskRequest(
            task_id=task_id, command=task_request["command"], parameters=grpc_parameters
        )
        try:
            response = self.executor_client.ExecuteTask(grpc_request)
            # Interpret the response based on the 'status' field, 0 is for success
            success = response.status == 0
            error_msg = response.error if not success else ""
            return {"success": success, "task_id": task_id, "error": error_msg}
        except grpc.RpcError as e:
            return {"success": False, "error": str(e), "task_id": task_id}

    def list_tasks(self):
        """Lists all scheduled tasks.

        Returns:
            list: A list of all task dictionaries.
        """
        return list(self.tasks.values())

    def modify_task(self, modified_task_request):
        """
        Modifies an existing scheduled task.

        Args:
            modified_task_request (dict): Updated task information.

        Returns:
            dict: A result dictionary indicating success or failure.
        """
        task_id = modified_task_request.get("task_id")
        if task_id not in self.tasks:
            return {"success": False, "error": "Task not found"}

        self.tasks[task_id] = modified_task_request
        return {"success": True}

    def delete_task(self, task_id):
        """
        Deletes an existing scheduled task.

        Args:
            task_id (str): The ID of the task to delete.

        Returns:
            dict: A result dictionary indicating success or failure.
        """
        if task_id not in self.tasks:
            return {"success": False, "error": "Task not found"}

        del self.tasks[task_id]
        return {"success": True}
