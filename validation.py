def validate_title(title):
    """Validate a task title."""

    if not isinstance(title, str):
        raise ValueError("Task title must be text.")

    title = title.strip()

    if not title:
        raise ValueError("Task title cannot be empty.")

    if len(title) > 100:
        raise ValueError("Task title cannot exceed 100 characters.")

    return title


def validate_task_id(task_id):
    """Validate a task ID."""

    try:
        task_id = int(task_id)
    except (ValueError, TypeError):
        raise ValueError("Task ID must be a number.")

    if task_id <= 0:
        raise ValueError("Task ID must be greater than zero.")

    return task_id