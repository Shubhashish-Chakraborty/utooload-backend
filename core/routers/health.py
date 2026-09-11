from fastapi import APIRouter
from core.config import COOKIE_FILE_PATH, settings
import os

router = APIRouter()


@router.get("/health")
def health():
    return {"status": "ok", "service": "utooload-backend"}

@router.get("/debug-cookies")
def debug_cookies():
    """TEMPORARY diagnostic endpoint — remove once cookies are confirmed
    working. Never returns actual cookie contents, only whether they
    loaded and how big the file is."""
    env_set = bool(settings.YTDLP_COOKIES_B64)
    file_exists = bool(COOKIE_FILE_PATH) and os.path.exists(COOKIE_FILE_PATH)
    file_size = os.path.getsize(COOKIE_FILE_PATH) if file_exists else 0
    return {
        "cookie_env_var_set": env_set,
        "cookie_file_written": file_exists,
        "cookie_file_size_bytes": file_size,
    }