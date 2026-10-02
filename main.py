from task_manager import TaskManager
from errors import TaskManagerError


def show_menu():
    print("\n===== PYTHON TASK MANAGER =====")
    print("1. Add Task")
    print("2. View Tasks")
    print("3. Complete Task")
    print("4. Delete Task")
    print("5. Exit")


def main():
    manager = TaskManager()

    while True:
        show_menu()

        choice = input("Enter your choice: ").strip()

        try:
            if choice == "1":
                title = input("Enter task title: ")

                task = manager.add_task(title)

                print(
                    f"Task added successfully. "
                    f"Task ID: {task['id']}"
                )

            elif choice == "2":
                tasks = manager.get_tasks()

                if not tasks:
                    print("No tasks available.")
                else:
                    print("\n--- Tasks ---")

                    for task in tasks:
                        status = (
                            "Completed"
                            if task["completed"]
                            else "Pending"
                        )

                        print(
                            f"{task['id']}. "
                            f"{task['title']} - {status}"
                        )

            elif choice == "3":
                task_id = input("Enter task ID: ")

                manager.complete_task(task_id)

                print("Task marked as completed.")

            elif choice == "4":
                task_id = input("Enter task ID: ")

                manager.delete_task(task_id)

                print("Task deleted successfully.")

            elif choice == "5":
                print("Thank you for using Python Task Manager!")
                break

            else:
                print("Invalid choice. Please enter 1-5.")

        except TaskManagerError as error:
            print(f"Error: {error}")

        except ValueError as error:
            print(f"Error: {error}")

        except Exception as error:
            print(f"Unexpected error: {error}")


if __name__ == "__main__":
    main()