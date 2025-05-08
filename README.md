# Slack File Downloader

A robust Python CLI tool to download all files from your Slack workspace — across all public and private channels you are a member of.

---

## 📦 Features

- ✅ Download files from all channels
- 🗂 Organizes files by channel name
- 🔁 Skips previously downloaded files (tracked by ID)
- 📎 Supports Slack-hosted + external file URLs
- 💤 Honors Slack's rate limits
- 🧹 Sanitizes filenames
- 🔐 Loads config from `.env`
- 🧪 Modular and testable design

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

Alternatively, if hosted in Github:

```bash
pip install git+https://github.com/your-username/slack-file-downloader.git
```

Create an `.env` file with:

```bash
SLACK_API_TOKEN=xoxp-your-slack-token
DOWNLOAD_THROTTLE=0.3
DEBUG_MODE=false
```

## Usage

```bash
slackfiles [options]

Options:
========
--debug               Process only the first channel (for testing)
--dry-run             Simulate download without saving files
--channel <name>      Download files from a single channel
--summary-json <file> Output summary stats to a JSON file
```

## Output

Files are saved to:

```bash
slack_downloads/<channel_name>/filename.ext
```

Log file is saved as:

```bash
slack_downloads/download.log
```

## Running Tests

```bash
python -m unittest discover tests
```

## Development

To add dependencies:

```bash
pip install <package>
pip freeze > requirements.txt  # optional
```

To run the script directly in debug mode:

```bash
python -m slackFiles.app --debug
```

## 🔐 Required OAuth Scopes

Make sure your Slack token has the following scopes:

- `files:read`
- `channels:history`
- `groups:history`
- `im:history`
- `mpim:history`
- `users:read`
- `remote_files:read`

## License

MIT © Juan Lazarde
