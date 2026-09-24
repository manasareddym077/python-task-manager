import json
import os
import tempfile

TASKS_FILE = "tasks.json"


def load_tasks():
    if not os.path.exists(TASKS_FILE):
        return []

    try:
        with open(TASKS_FILE, "r", encoding="utf-8") as file:
            return json.load(file)
    except (json.JSONDecodeError, OSError):
        return []


def save_tasks(tasks):
    directory = os.path.dirname(os.path.abspath(TASKS_FILE))

    fd, temp_path = tempfile.mkstemp(
        dir=directory,
        prefix="tasks_",
        suffix=".tmp"
    )

    try:
        with os.fdopen(fd, "w", encoding="utf-8") as file:
            json.dump(tasks, file, indent=2)
            file.flush()
            os.fsync(file.fileno())

        os.replace(temp_path, TASKS_FILE)

    except Exception:
        try:
            os.remove(temp_path)
        except OSError:
            pass
        raise


def add_task(tasks):
    name = input("Enter task name: ").strip()

    if not name:
        print("Error: task name cannot be empty.")
        return

    tasks.append({
        "name": name,
        "completed": False
    })

    save_tasks(tasks)
    print("Task added successfully.")


def view_tasks(tasks):
    if not tasks:
        print("No tasks found.")
        return

    print("\nTasks:")

    for i, task in enumerate(tasks, 1):
        status = "✓" if task["completed"] else " "
        print(f"{i}. [{status}] {task['name']}")


def get_task_index(tasks):
    if not tasks:
        print("No tasks available.")
        return None

    try:
        number = int(input("Enter task number: "))
    except ValueError:
        print("Error: enter a valid number.")
        return None

    if number < 1 or number > len(tasks):
        print("Error: invalid task number.")
        return None

    return