"""Small, dependency-free helpers: URL validation + filename sanitizing."""
import re
from urllib.parse import urlparse

from core.config import settings


def is_youtube_url(url: str) -> bool:
    """True only for youtube.com / youtu.be family of hosts."""
    try:
        host = (urlparse(str(url)).hostname or "").lower()
    except ValueError:
        return False
    return any(host == h or host.endswith("." + h) for h in settings.ALLOWED_HOSTS)


def sanitize_filename(name: str) -> str:
    """Strip anything that isn't filesystem/URL-safe, cap length."""
    name = re.sub(r"[^\w\s\-\.]", "", name or "").strip()
    name = re.sub(r"\s+", "_", name)
    return name[:100] or "utooload_download"