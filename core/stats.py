"""In-memory request counters for lightweight activity stats."""
from calendar import month_name
from datetime import datetime, timezone
from threading import Lock

_lock = Lock()
_resolve_count = 0
_number_of_downloads = 0
_last_resolved: datetime | None = None
_last_updated: datetime | None = None


def _format_month_year(value: datetime | None) -> str | None:
    if value is None:
        return None
    return f"{month_name[value.month]} {value.year}"


def increment_resolve_count() -> None:
    global _resolve_count, _last_resolved, _last_updated

    with _lock:
        _resolve_count += 1
        _last_resolved = datetime.now(timezone.utc)
        _last_updated = _last_resolved


def increment_number_of_downloads() -> None:
    global _number_of_downloads, _last_updated

    with _lock:
        _number_of_downloads += 1
        _last_updated = datetime.now(timezone.utc)


def get_stats() -> dict[str, int | str | None]:
    with _lock:
        return {
            "resolveCount": _resolve_count,
            "numberOfDownloads": _number_of_downloads,
            "lastResolved": _format_month_year(_last_resolved),
            "lastUpdated": _format_month_year(_last_updated),
        }
