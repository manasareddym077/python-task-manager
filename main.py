from task_manager import TaskManager


def show_menu():
    """Display the main menu."""

    print("\n===== TASK MANAGER =====")
    print("1. Add Task")
    print("2. View Tasks")
    print("3. Complete Task")
    print("4. Delete Task")
    print("5. Exit")


def main():
    """Run the Task Manager application."""

    manager = TaskManager()

    while True:
        show_menu()

        choice = input("Enter your choice: ").strip()

        if choice == "1":
            task = input("Enter task: ")

            try:
                manager.add_task(task)
            except ValueError as error:
                print("Error:", error)

        elif choice == "2":
            manager.view_tasks()

        elif choice == "3":
            manager.complete_task()

        elif choice == "4":
            manager.delete_task()

        elif choice == "5":
            print("Thank you for using Task Manager!")
            break

        else:
            print("Invalid choice! Please enter 1-5.")


if __name__ == "__main__":
    main()