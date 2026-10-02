import unittest
import os
import tempfile

from task_manager import TaskManager


class TestTaskManager(unittest.TestCase):

    def setUp(self):
        self.test_file = tempfile.NamedTemporaryFile(
            delete=False
        ).name

        self.manager = TaskManager(self.test_file)

    def tearDown(self):
        if os.path.exists(self.test_file):
            os.remove(self.test_file)

    def test_add_task(self):
        self.manager.add_task("Learn Python")

        self.assertEqual(len(self.manager.tasks), 1)
        self.assertEqual(
            self.manager.tasks[0]["task"],
            "Learn Python"
        )

    def test_empty_task(self):
        with self.assertRaises(ValueError):
            self.manager.add_task("")

    def test_complete_task(self):
        self.manager.add_task("Complete project")

        self.manager.tasks[0]["completed"] = True

        self.assertTrue(
            self.manager.tasks[0]["completed"]
        )

    def test_delete_task(self):
        self.manager.add_task("Delete me")

        self.manager.tasks.pop(0)

        self.assertEqual(len(self.manager.tasks), 0)


if __name__ == "__main__":
    unittest.main()