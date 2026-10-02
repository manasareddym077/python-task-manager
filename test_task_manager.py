import unittest

from task_manager import TaskManager
from errors import TaskNotFoundError


class TestTaskManager(unittest.TestCase):

    def setUp(self):
        self.manager = TaskManager()

    def test_add_task(self):
        task = self.manager.add_task("Learn Python")

        self.assertEqual(task["id"], 1)
        self.assertEqual(task["title"], "Learn Python")
        self.assertFalse(task["completed"])

    def test_empty_task(self):
        with self.assertRaises(ValueError):
            self.manager.add_task("")

    def test_long_task(self):
        long_title = "A" * 101

        with self.assertRaises(ValueError):
            self.manager.add_task(long_title)

    def test_complete_task(self):
        task = self.manager.add_task("Complete Task 4")

        self.manager.complete_task(task["id"])

        self.assertTrue(task["completed"])

    def test_delete_task(self):
        task = self.manager.add_task("Delete this")

        self.manager.delete_task(task["id"])

        self.assertEqual(len(self.manager.get_tasks()), 0)

    def test_task_not_found(self):
        with self.assertRaises(TaskNotFoundError):
            self.manager.get_task(999)

    def test_invalid_task_id(self):
        with self.assertRaises(ValueError):
            self.manager.get_task("abc")


if __name__ == "__main__":
    unittest.main()