
# Task Manager

A simple persistent command-line task manager written with Python's standard
library. Tasks are saved to `tasks.json` in the project directory.

## Features

- Add tasks
- View all tasks
- Mark tasks as complete
- Delete tasks
- Persist tasks between runs
- Validate empty task names and invalid task numbers
- Atomic file saves to reduce the risk of corrupting task data
- Automated tests using `unittest`

## Requirements

- Python 3.10 or newer
- No third-party packages

## Run the application

```bash
python task_manager.py
```

## Run the tests

```bash
python -m unittest -v
```

