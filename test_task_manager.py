import json
import tempfile
import unittest
from pathlib import Path

from task_manager import TaskManager


class TaskManagerTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temporary_directory = tempfile.TemporaryDirectory()
        self.storage_path = Path(self.temporary_directory.name) / "tasks.json"
        self.manager = TaskManager(self.storage_path)

    def tearDown(self) -> None:
        self.temporary_directory.cleanup()

    def test_starts_empty_when_storage_file_is_missing(self) -> None:
        self.assertEqual(list(self.manager.all_tasks()), [])

    def test_add_strips_whitespace_and_persists(self) -> None:
        task = self.manager.add("  Buy milk  ")

        self.assertEqual(task.title, "Buy milk")
        reloaded_manager = TaskManager(self.storage_path)
        self.assertEqual([item.title for item in reloaded_manager.all_tasks()], ["Buy milk"])

    def test_empty_task_is_rejected(self) -> None:
        with self.assertRaisesRegex(ValueError, "cannot be empty"):
            self.manager.add("   ")

    def test_complete_task_persists(self) -> None:
        self.manager.add("Read a book")
        completed = self.manager.complete(1)

        self.assertTrue(completed.completed)
        reloaded_manager = TaskManager(self.storage_path)
        self.assertTrue(list(reloaded_manager.all_tasks())[0].completed)

    def test_delete_task_returns_deleted_task(self) -> None:
        self.manager.add("First task")
        self.manager.add("Second task")

        deleted = self.manager.delete(1)

        self.assertEqual(deleted.title, "First task")
        self.assertEqual(
            [task.title for task in self.manager.all_tasks()],
            ["Second task"],
        )

    def test_invalid_task_number_is_rejected(self) -> None:
        with self.assertRaisesRegex(ValueError, "Invalid task number"):
            self.manager.delete(1)

    def test_invalid_json_is_rejected(self) -> None:
        self.storage_path.write_text('{"not": "a list"}', encoding="utf-8")

        with self.assertRaises(ValueError):
            TaskManager(self.storage_path)

    def test_storage_is_valid_json(self) -> None:
        self.manager.add("Keep this task")

        saved_data = json.loads(self.storage_path.read_text(encoding="utf-8"))
        self.assertEqual(saved_data[0]["title"], "Keep this task")


if __name__ == "__main__":
    unittest.main()