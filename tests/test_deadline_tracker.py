"""Tests for common actions and mistakes in the deadline tracker."""

import json
import subprocess
import sys
import tempfile
import unittest
from datetime import date, timedelta
from pathlib import Path


SCRIPT = Path(__file__).resolve().parents[1] / "scripts" / "deadline_tracker.py"


class DeadlineTrackerTests(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.data_file = Path(self.temp_dir.name) / "tasks.json"

    def tearDown(self):
        self.temp_dir.cleanup()

    def run_tracker(self, *args):
        return subprocess.run(
            [sys.executable, str(SCRIPT), "--data-file", str(self.data_file), *args],
            capture_output=True, text=True, check=False,
        )

    def test_add_and_list_persists_task(self):
        result = self.run_tracker("add", "Mini-Project 2", "2026-10-28")
        self.assertEqual(result.returncode, 0, result.stderr)
        data = json.loads(self.data_file.read_text(encoding="utf-8"))
        self.assertEqual(data[0]["title"], "Mini-Project 2")
        self.assertIn("Mini-Project 2", self.run_tracker("list").stdout)

    def test_invalid_date_does_not_save_task(self):
        result = self.run_tracker("add", "Wrong date", "2026-02-30")
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("valid date", result.stderr)
        self.assertFalse(self.data_file.exists())

    def test_blank_title_is_rejected(self):
        result = self.run_tracker("add", "  ", "2026-10-28")
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("cannot be empty", result.stderr)

    def test_done_hides_task_from_pending_list(self):
        self.run_tracker("add", "Read chapter", "2026-12-01")
        self.assertEqual(self.run_tracker("done", "1").returncode, 0)
        self.assertNotIn("Read chapter", self.run_tracker("list").stdout)
        self.assertIn("Read chapter", self.run_tracker("list", "--all").stdout)

    def test_nonexistent_id_does_not_change_data(self):
        self.run_tracker("add", "Read chapter", "2026-12-01")
        before = self.data_file.read_text(encoding="utf-8")
        result = self.run_tracker("done", "99")
        self.assertNotEqual(result.returncode, 0)
        self.assertEqual(before, self.data_file.read_text(encoding="utf-8"))

    def test_upcoming_includes_overdue_tasks(self):
        yesterday = (date.today() - timedelta(days=1)).isoformat()
        tomorrow = (date.today() + timedelta(days=1)).isoformat()
        next_month = (date.today() + timedelta(days=30)).isoformat()
        self.run_tracker("add", "Overdue assignment", yesterday)
        self.run_tracker("add", "Due tomorrow", tomorrow)
        self.run_tracker("add", "Far away", next_month)
        result = self.run_tracker("upcoming", "--days", "7")
        self.assertEqual(result.returncode, 0)
        self.assertIn("Overdue assignment", result.stdout)
        self.assertIn("Due tomorrow", result.stdout)
        self.assertNotIn("Far away", result.stdout)

    def test_negative_days_are_rejected(self):
        result = self.run_tracker("upcoming", "--days", "-1")
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("zero or greater", result.stderr)

    def test_invalid_json_is_not_overwritten(self):
        self.data_file.write_text("broken JSON", encoding="utf-8")
        result = self.run_tracker("add", "Task", "2026-12-01")
        self.assertNotEqual(result.returncode, 0)
        self.assertEqual(self.data_file.read_text(encoding="utf-8"), "broken JSON")


if __name__ == "__main__":
    unittest.main()
