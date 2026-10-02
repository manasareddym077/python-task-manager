class TaskManagerError(Exception):
    """Base error for the Task Manager."""


class TaskNotFoundError(TaskManagerError):
    """Raised when a task cannot be found."""