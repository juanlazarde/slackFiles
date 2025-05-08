def load_downloaded_ids(path) -> set:
    return set(path.read_text().splitlines()) if path.exists() else set()


def persist_downloaded_ids(ids: set, path):
    with path.open("w") as f:
        f.writelines(f"{fid}\n" for fid in sorted(ids))
