import unittest
from unittest.mock import MagicMock, patch

from slackFiles import app


class TestAppIntegration(unittest.TestCase):
    @patch("slackFiles.app.get_all_channels")
    @patch("slackFiles.app.fetch_files_from_channel")
    @patch("slackFiles.app.download_file")
    def test_main_with_mocked_components(self, mock_download, mock_fetch_files, mock_get_channels):
        mock_get_channels.return_value = [
            {"id": "C1", "name": "general"},
        ]
        mock_fetch_files.return_value = [{"id": "F123", "name": "test.txt", "url_private": "https://..."}]

        with (
            patch("slackFiles.app.load_downloaded_ids", return_value=set()),
            patch("slackFiles.app.persist_downloaded_ids") as mock_save,
            patch("slackFiles.app.time.sleep"),
            patch("slackFiles.app.parse_args") as mock_args,
        ):

            mock_args.return_value = MagicMock(debug=True, dry_run=True, channel=None, summary_json=None)
            app.main()

            mock_get_channels.assert_called_once()
            mock_fetch_files.assert_called_once_with("C1")
            mock_download.assert_not_called()  # dry-run
            mock_save.assert_called_once()


if __name__ == "__main__":
    unittest.main()
