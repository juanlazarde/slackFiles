# slack_api.py

import requests

from .config import get_config
from .downloader import rate_limit_sleep
from .logger import logger

config = get_config()
SLACK_API_BASE_URL = config["SLACK_API_BASE_URL"]
HEADERS = config["HEADERS"]
MAX_API_ITERATIONS = config["MAX_API_ITERATIONS"]


def get_all_channels() -> list:
    channels, cursor = [], None
    iterations = 0

    while iterations < MAX_API_ITERATIONS:
        params = {
            "types": "public_channel,private_channel",
            "limit": 200,
            **({"cursor": cursor} if cursor else {}),
        }
        resp = requests.get(f"{SLACK_API_BASE_URL}/conversations.list", headers=HEADERS, params=params, timeout=10)
        data = resp.json()

        if not data.get("ok"):
            logger.error(f"❌ Failed to fetch channels: {data.get('error')}")
            break

        channels.extend(ch for ch in data["channels"] if ch.get("is_member"))
        cursor = data.get("response_metadata", {}).get("next_cursor")
        if not cursor:
            break

        iterations += 1
        rate_limit_sleep(resp)

    if iterations == MAX_API_ITERATIONS:
        logger.warning(f"⚠️ Exited channels due to API iteration limit: {iterations}.")

    return channels


def fetch_files_from_channel(channel_id: str) -> list:
    files, seen_ids, cursor = [], set(), None
    iterations = 0

    while iterations < MAX_API_ITERATIONS:
        params = {"channel": channel_id, "limit": 200, **({"cursor": cursor} if cursor else {})}
        resp = requests.get(f"{SLACK_API_BASE_URL}/conversations.history", headers=HEADERS, params=params, timeout=10)
        data = resp.json()

        if not data.get("ok"):
            logger.error(f"❌ Error fetching messages from {channel_id}: {data.get('error')}")
            break

        for msg in data.get("messages", []):
            for f in msg.get("files", []):
                if f["id"] not in seen_ids:
                    seen_ids.add(f["id"])
                    files.append(f)
            for a in msg.get("attachments", []):
                url = a.get("original_url") or a.get("title_link")
                if url and url not in seen_ids:
                    seen_ids.add(url)
                    files.append({"id": url, "name": a.get("title", "external_link"), "external_url": url})

        cursor = data.get("response_metadata", {}).get("next_cursor")
        if not cursor:
            break

        iterations += 1
        rate_limit_sleep(resp)

    if iterations == MAX_API_ITERATIONS:
        logger.warning(f"⚠️ Exited fetching files in channel {channel_id} due to API iteration limit: {iterations}.")

    return files
