import typer

import data
from data import *
from database import Database

interface = typer.Typer()
project_app = typer.Typer()
task_app = typer.Typer()

project_app.add_typer(task_app, name="tasks")
interface.add_typer(project_app, name="projects")

database = Database()


@project_app.command("list")
def project_list():
    """List of the available projects."""
    typer.clear()

    project_to_table(database.get_project_list())


@project_app.command("create")
def project_create(project_name: str, description: str = None):
    """Creates a new project"""
    typer.clear()

    project = Project(None, project_name, description)
    database.create_project(project)

    header_msg(f"Project {project_name} with the following description: {description} was created")


@project_app.command("clear")
def project_clear():
    """Deletes all projects from db"""
    typer.clear()

    database.clear_task()
    database.clear_project()

    header_msg("All projects were successfully deleted")


@task_app.command("list")
def task_list_by_project(project_name: str = None):
    """List of the available tasks in the given project or in the whole database"""
    typer.clear()

    if project_name is None:
        task_data_to_table(database.get_task_list())
    else:
        project_id = database.get_project_id(project_name)
        if len(project_id) == 0:
            error_msg(f"The project with the name {project_name} doesn't exist")
        else:
            header_msg(f"List of the tasks in the project {project_name}:")
            task_data_to_table(database.get_task_list_by_project(*project_id[0]))
            header_msg(f"Opened tasks: {database.count_task_by_state(*project_id[0], TaskStatus.OPEN)[0][0]}")
            header_msg(f"Closed tasks: {database.count_task_by_state(*project_id[0], TaskStatus.CLOSED)[0][0]}")


@task_app.command("clear")
def task_clear(project_name: str):
    """Deletes all tasks from project"""
    typer.clear()

    project_id = database.get_project_id(project_name)
    if len(project_id) == 0:
        error_msg(f"The project with the name {project_name} doesn't exist")
    else:
        database.clear_task_by_id(*project_id[0])
        header_msg("All tasks were successfully deleted")


@task_app.command("open")
def task_open(task_id: int):
    """Opens the task by task id"""
    typer.clear()

    header_msg(f"Opened the task with id: {task_id}")

    database.open_task(task_id)


@task_app.command("close")
def task_close(task_id: int):
    """Closes the task by task id"""
    typer.clear()

    header_msg(f"Closed the task with id: {task_id}")

    database.close_task(task_id)


@task_app.command("show")
def task_show(task_id: int):
    """Shows the task by task id"""
    typer.clear()

    task_data_to_table(database.get_task_by_id(task_id))


@task_app.command("create")
def task_create(project_name: str, title: str, description: str = None):
    """Create a new task"""
    typer.clear()

    project_id = database.get_project_id(project_name)
    if len(project_id) == 0:
        error_msg(f"The project with the name {project_name} doesn't exist")
    else:
        header_msg(f"Successfully added task {title} to the {project_name}")
        task = Task(None, title, description, data.TaskStatus.OPEN, *project_id[0])
        database.create_task(task)


if __name__ == "__main__":
    interface()
