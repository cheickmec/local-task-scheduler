import subprocess

from local_task_scheduler.grpc_services.grpc_types import (
    executor_pb2,
    executor_pb2_grpc,
)


class ExecutorService(executor_pb2_grpc.ExecutorServiceServicer):
    def ExecuteTask(self, request, context):
        try:
            # Running the command
            completed_process = subprocess.run(
                request.command, shell=True, capture_output=True, text=True
            )
            if completed_process.returncode == 0:
                return executor_pb2.TaskResponse(
                    task_id=request.task_id, status=0, output=completed_process.stdout
                )
            else:
                return executor_pb2.TaskResponse(
                    task_id=request.task_id,
                    status=completed_process.returncode,
                    error=completed_process.stderr,
                )
        except Exception as e:
            return executor_pb2.TaskResponse(
                task_id=request.task_id,
                status=-1,  # A custom status indicating internal failure
                error=str(e),
            )
