from validation import validate_title, validate_task_id
from errors import TaskNotFoundError


class TaskManager:
    """Manage tasks for the application."""

    def __init__(self):
        self.tasks = []
        self.next_id = 1

    def add_task(self, title):
        """Add a new task."""

        title = validate_title(title)

        task = {
            "id": self.next_id,
            "title": title,
            "completed": False
        }

        self.tasks.append(task)
        self.next_id += 1

        return task

    def get_tasks(self):
        """Return all tasks."""
        return self.tasks

    def get_task(self, task_id):
        """Find a task by ID."""

        task_id = validate_task_id(task_id)

        for task in self.tasks:
            if task["id"] == task_id:
                return task

        raise TaskNotFoundError(
            f"Task with ID {task_id} was not found."
        )

    def complete_task(self, task_id):
        """Mark a task as completed."""

        task = self.get_task(task_id)
        task["completed"] = True

        return task

    def delete_task(self, task_id):
        """Delete a task."""

        task = self.get_task(task_id)
        self.tasks.remove(task)

        return task