# Central config for the Utooload backend.

import os
import tempfile


class Settings:
    TMP_DIR: str = tempfile.gettempdir()
    MAX_VIDEO_HEIGHT: int = 720
    ALLOWED_HOSTS = {
        "youtube.com",
        "www.youtube.com",
        "m.youtube.com",
        "youtu.be",
        "music.youtube.com",
    }


settings = Settings()
os.makedirs(settings.TMP_DIR, exist_ok=True)