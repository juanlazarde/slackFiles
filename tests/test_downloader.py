# tests/test_downloader.py
import tempfile
import unittest
from pathlib import Path

from slackFiles.downloader import get_unique_filename


class TestDownloader(unittest.TestCase):
    def test_returns_new_filename_if_not_exists(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            tmp_path = Path(tmpdir)
            result = get_unique_filename("example.txt", tmp_path)
            self.assertEqual(result.name, "example.txt")

    def test_appends_increment_if_file_exists(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            tmp_path = Path(tmpdir)
            (tmp_path / "example.txt").touch()
            (tmp_path / "example_1.txt").touch()
            result = get_unique_filename("example.txt", tmp_path)
            self.assertEqual(result.name, "example_2.txt")

    def test_raises_error_if_too_many_versions(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            tmp_path = Path(tmpdir)
            for i in range(10000):
                name = f"example_{i}.txt" if i else "example.txt"
                (tmp_path / name).touch()
            with self.assertRaises(RuntimeError):
                get_unique_filename("example.txt", tmp_path)


if __name__ == "__main__":
    unittest.main()
