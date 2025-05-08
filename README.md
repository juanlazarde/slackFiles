# Slack File Downloader

A robust Python CLI tool that downloads all files you have access to in your Slack workspace — from public and private channels, including Slack-hosted and external links.

---

## 📦 Features

- ✅ Download files from all joined channels
- 🗂 Organizes files by channel name
- 🔁 Skips already-downloaded files using a tracker file
- 🔗 Supports both Slack-hosted and external file URLs
- 💤 Honors Slack's rate limits (with Retry-After support)
- 🧼 Sanitizes filenames using `pathvalidate`
- 🔐 Loads config from `.env` (or environment)
- 🧪 Fully testable with unit and integration coverage
- 📊 CLI output + optional JSON summary

---

## 🚀 Installation

Clone and install dependencies:

```bash
git clone https://github.com/your-username/slack-file-downloader.git
cd slack-file-downloader
python3 -m venv .venv
source .venv/bin/activate
pip install -e .
```

Or install directly from Github:

```bash
pip install git+https://github.com/your-username/slack-file-downloader.git
```

## 🛠 Configuration

Create a `.env` file with:

```text
SLACK_API_TOKEN=xoxp-your-slack-token
DOWNLOAD_THROTTLE=0.3
DEBUG_MODE=false
```

> 💡 You must be a member of the channels you want to fetch files from.

## 🔐 Required OAuth Scopes

Make sure your Slack token has the following scopes:

- `files:read`
- `channels:history`
- `groups:history`
- `im:history`
- `mpim:history`
- `users:read`
- `remote_files:read`

Refer to [Slack’s API Scopes](https://api.slack.com/scopes) for how to attach these to your token.

### How to Create a Slack API Token

1. Go to <https://api.slack.com/apps>
2. Click Create New App > From scratch.
3. Give your app a name and select your workspace.
4. Under OAuth & Permissions, add the required scopes listed above.
5. Install the app to your workspace.
6. After installation, you’ll find your OAuth Token under

>💡 **OAuth Tokens for Your Workspace** start with `xoxp-`.
>
>💡 Make sure the app is installed by a user who is a member of all the channels you want to access.

## 🧑‍💻 Usage

```bash
slackfiles [-h] [options]
```

```text
Options:
========
--debug               Process only the first channel (for testing)
--dry-run             Simulate download without saving files
--channel <name>      Download files from a single channel
--summary-json <file> Output summary stats to a JSON file
```

## 📁 Output

- Files saved to: `slack_downloads/<channel>/filename.ext`
- Log file saved to: `slack_downloads/download.log`
- ID tracker: `.downloaded_file_ids.txt` (to skip duplicates)

## 🧪 Running Tests

```bash
python -m unittest discover tests
```

## 🧱 Development

To add dependencies:

```bash
pip install <package>
pip freeze > requirements.txt  # optional
```

To run the script directly in debug mode:

```bash
python -m slackFiles.app --debug
```

## 📄 License

MIT © 2025 Juan Lazarde
