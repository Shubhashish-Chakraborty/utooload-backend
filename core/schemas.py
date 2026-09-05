"""Pydantic request/response models shared across routers."""
from typing import Literal, Optional

from pydantic import BaseModel, HttpUrl


class ResolveRequest(BaseModel):
    url: HttpUrl


class FormatOption(BaseModel):
    format_id: str
    ext: Optional[str] = None
    resolution: Optional[str] = None
    abr: Optional[float] = None
    filesize_approx: Optional[int] = None
    note: Optional[str] = None


class ResolveResponse(BaseModel):
    title: Optional[str] = None
    thumbnail: Optional[str] = None
    duration: Optional[int] = None
    formats: list[FormatOption] = []


class DownloadRequest(BaseModel):
    url: HttpUrl
    mode: Literal["audio", "video"]
    # Only used when mode == "video". Ignored for audio.
    quality: Literal["360p", "480p", "720p", "best"] = "720p"