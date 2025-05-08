# tests/test_tracker.py
import tempfile
import unittest
from pathlib import Path

from slackFiles.tracker import load_downloaded_ids, persist_downloaded_ids


class TestTracker(unittest.TestCase):
    def test_load_and_persist_ids(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            file_path = Path(tmpdir) / "ids.txt"
            ids_to_save = {"a", "b", "c"}

            persist_downloaded_ids(ids_to_save, file_path)
            loaded_ids = load_downloaded_ids(file_path)

            self.assertEqual(loaded_ids, ids_to_save)


if __name__ == "__main__":
    unittest.main()
