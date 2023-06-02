import os.path
import sqlite3

import data


class Database:
    DB_PATH = "todos.db"

    # sql queries
    # tables creation
    PROJECT_TABLE = """
        CREATE TABLE project(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT, 
            description TEXT NULL
        );
    """

    TASK_TABLE = """
        CREATE TABLE task(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT, 
            description TEXT,
            status INTEGER, 
            project_id INTEGER,
            FOREIGN KEY(project_id) REFERENCES project(id)
        );
    """

    # project queries
    PROJECT_LIST = "SELECT * FROM project;"
    PROJECT_CLEAR = "DELETE FROM project;"
    PROJECT_CREATE = "INSERT INTO project(name, description) VALUES(?, ?);"
    PROJECT_ID_BY_NAME = "SELECT id FROM project WHERE name = ? LIMIT 1;"

    # task queries
    TASK_LIST = "SELECT * FROM task;"
    TASK_CLEAR = "DELETE FROM task;"
    TASK_LIST_BY_PROJECT = "SELECT * FROM task WHERE project_id = (?);"
    TASK_BY_ID = "SELECT * FROM task WHERE id = ?;"
    TASK_STATUS_UPDATE = "UPDATE task SET status = ? WHERE id = ?;"
    TASK_CREATE = "INSERT INTO task(title, description, status, project_id) VALUES(?, ?, ?, ?);"
    TASK_COUNT_BY_STATE = "SELECT COUNT() FROM task WHERE project_id = ? AND status = ?;"
    TASK_CLEAR_BY_ID = "DELETE FROM task WHERE project_id = ?;"

    def get_project_list(self):
        return self.run_query(query=self.PROJECT_LIST, fetch=True)

    def clear_project(self):
        return self.run_query(query=self.PROJECT_CLEAR, commit=True)

    def create_project(self, project: data.Project):
        return self.run_query(query=self.PROJECT_CREATE, args=(project.name, project.description), commit=True)

    def get_project_id(self, project_name: str):
        return self.run_query(query=self.PROJECT_ID_BY_NAME, args=[project_name], fetch=True)

    def get_task_list(self):
        return self.run_query(query=self.TASK_LIST, fetch=True)

    def clear_task(self):
        return self.run_query(query=self.TASK_CLEAR, commit=True)

    def get_task_list_by_project(self, project_id: int):
        return self.run_query(query=self.TASK_LIST_BY_PROJECT, args=[project_id], fetch=True)

    def close_task(self, task_id: int):
        return self.run_query(query=self.TASK_STATUS_UPDATE, args=(data.TaskStatus.CLOSED, task_id), commit=True)

    def open_task(self, task_id: int):
        return self.run_query(query=self.TASK_STATUS_UPDATE, args=(data.TaskStatus.OPEN, task_id), commit=True)

    def get_task_by_id(self, task_id: int):
        return self.run_query(query=self.TASK_BY_ID, args=[task_id], fetch=True)

    def create_task(self, task: data.Task):
        return self.run_query(query=self.TASK_CREATE, args=(task.title, task.description, task.status, task.project_id),
                              commit=True)

    def count_task_by_state(self, project_id: int, status: int):
        return self.run_query(query=self.TASK_COUNT_BY_STATE, args=(project_id, status), fetch=True)

    def clear_task_by_id(self, project_id):
        return self.run_query(query=self.TASK_CLEAR_BY_ID, args=[project_id], commit=True)

    def run_query(self, query, args=None, commit=False, fetch=False):
        args = args or ()
        fetched_data = None

        with self.get_connection() as connection:
            cursor = connection.cursor()
            cursor.execute(query, args)

            if commit:
                connection.commit()
            if fetch:
                fetched_data = cursor.fetchall()

        return fetched_data

    def db_exist(self):
        return os.path.exists(self.DB_PATH)

    def get_connection(self):
        return sqlite3.connect(self.DB_PATH)

    def initialize(self):
        if self.db_exist():
            return

        with self.get_connection() as connection:
            cursor = connection.cursor()

            cursor.execute(self.PROJECT_TABLE)
            cursor.execute(self.TASK_TABLE)

            connection.commit()
