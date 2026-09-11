"""
Central config for the Utooload backend.

Kept deliberately tiny — everything that changes between local dev and
Vercel goes through here, so there's one place to look when something's
off (e.g. temp dir, quality caps).
"""
import os
import tempfile


class Settings:
    # Vercel only allows writes to /tmp — tempfile.gettempdir() resolves
    # correctly both locally (Linux/Mac) and on Vercel's runtime.
    TMP_DIR: str = tempfile.gettempdir()

    # Hard cap on video height. Keeps file size + processing time predictable,
    # which matters a lot on a platform with a function duration ceiling.
    MAX_VIDEO_HEIGHT: int = 720

    # Only allow these hosts. Keeps this a "YouTube saver", not a generic
    # link-to-file proxy.
    ALLOWED_HOSTS = {
        "youtube.com",
        "www.youtube.com",
        "m.youtube.com",
        "youtu.be",
        "music.youtube.com",
    }

    # Base64-encoded contents of a Netscape-format cookies.txt, set as a
    # Vercel env var. Needed because cloud/datacenter IPs (like Vercel's)
    # get YouTube's "Sign in to confirm you're not a bot" check far more
    # often than residential IPs do. Never commit the raw cookies file.
    YTDLP_COOKIES_B64: str = os.environ.get("YTDLP_COOKIES_B64", "")


settings = Settings()
os.makedirs(settings.TMP_DIR, exist_ok=True)

# Decode cookies once per cold start (not per-request) and write to /tmp.
COOKIE_FILE_PATH = os.path.join(settings.TMP_DIR, "yt_cookies.txt")
if settings.YTDLP_COOKIES_B64:
    import base64

    try:
        with open(COOKIE_FILE_PATH, "wb") as f:
            f.write(base64.b64decode(settings.YTDLP_COOKIES_B64))
    except Exception:
        # If decoding fails, fall back to cookie-less requests rather than
        # crashing the whole function on import.
        COOKIE_FILE_PATH = None
else:
    COOKIE_FILE_PATH = None
