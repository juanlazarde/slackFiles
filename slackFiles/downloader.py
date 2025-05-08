import logging
import os
import time
from pathlib import Path
from typing import Optional

import requests
import requests.exceptions
from pathvalidate import sanitize_filename

from .config import get_config

config = get_config()
DOWNLOAD_DIR = config["DOWNLOAD_DIR"]
HEADERS = config["HEADERS"]
MAX_RETRIES = 3


def rate_limit_sleep(response: Optional[requests.Response] = None, default: float = 1.0) -> None:
    time.sleep(int(response.headers.get("Retry-After", default)) if response else default)


def get_unique_filename(base: str, directory: Path) -> Path:
    stem, ext = os.path.splitext(base)
    for i in range(10000):
        filename = f"{stem}_{i}{ext}" if i else base
        filepath = directory / filename
        if not filepath.exists():
            return filepath
    raise RuntimeError(f"Too many versions of '{base}' in {directory}")


def download_file(file_info: dict, channel_name: str, logger: logging.Logger) -> None:
    url = file_info.get("url_private_download") or file_info.get("url_private") or file_info.get("external_url")
    if not url:
        logger.warning(f"⚠️  No downloadable URL for file {file_info.get('id')}")
        return

    base = sanitize_filename(file_info.get("name", file_info["id"]), replacement_text="_")
    channel_dir = DOWNLOAD_DIR / channel_name
    channel_dir.mkdir(parents=True, exist_ok=True)

    try:
        filepath = get_unique_filename(base, channel_dir)
    except RuntimeError as e:
        logger.warning(f"⚠️ {e}")
        return
    filename = filepath.name

    for attempt in range(1, MAX_RETRIES + 1):
        try:
            headers = HEADERS if "slack.com" in url else {}
            resp = requests.get(url, headers=headers, stream=True, timeout=10)
            if resp.status_code == 200:
                with open(filepath, "wb") as f:
                    for chunk in resp.iter_content(1024):
                        f.write(chunk)
                logger.info(f"⬇️ {filename} | #{channel_name} | ID: {file_info.get('id')} | URL: {url}")
                break
            elif resp.status_code == 429:
                logger.warning(f"⚠️ Rate limited. Retrying in {attempt} seconds...")
                rate_limit_sleep(resp, attempt)
                continue
            elif resp.status_code == 404:
                logger.warning(f"⚠️ File not found: {filename} (404)")
                break
            elif resp.status_code == 403:
                logger.warning(f"⚠️ Permission denied: {filename} (403)")
                break
            elif resp.status_code == 500:
                logger.warning(f"⚠️ Server error: {filename} (500)")
            elif resp.status_code == 503:
                logger.warning(f"⚠️ Service unavailable: {filename} (503)")
                break
            elif resp.status_code == 408:
                logger.warning(f"⚠️ Request timeout: {filename} (408)")
                break
            elif resp.status_code == 400:
                logger.warning(f"⚠️ Bad request: {filename} (400)")
                break
            elif resp.status_code == 401:
                logger.warning(f"⚠️ Unauthorized: {filename} (401)")
                break
            elif resp.status_code == 429:
                logger.warning(f"⚠️ Too many requests: {filename} (429)")
            else:
                logger.warning(f"⚠️ Failed ({resp.status_code}): {filename}")
                break
        except requests.exceptions.RequestException as e:
            logger.warning(f"⚠️ Request error: {filename} | Attempt {attempt}/{MAX_RETRIES}: {e}")
            if attempt == MAX_RETRIES:
                logger.error(f"❌ Failed to download {filename} after {MAX_RETRIES} attempts.")
        time.sleep(2**attempt)  # Exponential backoff
    else:
        logger.error(f"❌ Failed to download {url} after {MAX_RETRIES} attempts.")
