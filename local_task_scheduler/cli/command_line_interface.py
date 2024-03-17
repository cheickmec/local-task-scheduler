import click

from local_task_scheduler.scheduler.scheduler_service import SchedulerService

# Initialize the SchedulerService
scheduler_service = SchedulerService()


@click.group()
def cli():
    """Local Task Scheduler CLI."""
    pass


@click.command(help="Schedule a new task")
@click.option("--id", required=True, help="Task ID")
@click.option("--command", required=True, help="Command to execute")
@click.option(
    "--parameters",
    multiple=True,
    type=(str, str),
    help="Additional parameters in key=value format",
)
def schedule(id, command, parameters):
    task_request = {"task_id": id, "command": command, "parameters": dict(parameters)}
    response = scheduler_service.schedule_task(task_request)
    click.echo(
        "Task Scheduled"
        if response["success"]
        else "Failed to schedule task: " + response.get("error")
    )


@click.command(help="List all scheduled tasks")
def list_tasks():
    tasks = scheduler_service.list_tasks()
    for task in tasks:
        click.echo(f"ID: {task['task_id']}, Command: {task['command']}")


@click.command(help="Modify an existing task")
@click.option("--id", required=True, help="Task ID")
@click.option("--command", required=True, help="New command to execute")
@click.option(
    "--parameters",
    multiple=True,
    type=(str, str),
    help="New additional parameters in key=value format",
)
def modify(id, command, parameters):
    modified_task_request = {
        "task_id": id,
        "command": command,
        "parameters": dict(parameters),
    }
    response = scheduler_service.modify_task(modified_task_request)
    click.echo(
        "Task Modified"
        if response["success"]
        else "Failed to modify task: " + response.get("error")
    )


@click.command(help="Delete an existing task")
@click.option("--id", required=True, help="Task ID to delete")
def delete(id):
    response = scheduler_service.delete_task(id)
    click.echo(
        "Task Deleted"
        if response["success"]
        else "Failed to delete task: " + response.get("error")
    )


# Add commands to the CLI group
cli.add_command(schedule)
cli.add_command(list_tasks, name="list")
cli.add_command(modify)
cli.add_command(delete)

if __name__ == "__main__":
    cli()
