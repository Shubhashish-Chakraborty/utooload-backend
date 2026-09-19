import os

from fastapi import APIRouter, HTTPException
from fastapi.responses import FileResponse
from starlette.background import BackgroundTask
import yt_dlp

from core.schemas import DownloadRequest
from core.services.ytdlp_service import download_media
from core.stats import increment_number_of_downloads
from core.utils.validators import is_youtube_url

router = APIRouter()


def _cleanup(path: str) -> None:
    """Runs after the response is fully sent — keeps /tmp from filling up
    across invocations on the same warm function instance."""
    try:
        if os.path.exists(path):
            os.remove(path)
    except OSError:
        pass


@router.post("/download")
def download(payload: DownloadRequest):
    increment_number_of_downloads()

    url = str(payload.url)

    if not is_youtube_url(url):
        raise HTTPException(status_code=400, detail="Only YouTube URLs are supported.")

    try:
        file_path, filename, media_type = download_media(url, payload.mode, payload.quality)
    except yt_dlp.utils.DownloadError as e:
        raise HTTPException(status_code=422, detail=f"Couldn't download this video: {e}")
    except FileNotFoundError as e:
        raise HTTPException(status_code=500, detail=str(e))
    except Exception:
        raise HTTPException(status_code=500, detail="Unexpected error while processing the video.")

    return FileResponse(
        path=file_path,
        media_type=media_type,
        filename=filename,
        background=BackgroundTask(_cleanup, file_path),
    )
