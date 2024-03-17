import logging
from concurrent import futures

import grpc

from local_task_scheduler.executor.executor_service import ExecutorService
from local_task_scheduler.grpc_services.grpc_types import executor_pb2_grpc

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(message)s")


def serve():
    logging.info("Starting gRPC server...")
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    executor_pb2_grpc.add_ExecutorServiceServicer_to_server(ExecutorService(), server)
    server.add_insecure_port("[::]:50051")
    try:
        server.start()
        logging.info("gRPC server listening on port 50051")
        server.wait_for_termination()
    except Exception as e:
        logging.error(f"gRPC server error: {e}")


if __name__ == "__main__":
    serve()
