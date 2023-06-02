from enum import IntEnum
from dataclasses import dataclass
from typing import Union

from rich import print
from rich.table import Table


class TaskStatus(IntEnum):
    OPEN = 0
    CLOSED = 1


@dataclass
class Project:
    id: Union[int, None]
    name: str
    description: Union[str, None]


@dataclass
class Task:
    id: Union[int, None]
    title: str
    description: Union[str, None]
    status: int
    project_id: int


def error_msg(str_):
    print(f"[bold red]{str_}[/bold red]")


def success_msg(str_):
    print(f"[bold green3]{str_}[bold /green3]")


def header_msg(str_):
    print(f"[bold blue]{str_}[/bold blue]")


def project_to_table(fetched_data):
    project_table = Table("Id", "Name", "Description", style="green")
    project_table.title = "Projects table :construction:"
    project_table.title_style = "bold white"
    project_table.header_style = "bold yellow"

    for row in fetched_data:
        project_table.add_row(str(row[0]), str(row[1]), str(row[2]), style="bold white")

    print(project_table)


def task_data_to_table(fetched_data):
    task_table = Table("Id", "Title", "Description", "Status", "Project Id", style="green")
    task_table.title = "Tasks table :pencil:"
    task_table.title_style = "bold white"
    task_table.header_style = "bold yellow"

    for row in fetched_data:
        if row[3] == 1:
            status = "CLOSED"
        else:
            status = "OPEN"

        task_table.add_row(str(row[0]), str(row[1]), str(row[2]), status, str(row[4]), style="bold white")

    print(task_table)
