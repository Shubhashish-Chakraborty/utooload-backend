import os
from pathlib import Path
import tempfile


class Settings:
    TMP_DIR: str = tempfile.gettempdir()
    MAX_VIDEO_HEIGHT: int = 1080
    ALLOWED_HOSTS = {
        "youtube.com",
        "www.youtube.com",
        "m.youtube.com",
        "youtu.be",
        "music.youtube.com",
    }


settings = Settings()
os.makedirs(settings.TMP_DIR, exist_ok=True)

# Cookies are mounted into the container at /app/secrets/cookies.txt via
# docker-compose's volume mapping (./secrets -> /app/secrets).
_cookie_path = Path(__file__).resolve().parent.parent / "secrets" / "cookies.txt"
COOKIE_FILE_PATH = str(_cookie_path) if _cookie_path.exists() else None