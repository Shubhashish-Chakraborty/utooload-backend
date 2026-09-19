import logging

from fastapi import APIRouter, HTTPException
import yt_dlp

from core.schemas import ResolveRequest, ResolveResponse
from core.services.ytdlp_service import resolve_formats
from core.stats import increment_resolve_count
from core.utils.validators import is_youtube_url

logger = logging.getLogger("uvicorn.error")
router = APIRouter()


@router.post("/resolve", response_model=ResolveResponse)
def resolve(payload: ResolveRequest):
    increment_resolve_count()

    url = str(payload.url)

    if not is_youtube_url(url):
        raise HTTPException(status_code=400, detail="Only YouTube URLs are supported.")

    try:
        data = resolve_formats(url)
    except yt_dlp.utils.DownloadError as e:
        raise HTTPException(status_code=422, detail=f"Couldn't read this video: {e}")
    except Exception:
        logger.exception("Unexpected error in /api/resolve")  # logs!
        raise HTTPException(status_code=500, detail="Unexpected error while resolving the video.")

    return data
