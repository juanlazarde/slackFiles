import argparse
import json
import time

from .config import get_config
from .downloader import download_file
from .logger import logger
from .slack_api import fetch_files_from_channel, get_all_channels
from .tracker import load_downloaded_ids, persist_downloaded_ids

config = get_config()
DOWNLOAD_THROTTLE = config["DOWNLOAD_THROTTLE"]
ID_TRACK_FILE = config["ID_TRACK_FILE"]


def parse_args():
    parser = argparse.ArgumentParser(description="Slack File Downloader")
    parser.add_argument("--debug", action="store_true", help="Limit to the first channel")
    parser.add_argument("--dry-run", action="store_true", help="Simulate downloads without saving files")
    parser.add_argument("--channel", type=str, help="Download from only one specific channel by name")
    parser.add_argument("--summary-json", type=str, help="Path to write a summary report as JSON")
    return parser.parse_args()


def main():
    start_time = time.time()
    total_downloaded = 0
    total_skipped = 0

    args = parse_args()
    downloaded_ids = load_downloaded_ids(ID_TRACK_FILE)
    new_ids = set()

    logger.info("Fetching channels...")
    channels = get_all_channels()

    if args.channel:
        channels = [c for c in channels if c["name"] == args.channel]
        if not channels:
            msg = f"❌ No channel found matching --channel={args.channel}"
            print(msg)
            logger.warning(msg)
            return

    if args.debug:
        channels = channels[:1]
        logger.debug("Debug mode: only first channel used.")

    for ch in channels:
        try:
            logger.info(f"Scanning #{ch['name']} ({ch['id']})...")
            files = fetch_files_from_channel(ch["id"])
            logger.info(f"Found {len(files)} file(s).")

            for i, f in enumerate(files, 1):
                if f["id"] in downloaded_ids:
                    logger.debug(f"Skipped: {f.get('name', f['id'])} (already downloaded)")
                    total_skipped += 1
                    continue
                else:
                    total_downloaded += 1

                logger.info(f"Downloading {i}/{len(files)}: {f.get('name', f['id'])}")

                if not args.dry_run:
                    download_file(f, ch["name"], logger)

                new_ids.add(f["id"])
                logger.debug(f"Sleeping for {DOWNLOAD_THROTTLE:.2f} seconds")
                time.sleep(DOWNLOAD_THROTTLE)
        except Exception as e:
            logger.warning(f"Skipping channel #{ch['name']} due to error: {e}")
            continue

    persist_downloaded_ids(downloaded_ids | new_ids, ID_TRACK_FILE)

    if args.summary_json:
        summary = {
            "downloaded": total_downloaded,
            "skipped": total_skipped,
            "duration": round(time.time() - start_time, 2),
            "channels_processed": len(channels),
        }
        with open(args.summary_json, "w") as f:
            json.dump(summary, f, indent=2)
        logger.info(f"📄 Summary written to: {args.summary_json}")


if __name__ == "__main__":
    main()
