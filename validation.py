def validate_task(task):
    """Validate the task name."""

    if not isinstance(task, str):
        raise ValueError("Task must be text.")

    task = task.strip()

    if task == "":
        raise ValueError("Task cannot be empty!")

    if len(task) > 200:
        raise ValueError("Task is too long. Maximum 200 characters.")

    return task


def validate_task_number(number, total_tasks):
    """Validate the selected task number."""

    try:
        number = int(number)
    except ValueError:
        raise ValueError("Task number must be a number.")

    if number < 1 or number > total_tasks:
        raise ValueError("Invalid task number.")

    return number