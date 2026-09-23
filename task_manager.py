"""A small, persistent command-line task manager."""

from __future__ import annotations

import json
import os
import tempfile
from dataclasses import asdict, dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Iterable


@dataclass
class Task:
    """A task stored by the task manager."""

    title: str
    completed: bool = False
    created_at: str = ""

    def __post_init__(self) -> None:
        if not self.created_at:
            self.created_at = datetime.now(timezone.utc).isoformat()


class TaskManager:
    """Manage tasks and persist them to a JSON file."""

    def __init__(self, storage_path: str | Path = "tasks.json") -> None:
        self.storage_path = Path(storage_path)
        self.tasks: list[Task] = []
        self.load()

    def load(self) -> None:
        """Load tasks from disk, treating a missing file as an empty list."""
        if not self.storage_path.exists():
            self.tasks = []
            return

        try:
            with self.storage_path.open("r", encoding="utf-8") as file:
                raw_tasks = json.load(file)
        except (OSError, json.JSONDecodeError) as error:
            raise ValueError(f"Could not read {self.storage_path}: {error}") from error

        if not isinstance(raw_tasks, list):
            raise ValueError(f"{self.storage_path} must contain a JSON list")

        self.tasks = [self._task_from_dict(item) for item in raw_tasks]

    def save(self) -> None:
        """Save tasks atomically so an interrupted write does not corrupt the file."""
        self.storage_path.parent.mkdir(parents=True, exist_ok=True)

        file_descriptor, temporary_name = tempfile.mkstemp(
            prefix=f".{self.storage_path.name}.",
            dir=self.storage_path.parent,
            text=True,
        )

        try:
            with os.fdopen(file_descriptor, "w", encoding="utf-8") as file:
                json.dump([asdict(task) for task in self.tasks], file, indent=2)
                file.write("\n")
            os.replace(temporary_name, self.storage_path)
        except OSError:
            try:
                os.unlink(temporary_name)
            except OSError:
                pass
            raise

    def add(self, title: str) -> Task:
        """Add a non-empty task and return it."""
        cleaned_title = title.strip()
        if not cleaned_title:
            raise ValueError("Task cannot be empty.")

        task = Task(cleaned_title)
        self.tasks.append(task)
        self.save()
        return task

    def complete(self, task_number: int) -> Task:
        """Mark a task as complete using its 1-based display number."""
        task = self._get_task(task_number)
        if task.completed:
            raise ValueError("Task is already complete.")

        task.completed = True
        self.save()
        return task

    def delete(self, task_number: int) -> Task:
        """Delete a task using its 1-based display number."""
        index = self._get_index(task_number)
        deleted_task = self.tasks.pop(index)
        self.save()
        return deleted_task

    def all_tasks(self) -> Iterable[Task]:
        """Return tasks in their display order."""
        return tuple(self.tasks)

    def _get_task(self, task_number: int) -> Task:
        return self.tasks[self._get_index(task_number)]

    def _get_index(self, task_number: int) -> int:
        if not isinstance(task_number, int) or isinstance(task_number, bool):
            raise ValueError("Task number must be an integer.")
        if task_number < 1 or task_number > len(self.tasks):
            raise ValueError("Invalid task number.")
        return task_number - 1

    @staticmethod
    def _task_from_dict(value: object) -> Task:
        if not isinstance(value, dict):
            raise ValueError("Each saved task must be an object.")

        title = value.get("title")
        completed = value.get("completed", False)
        created_at = value.get("created_at", "")

        if not isinstance(title, str) or not title.strip():
            raise ValueError("Each saved task needs a non-empty title.")
        if not isinstance(completed, bool):
            raise ValueError("Task completion status must be true or false.")
        if not isinstance(created_at, str):
            raise ValueError("Task creation time must be text.")

        return Task(title=title, completed=completed, created_at=created_at)


def display_tasks(manager: TaskManager) -> None:
    tasks = list(manager.all_tasks())
    if not tasks:
        print("\nNo tasks available.")
        return

    print("\nYour Tasks:")
    for number, task in enumerate(tasks, start=1):
        status = "x" if task.completed else " "
        print(f"{number}. [{status}] {task.title}")


def read_input(prompt: str) -> str | None:
    """Read input and exit cleanly when stdin is closed."""
    try:
        return input(prompt)
    except EOFError:
        print("\nInput closed. Exiting.")
        return None


def read_task_number(prompt: str) -> int | None:
    try:
        value = read_input(prompt)
        if value is None:
            return None
        return int(value.strip())
    except ValueError:
        print("Please enter a valid task number.")
        return None


def run_cli(manager: TaskManager) -> None:
    """Run the interactive command-line interface."""
    while True:
        print("\n===== TASK MANAGER =====")
        print("1. Add Task")
        print("2. View Tasks")
        print("3. Complete Task")
        print("4. Delete Task")
        print("5. Exit")

        choice = read_input("Enter your choice: ")
        if choice is None:
            return
        choice = choice.strip()

        try:
            if choice == "1":
                title = read_input("Enter task: ")
                if title is None:
                    return
                task = manager.add(title)
                print(f"Task added: {task.title}")
            elif choice == "2":
                display_tasks(manager)
            elif choice == "3":
                number = read_task_number("Enter task number to complete: ")
                if number is not None:
                    task = manager.complete(number)
                    print(f"Completed: {task.title}")
            elif choice == "4":
                number = read_task_number("Enter task number to delete: ")
                if number is not None:
                    task = manager.delete(number)
                    print(f"Deleted: {task.title}")
            elif choice == "5":
                print("Thank you!")
                return
            else:
                print("Invalid choice. Please select 1-5.")
        except ValueError as error:
            print(f"Error: {error}")
        except OSError as error:
            print(f"Storage error: {error}")


def main() -> None:
    try:
        run_cli(TaskManager())
    except ValueError as error:
        print(f"Could not start task manager: {error}")


if __name__ == "__main__":
    main()