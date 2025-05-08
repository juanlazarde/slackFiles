# config.py

import os
from functools import lru_cache
from pathlib import Path

import requests
from dotenv import load_dotenv

load_dotenv()


@lru_cache()
def get_config():
    token = os.getenv("SLACK_API_TOKEN")
    if not token:
        raise EnvironmentError("Missing SLACK_API_TOKEN")

    headers = {"Authorization": f"Bearer {token}"}
    base_url = os.getenv("SLACK_API_BASE_URL", "https://slack.com/api")

    try:
        resp = requests.get(f"{base_url}/auth.test", headers=headers, timeout=10)
        resp.raise_for_status()
        if not resp.json().get("ok"):
            raise EnvironmentError("SLACK_TOKEN is invalid or missing required scopes")
    except Exception as e:
        raise EnvironmentError(f"SLACK_TOKEN validation failed: {e}")

    return {
        "SLACK_TOKEN": token,
        "HEADERS": headers,
        "SLACK_API_BASE_URL": base_url,
        "DOWNLOAD_DIR": Path(os.getenv("DOWNLOAD_DIR", "slack_downloads")),
        "ID_TRACK_FILE": Path("slack_downloads") / ".downloaded_file_ids.txt",
        "LOG_FILE": Path("slack_downloads") / "download.log",
        "MAX_API_ITERATIONS": 100,
        "DOWNLOAD_THROTTLE": float(os.getenv("DOWNLOAD_THROTTLE", "0.2")),
        "DEBUG_MODE": os.getenv("DEBUG_MODE", "false").lower() == "true",
    }
