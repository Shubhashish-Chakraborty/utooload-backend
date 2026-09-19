"""In-memory request counters for lightweight activity stats."""
from threading import Lock

_lock = Lock()
_resolve_count = 0
_number_of_downloads = 0


def increment_resolve_count() -> None:
    global _resolve_count

    with _lock:
        _resolve_count += 1


def increment_number_of_downloads() -> None:
    global _number_of_downloads
    
    with _lock:
        _number_of_downloads += 1


def get_stats() -> dict[str, int]:
    with _lock:
        return {
            "resolveCount": _resolve_count,
            "numberOfDownloads": _number_of_downloads,
        }
