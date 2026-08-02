"""Zelretch Addon: Social Downloader.

Downloads public media supported by yt-dlp. The Addon keeps dependency checks
lazy so normal Zelretch startup is not delayed when the command is unused.
"""

from __future__ import annotations

import asyncio
import importlib.util
import json
import os
import re
import shutil
import sys
import tempfile
import time
from pathlib import Path
from typing import Optional
from urllib.parse import urlparse

from pyrogram import Client
from pyrogram.enums import ParseMode
from pyrogram.types import LinkPreviewOptions, ReplyParameters

from command import who_message, zel_command, zel_sudo
from requirements_installer import install_library

ZELRETCH_MODULE_INFO = {
    "title": "Social Downloader",
    "icon": "📥",
    "category": "Files & Media",
    "description": "Downloads public videos and audio from websites supported by yt-dlp.",
    "developer": "Siam Chowdhury",
    "github": "https://github.com/ChowdhurySiam",
    "telegram": "https://t.me/Ch0wdhury_Siam",
    "undo": ".undo (reply to the Addon output)",
}

MODULE_NAME = "SocialMediaDL"
FILENAME = os.path.basename(__file__)
URL_PATTERN = re.compile(r"https?://[^\s<>]+", re.IGNORECASE)
VIDEO_EXTENSIONS = {".mp4", ".mkv", ".webm", ".mov", ".m4v"}
AUDIO_EXTENSIONS = {".mp3", ".m4a", ".aac", ".ogg", ".opus", ".wav", ".flac"}


def _plain_edit_kwargs() -> dict:
    return {
        "parse_mode": ParseMode.DISABLED,
        "link_preview_options": LinkPreviewOptions(is_disabled=True),
    }


def _extract_url(message) -> Optional[str]:
    candidates = [
        getattr(message, "text", None),
        getattr(message, "caption", None),
    ]
    replied = getattr(message, "reply_to_message", None)
    if replied is not None:
        candidates.extend(
            [getattr(replied, "text", None), getattr(replied, "caption", None)]
        )

    for candidate in candidates:
        if not candidate:
            continue
        match = URL_PATTERN.search(str(candidate))
        if not match:
            continue
        url = match.group(0).rstrip(".,;:!?)]}\"'")
        parsed = urlparse(url)
        if parsed.scheme in {"http", "https"} and parsed.netloc:
            return url
    return None


def _max_download_bytes() -> int:
    try:
        megabytes = int(os.environ.get("SOCIAL_DL_MAX_MB", "500"))
    except ValueError:
        megabytes = 500
    megabytes = max(25, min(1900, megabytes))
    return megabytes * 1024 * 1024


def _download_timeout() -> int:
    try:
        seconds = int(os.environ.get("SOCIAL_DL_TIMEOUT", "900"))
    except ValueError:
        seconds = 900
    return max(60, min(3600, seconds))


def _find_downloaded_media(directory: Path) -> Optional[Path]:
    ignored_suffixes = {".json", ".part", ".ytdl", ".temp"}
    candidates = [
        path
        for path in directory.rglob("*")
        if path.is_file()
        and path.suffix.lower() not in ignored_suffixes
        and not path.name.endswith((".info.json", ".description"))
    ]
    if not candidates:
        return None
    return max(candidates, key=lambda path: path.stat().st_size)


def _read_metadata(directory: Path) -> dict:
    for path in directory.rglob("*.info.json"):
        try:
            value = json.loads(path.read_text(encoding="utf-8"))
            if isinstance(value, dict):
                return value
        except (OSError, UnicodeDecodeError, json.JSONDecodeError):
            continue
    return {}


async def _ensure_yt_dlp() -> None:
    if importlib.util.find_spec("yt_dlp") is not None:
        return
    installed = await asyncio.to_thread(install_library, "yt-dlp")
    if not installed or importlib.util.find_spec("yt_dlp") is None:
        raise RuntimeError("yt-dlp could not be installed. Rebuild Zelretch with the latest main package.")


async def _edit_status(message, text: str) -> None:
    try:
        await message.edit(text, **_plain_edit_kwargs())
    except Exception:
        pass


