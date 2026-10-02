import json
import os
from errors import TaskManagerError
from validation import validate_task, validate_task_number


class TaskManager:
    """Manages tasks with persistent JSON storage."""

    def __init__(self, filename="tasks.json"):
        self.filename = filename
        self.tasks = []
        self.load_tasks()

    def load_tasks(self):
        """Load tasks from the JSON file."""
        if not os.path.exists(self.filename):
            self.tasks = []
            return

        try:
            with open(self.filename, "r") as file:
                self.tasks = json.load(file)
        except (json.JSONDecodeError, OSError):
            self.tasks = []

    def save_tasks(self):
        """Save tasks safely to the JSON file."""
        temp_file = self.filename + ".tmp"

        try:
            with open(temp_file, "w") as file:
                json.dump(self.tasks, file, indent=4)

            os.replace(temp_file, self.filename)

        except OSError as error:
            raise TaskManagerError(f"Unable to save tasks: {error}")

    def add_task(self, task):
        """Add a new task."""
        task = validate_task(task)

        self.tasks.append({
            "task": task,
            "completed": False
        })

        self.save_tasks()
        print("Task added successfully!")

    def view_tasks(self):
        """Display all tasks."""
        if not self.tasks:
            print("No tasks available.")
            return

        print("\nYour Tasks:")

        for i, task in enumerate(self.tasks, 1):
            status = "Completed" if task["completed"] else "Pending"
            print(f"{i}. {task['task']} - {status}")

    def complete_task(self):
        """Mark a task as completed."""
        if not self.tasks:
            print("No tasks available.")
            return

        try:
            number = validate_task_number(
                input("Enter task number to complete: "),
                len(self.tasks)
            )

            self.tasks[number - 1]["completed"] = True
            self.save_tasks()

            print("Task completed successfully!")

        except ValueError as error:
            print("Error:", error)

    def delete_task(self):
        """Delete a task."""
        if not self.tasks:
            print("No tasks available.")
            return

        try:
            number = validate_task_number(
                input("Enter task number to delete: "),
                len(self.tasks)
            )

            removed = self.tasks.pop(number - 1)
            self.save_tasks()

            print(f"Deleted: {removed['task']}")

        except ValueError as error:
            print("Error:", error)