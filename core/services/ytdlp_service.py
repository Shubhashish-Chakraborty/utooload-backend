"""
Thin wrapper around yt-dlp for the two things this backend needs:
  1. resolve_formats  -> metadata + available formats, no download
  2. download_media    -> actually fetch + (if needed) transcode, return a
                           local file path ready to stream back to the client

Design note: everything here runs SYNCHRONOUSLY inside a single request.
That's deliberate — see the README for why the async job-queue pattern
doesn't fit a serverless deployment target well, and how request duration
limits factor into MAX_VIDEO_HEIGHT.
"""

import os
import uuid
from typing import Literal

import yt_dlp

from core.config import settings
from core.services.ffmpeg_setup import get_ffmpeg_path
from core.utils.validators import sanitize_filename

QUALITY_HEIGHT_MAP = {
    "360p": 360,
    "480p": 480,
    "720p": 720,
    "best": None,
}


def resolve_formats(url: str) -> dict:
    ydl_opts = {
        "quiet": True,
        "no_warnings": True,
        "skip_download": True,
        "noplaylist": True,
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=False)

    formats = []
    for f in info.get("formats", []):
        formats.append(
            {
                "format_id": f.get("format_id"),
                "ext": f.get("ext"),
                "resolution": f.get("resolution"),
                "abr": f.get("abr"),
                "filesize_approx": f.get("filesize") or f.get("filesize_approx"),
                "note": f.get("format_note"),
            }
        )

    return {
        "title": info.get("title"),
        "thumbnail": info.get("thumbnail"),
        "duration": info.get("duration"),
        "formats": formats,
    }


def download_media(
    url: str,
    mode: Literal["audio", "video"],
    quality: str = "720p",
) -> tuple[str, str, str]:
    """
    Downloads (and transcodes if needed) the requested media.
    Returns (file_path, download_filename, media_type).
    Caller is responsible for deleting file_path after the response is sent.
    """
    job_id = uuid.uuid4().hex
    out_template = os.path.join(settings.TMP_DIR, f"{job_id}.%(ext)s")
    ffmpeg_path = get_ffmpeg_path()

    if mode == "audio":
        expected_ext = "mp3"
        media_type = "audio/mpeg"
        ydl_opts = {
            "format": "bestaudio/best",
            "outtmpl": out_template,
            "ffmpeg_location": ffmpeg_path,
            "postprocessors": [
                {
                    "key": "FFmpegExtractAudio",
                    "preferredcodec": "mp3",
                    "preferredquality": "192",
                }
            ],
            "noplaylist": True,
            "quiet": True,
            "no_warnings": True,
        }
    else:
        height_cap = QUALITY_HEIGHT_MAP.get(quality, settings.MAX_VIDEO_HEIGHT)
        # Never let a client request above our server-side ceiling, even if
        # they pass "best" — keeps runtime/file-size predictable on a
        # function-duration-limited platform.
        if height_cap is None or height_cap > settings.MAX_VIDEO_HEIGHT:
            height_cap = settings.MAX_VIDEO_HEIGHT

        fmt = f"bestvideo[height<={height_cap}]+bestaudio/best[height<={height_cap}]"
        expected_ext = "mp4"
        media_type = "video/mp4"
        ydl_opts = {
            "format": fmt,
            "outtmpl": out_template,
            "ffmpeg_location": ffmpeg_path,
            "merge_output_format": "mp4",
            "noplaylist": True,
            "quiet": True,
            "no_warnings": True,
        }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=True)

    file_path = os.path.join(settings.TMP_DIR, f"{job_id}.{expected_ext}")
    if not os.path.exists(file_path):
        raise FileNotFoundError(
            "Expected output file was not found after yt-dlp finished — "
            "the source format may not have matched what was requested."
        )

    safe_title = sanitize_filename(info.get("title", "utooload_download"))
    filename = f"{safe_title}.{expected_ext}"
    return file_path, filename, media_type