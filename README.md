# Local Task Scheduler and Executor
```mermaid
graph LR;
    CLI[CLI Interface] -->|Schedules Tasks| Scheduler[Scheduler Service];
    Scheduler -->|Requests Execution| Executor[Executor Service];
    Scheduler -->|Stores Tasks| DB[(Database)];
    Executor -->|Executes Tasks| System[System/Environment];
    
    classDef service fill:#f9f,stroke:#333,stroke-width:2px;
    classDef database fill:#bbf,stroke:#f66,stroke-width:2px,stroke-dasharray: 5;
    classDef module fill:#dfd,stroke:#393,stroke-width:2px;
    class Scheduler,Executor,Logger service;
    class DB database;
    class Security,CLI module;
    
```
## Overview
The Local Task Scheduler and Executor is a robust backend system designed to schedule and execute tasks with precision and reliability. Utilizing gRPC for efficient inter-service communication and focusing on security, this system allows for the definition, scheduling, and execution of tasks via a command-line interface.

## Features
- **Task Scheduling**: Schedule tasks specifying commands to run and their execution times.
- **Task Execution**: Executes scheduled tasks, handling concurrent execution.
- **Security**: Implements basic encryption for task data and gRPC communication.
- **CLI**: Command-line interface for managing tasks.

## Getting Started

### Prerequisites
- Python 3.12 or newer
- Poetry for dependency management

Note: Before running any script, ensure your PYTHONPATH includes the path `local_task_scheduler/grpc_services/grpc_types`
### Installation
1. Clone the repository:
```shell
git clone https://cheickmec/local-task-scheduler.git
cd local-task-scheduler
```
1. Install dependencies using Poetry:
```shell
poetry install
```
1. Generate Python classes from Protobuf definitions (ensure `protoc` is installed):
```shell
poetry run python -m grpc_tools.protoc \
  -I./local_task_scheduler/grpc_services/protobufs \
  --python_out=./local_task_scheduler/grpc_services/grpc_types \
  --pyi_out=./local_task_scheduler/grpc_services/grpc_types \
  --grpc_python_out=./local_task_scheduler/grpc_services/grpc_types \
  ./local_task_scheduler/grpc_services/protobufs/*.proto
```
### Testing the Application
- To run all tests
```shell
poetry run pytest tests
```

### Running the Application
- To start the application locally:
```shell
poetry run python main.py
```

- To run using Docker:
```shell
docker-compose up --build
```


## Usage
Describe how to use the command-line interface, including commands for scheduling, listing, modifying, and deleting tasks.

## Development
This section outlines the project structure, important modules, and guidelines for developing new features or fixing bugs.

### Project Structure
Briefly describe the project structure and the purpose of each component.

### Coding Standards
- Follow PEP 8 for style guidelines.
- Use type hints according to PEP 484.
- Write comprehensive tests for new features or bug fixes.

## Contributing
We welcome contributions! Please read [our contributing guidelines](CONTRIBUTING.md) to get started.

## License

## Contact
