"""Zelretch Addon: Text to Speech.

Creates a Telegram-compatible OGG/Opus voice note. The Google TTS request and
FFmpeg conversion run outside the event loop so other commands remain responsive.
"""

from __future__ import annotations

import asyncio
import importlib.util
import os
import shutil
import tempfile
from pathlib import Path
from typing import Optional

from pyrogram import Client
from pyrogram.enums import ParseMode
from pyrogram.types import LinkPreviewOptions, ReplyParameters

from command import who_message, zel_command, zel_sudo
from requirements_installer import install_library

ZELRETCH_MODULE_INFO = {
    "title": "Text to Speech",
    "icon": "🔊",
    "category": "Files & Media",
    "description": "Converts supplied or replied English text into a Telegram voice note.",
    "developer": "Siam Chowdhury",
    "github": "https://github.com/ChowdhurySiam",
    "telegram": "https://t.me/Ch0wdhury_Siam",
    "undo": ".undo (reply to the Addon output)",
}

MODULE_NAME = "TextToVoice"
FILENAME = os.path.basename(__file__)


def _plain_edit_kwargs() -> dict:
    return {
        "parse_mode": ParseMode.DISABLED,
        "link_preview_options": LinkPreviewOptions(is_disabled=True),
    }


def _extract_text(message) -> tuple[str, Optional[int]]:
    raw = getattr(message, "text", None) or getattr(message, "caption", None) or ""
    parts = str(raw).split(None, 1)
    if len(parts) > 1 and parts[1].strip():
        return parts[1].strip(), None

    replied = getattr(message, "reply_to_message", None)
    if replied is not None:
        text = getattr(replied, "text", None) or getattr(replied, "caption", None) or ""
        if str(text).strip():
            return str(text).strip(), getattr(replied, "id", None)
    return "", None


def _maximum_text_length() -> int:
    try:
        value = int(os.environ.get("TTS_MAX_CHARACTERS", "4000"))
    except ValueError:
        value = 4000
    return max(100, min(10000, value))


async def _ensure_gtts() -> None:
    if importlib.util.find_spec("gtts") is not None:
        return
    installed = await asyncio.to_thread(install_library, "gTTS>=2.5,<3")
    if not installed or importlib.util.find_spec("gtts") is None:
        raise RuntimeError("gTTS could not be installed. Rebuild Zelretch with the latest main package.")


def _generate_mp3(text: str, output_path: Path) -> None:
    from gtts import gTTS

    speech = gTTS(text=text, lang="en", slow=False, timeout=(10, 35))
    speech.save(str(output_path))


async def _convert_to_voice(mp3_path: Path, ogg_path: Path) -> bool:
    ffmpeg = shutil.which("ffmpeg")
    if not ffmpeg:
        return False

    process = await asyncio.create_subprocess_exec(
        ffmpeg,
        "-y",
        "-hide_banner",
        "-loglevel",
        "error",
        "-i",
        str(mp3_path),
        "-vn",
        "-c:a",
        "libopus",
        "-b:a",
        "48k",
        "-vbr",
        "on",
        "-application",
        "voip",
        str(ogg_path),
        stdout=asyncio.subprocess.DEVNULL,
        stderr=asyncio.subprocess.PIPE,
    )
    try:
        _, stderr = await asyncio.wait_for(process.communicate(), timeout=90)
    except asyncio.TimeoutError:
        process.kill()
        await process.wait()
        return False
    return process.returncode == 0 and ogg_path.is_file() and ogg_path.stat().st_size > 0


async def _edit_status(message, text: str) -> None:
    try:
        await message.edit(text, **_plain_edit_kwargs())
    except Exception:
        pass


@Client.on_message(
    zel_command(["voice", "tts"], MODULE_NAME, FILENAME, "[English text/reply]")
    & zel_sudo()
)
async def text_to_speech(client, message):
    source_message = message
    text, replied_message_id = _extract_text(source_message)
    status_message = await who_message(client, message)

    if not text:
        await _edit_status(
            status_message,
            "Send .voice <English text>, or reply to a text message with .voice.",
        )
        return

    maximum = _maximum_text_length()
    if len(text) > maximum:
        await _edit_status(
            status_message,
            f"The text is too long. The current limit is {maximum} characters.",
        )
        return

    await _edit_status(status_message, "Generating the voice note…")

    try:
        await _ensure_gtts()
        Path("temp").mkdir(parents=True, exist_ok=True)
        with tempfile.TemporaryDirectory(prefix="tts_", dir="temp") as directory:
            temp_directory = Path(directory)
            mp3_path = temp_directory / "speech.mp3"
            ogg_path = temp_directory / "speech.ogg"

            try:
                await asyncio.wait_for(
                    asyncio.to_thread(_generate_mp3, text, mp3_path), timeout=120
                )
            except asyncio.TimeoutError as exc:
                raise RuntimeError("The text-to-speech service timed out.") from exc

            if not mp3_path.is_file() or mp3_path.stat().st_size == 0:
                raise RuntimeError("The text-to-speech service returned an empty audio file.")

            reply_parameters = (
                ReplyParameters(message_id=replied_message_id)
                if replied_message_id
                else None
            )

            converted = await _convert_to_voice(mp3_path, ogg_path)
            if converted:
                await client.send_voice(
                    source_message.chat.id,
                    voice=str(ogg_path),
                    reply_parameters=reply_parameters,
                )
            else:
                # A legacy deployment may not contain FFmpeg. The MP3 remains
                # usable, so send it as audio rather than failing the command.
                await client.send_audio(
                    source_message.chat.id,
                    audio=str(mp3_path),
                    title="Text to Speech",
                    performer="Zelretch",
                    reply_parameters=reply_parameters,
                )

        try:
            await status_message.delete()
        except Exception:
            pass
    except Exception as exc:
        detail = " ".join(str(exc).split())
        await _edit_status(
            status_message,
            f"Text-to-speech failed.\n{detail[:900] or 'Unknown TTS error.'}",
        )
