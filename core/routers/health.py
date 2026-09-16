from fastapi import APIRouter
import os
import shutil

import yt_dlp

from core.config import COOKIE_FILE_PATH

router = APIRouter()


@router.get("/health")
def health():
    return {"status": "ok", "service": "utooload-backend"}


@router.get("/debug-cookies")
def debug_cookies():
    """TEMPORARY diagnostic endpoint."""
    file_exists = bool(COOKIE_FILE_PATH) and os.path.exists(COOKIE_FILE_PATH)
    file_size = os.path.getsize(COOKIE_FILE_PATH) if file_exists else 0

    first_line = None
    cookie_line_count = 0
    if file_exists:
        with open(COOKIE_FILE_PATH, "r", errors="replace") as f:
            lines = f.readlines()
        first_line = lines[0].strip() if lines else None
        cookie_line_count = sum(
            1 for line in lines if line.strip() and not line.strip().startswith("#")
        )

    return {
        "cookie_file_written": file_exists,
        "cookie_file_size_bytes": file_size,
        "cookie_file_first_line": first_line,
        "cookie_line_count": cookie_line_count,
        "yt_dlp_version": yt_dlp.version.__version__,
        "deno_found_on_path": shutil.which("deno") is not None,
    }