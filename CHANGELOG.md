# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/)
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

---

## [0.2.0] - 2025-05-07

### Added

- CLI support for `--debug`, `--dry-run`, `--channel`, `--summary-json`
- Full logging system with RotatingFileHandler
- File deduplication via `.downloaded_file_ids.txt`
- Filename sanitization with `pathvalidate`
- Exponential retry with `requests` on download errors
- Configurable output directory via `DOWNLOAD_DIR`
- Slack API token validation on startup (`auth.test`)
- Retry-after support for rate-limiting
- API iteration limits to prevent infinite loops
- Unit tests for `slack_api.py`, `downloader.py`, and integration
- Type hints and `py.typed` for type checker compatibility

## [0.1.0] - 2025-05-06

### Added

- Initial Slack file downloader script
- Download from all channels using Slack API
- Basic logging and download logic
- CLI install support via `pyproject.toml`