async def _run_yt_dlp(url: str, output_directory: Path, status_message) -> tuple[Path, dict]:
    max_bytes = _max_download_bytes()
    max_megabytes = max_bytes // (1024 * 1024)
    output_template = str(output_directory / "%(title).100s-%(id)s.%(ext)s")

    command = [
        sys.executable,
        "-m",
        "yt_dlp",
        "--no-playlist",
        "--newline",
        "--progress",
        "--progress-template",
        "download:%(progress._percent_str)s|%(progress._speed_str)s|%(progress._eta_str)s",
        "--restrict-filenames",
        "--no-mtime",
        "--write-info-json",
        "--no-write-comments",
        "--max-filesize",
        f"{max_megabytes}M",
        "-o",
        output_template,
    ]

    if shutil.which("ffmpeg"):
        command.extend(
            [
                "-f",
                "bv*[height<=1080]+ba/b[height<=1080]/b",
                "--merge-output-format",
                "mp4",
            ]
        )
    else:
        command.extend(["-f", "b[height<=1080]/b"])

    cookie_file = (os.environ.get("YTDLP_COOKIE_FILE") or "").strip()
    if cookie_file and Path(cookie_file).is_file():
        command.extend(["--cookies", cookie_file])

    command.append(url)
    process = await asyncio.create_subprocess_exec(
        *command,
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.STDOUT,
    )

    recent_lines: list[str] = []
    last_update = 0.0

    async def consume_output() -> int:
        nonlocal last_update
        assert process.stdout is not None
        while True:
            raw = await process.stdout.readline()
            if not raw:
                break
            line = raw.decode("utf-8", errors="replace").strip()
            if not line:
                continue
            recent_lines.append(line)
            del recent_lines[:-12]
            if line.startswith("download:"):
                now = time.monotonic()
                if now - last_update >= 3:
                    last_update = now
                    parts = line[len("download:") :].split("|", 2)
                    percent = parts[0].strip() if parts else "—"
                    speed = parts[1].strip() if len(parts) > 1 else "—"
                    eta = parts[2].strip() if len(parts) > 2 else "—"
                    await _edit_status(
                        status_message,
                        f"Downloading media…\nProgress: {percent}\nSpeed: {speed}\nETA: {eta}",
                    )
        return await process.wait()

    try:
        return_code = await asyncio.wait_for(consume_output(), timeout=_download_timeout())
    except asyncio.TimeoutError as exc:
        process.kill()
        await process.wait()
        raise RuntimeError("The download timed out before completion.") from exc

    if return_code != 0:
        diagnostic = "\n".join(recent_lines[-5:]) or "yt-dlp exited without details."
        if "Sign in" in diagnostic or "cookies" in diagnostic.lower():
            diagnostic += "\nThis source may require a YTDLP_COOKIE_FILE secret."
        raise RuntimeError(diagnostic[-900:])

    media_path = _find_downloaded_media(output_directory)
    if media_path is None:
        raise RuntimeError("The source returned no downloadable media file.")
    if media_path.stat().st_size > max_bytes:
        raise RuntimeError(
            f"The downloaded file exceeds the configured {max_megabytes} MB limit."
        )
    return media_path, _read_metadata(output_directory)


async def _send_media(client, source_message, status_message, media_path: Path, metadata: dict) -> None:
    title = str(metadata.get("title") or media_path.stem).strip()
    uploader = str(metadata.get("uploader") or "").strip()
    caption_lines = [title[:800]]
    if uploader:
        caption_lines.append(f"Source: {uploader[:120]}")
    caption = "\n".join(caption_lines)

    reply_id = None
    replied = getattr(source_message, "reply_to_message", None)
    if replied is not None:
        reply_id = getattr(replied, "id", None)
    reply_parameters = ReplyParameters(message_id=reply_id) if reply_id else None

    await _edit_status(status_message, "Download complete. Uploading to Telegram…")
    extension = media_path.suffix.lower()

    try:
        if extension in VIDEO_EXTENSIONS:
            await client.send_video(
                source_message.chat.id,
                video=str(media_path),
                caption=caption,
                supports_streaming=True,
                reply_parameters=reply_parameters,
                parse_mode=ParseMode.DISABLED,
            )
        elif extension in AUDIO_EXTENSIONS:
            await client.send_audio(
                source_message.chat.id,
                audio=str(media_path),
                caption=caption,
                reply_parameters=reply_parameters,
                parse_mode=ParseMode.DISABLED,
            )
        else:
            await client.send_document(
                source_message.chat.id,
                document=str(media_path),
                caption=caption,
                reply_parameters=reply_parameters,
                parse_mode=ParseMode.DISABLED,
            )
    except Exception:
        # Telegram may reject an otherwise valid video container. Sending the
        # same file as a document preserves the download instead of failing.
        await client.send_document(
            source_message.chat.id,
            document=str(media_path),
            caption=caption,
            reply_parameters=reply_parameters,
            parse_mode=ParseMode.DISABLED,
        )


@Client.on_message(
    zel_command(["socialdl", "sdl", "tt"], MODULE_NAME, FILENAME, "[url/reply]")
    & zel_sudo()
)
async def social_download(client, message):
    source_message = message
    url = _extract_url(source_message)
    status_message = await who_message(client, message)

    if not url:
        await _edit_status(
            status_message,
            "Send .socialdl <URL>, or reply to a message containing a public media URL.",
        )
        return

    await _edit_status(status_message, "Preparing the social-media downloader…")

    try:
        await _ensure_yt_dlp()
        Path("temp").mkdir(parents=True, exist_ok=True)
        with tempfile.TemporaryDirectory(prefix="socialdl_", dir="temp") as directory:
            media_path, metadata = await _run_yt_dlp(
                url, Path(directory), status_message
            )
            await _send_media(
                client, source_message, status_message, media_path, metadata
            )
        try:
            await status_message.delete()
        except Exception:
            pass
    except Exception as exc:
        detail = re.sub(r"\s+", " ", str(exc)).strip()
        await _edit_status(
            status_message,
            f"Social download failed.\n{detail[:900] or 'Unknown downloader error.'}",
        )
