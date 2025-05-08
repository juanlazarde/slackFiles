import unittest
from unittest.mock import MagicMock, patch

from slackFiles import slack_api


class TestSlackAPI(unittest.TestCase):
    @patch("slackFiles.slack_api.requests.get")
    def test_get_all_channels_success(self, mock_get):
        mock_response = MagicMock()
        mock_response.json.return_value = {
            "ok": True,
            "channels": [
                {"id": "C1", "name": "general", "is_member": True},
                {"id": "C2", "name": "random", "is_member": False},
            ],
            "response_metadata": {"next_cursor": ""},
        }
        mock_get.return_value = mock_response

        result = slack_api.get_all_channels()
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0]["name"], "general")

    @patch("slackFiles.slack_api.requests.get")
    def test_fetch_files_from_channel(self, mock_get):
        mock_response = MagicMock()
        mock_response.json.return_value = {
            "ok": True,
            "messages": [
                {
                    "files": [{"id": "F123", "name": "file.txt", "url_private": "https://..."}],
                    "attachments": [{"title": "external file", "original_url": "https://example.com"}],
                }
            ],
            "response_metadata": {"next_cursor": ""},
        }
        mock_get.return_value = mock_response

        result = slack_api.fetch_files_from_channel("C123")
        self.assertEqual(len(result), 2)
        self.assertTrue(any(f["id"] == "F123" for f in result))
        self.assertTrue(any("external_url" in f for f in result))


if __name__ == "__main__":
    unittest.main()
