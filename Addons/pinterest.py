"""Zelretch Addon: Pinterest Downloader

Downloads a Pinterest image or video from a public pin URL.

Category: Files & Media
Maintainer: Siam Chowdhury
GitHub: https://github.com/ChowdhurySiam
Telegram: @Ch0wdhury_Siam
"""

from __future__ import annotations

import asyncio
import json
import os
from typing import Any

from bs4 import BeautifulSoup
from pyrogram import Client

from command import get_text, who_message, zel_command, zel_sudo
from requirements_installer import install_library

install_library("requests bs4")
import requests

ZELRETCH_MODULE_INFO = {
    "title": "Pinterest Downloader",
    "icon": "📌",
    "category": "Files & Media",
    "description": "Downloads a supported Pinterest image or video from a public pin URL.",
    "developer": "Siam Chowdhury",
    "github": "https://github.com/ChowdhurySiam",
    "telegram": "https://t.me/Ch0wdhury_Siam",
}

LANGUAGES = {
    "en": {
        "searching": "<emoji id='5397755618750653196'>🌟</emoji> Searching Pinterest...",
        "usage": "Usage: <code>{prefix}pinterest &lt;pin URL&gt;</code>",
        "error": "<emoji id='5397755618750653196'>🌟</emoji> <b>Error:</b> {error}",
        "video": "<emoji id='5397755618750653196'>🌟</emoji> <b>Pinterest video</b>",
        "image": "<emoji id='5397755618750653196'>🌟</emoji> <b>Pinterest image</b>",
    }
}


def _download_page(url: str) -> str:
    response = requests.get(
        url,
        timeout=20,
        allow_redirects=True,
        headers={
            "User-Agent": (
                "Mozilla/5.0 (Linux; Android 13) AppleWebKit/537.36 "
                "Chrome/126.0 Mobile Safari/537.36"
            )
        },
    )
    response.raise_for_status()
    return response.text


def _video_from_pin_data(pin_data: dict[str, Any]) -> str | None:
    videos = pin_data.get("videos")
    if not isinstance(videos, dict):
        return None

    video_urls = videos.get("videoUrls")
    if isinstance(video_urls, list):
        urls = [str(url) for url in video_urls if str(url).startswith(("http://", "https://"))]
        for url in urls:
            if url.lower().endswith(".mp4") and "720" in url.lower():
                return url
        for url in urls:
            if url.lower().endswith(".mp4"):
                return url
        if urls:
            return urls[0]

    video_list = videos.get("videoList")
    if isinstance(video_list, dict):
        for key in ("v720P", "vHLSV4"):
            item = video_list.get(key)
            if isinstance(item, dict) and item.get("url"):
                return str(item["url"])
    return None


def _extract_media(html_text: str) -> tuple[str | None, str | None]:
    soup = BeautifulSoup(html_text, "html.parser")
    pin_data: dict[str, Any] = {}

    for script in soup.find_all("script", type="application/json"):
        try:
            data = json.loads(script.string or "")
        except (json.JSONDecodeError, TypeError):
            continue
        candidate = (
            data.get("response", {})
            .get("data", {})
            .get("v3GetPinQuery", {})
            .get("data", {})
        )
        if isinstance(candidate, dict):
            pin_data = candidate
            video_url = _video_from_pin_data(pin_data)
            if video_url:
                return video_url, None

    for script in soup.find_all("script", type="application/ld+json"):
        try:
            data = json.loads(script.string or "")
        except (json.JSONDecodeError, TypeError):
            continue
        candidates = data if isinstance(data, list) else [data]
        for item in candidates:
            if not isinstance(item, dict):
                continue
            content_url = item.get("contentUrl")
            if item.get("@type") == "VideoObject" and content_url:
                return str(content_url), None

    video_tag = soup.find("video", src=True)
    if video_tag and video_tag.get("src"):
        return str(video_tag["src"]), None

    for image in soup.find_all("img"):
        image_url = image.get("src") or image.get("data-src")
        if image_url and str(image_url).startswith(("http://", "https://")):
            return None, str(image_url)

    return None, None


@Client.on_message(
    zel_command("pinterest", "Pinterest", os.path.basename(__file__), "<pin URL>")
    & zel_sudo()
)
async def pinterest(client, message):
    message = await who_message(client, message)
    parts = (message.text or "").split(maxsplit=1)
    if len(parts) < 2 or not parts[1].strip():
        from command import my_prefix

        await message.edit(
            get_text(
                "Pinterest",
                "usage",
                LANGUAGES=LANGUAGES,
                prefix=my_prefix(),
            )
        )
        return

    pin_url = parts[1].strip()
    if not pin_url.startswith(("http://", "https://")):
        await message.edit(
            get_text(
                "Pinterest",
                "error",
                LANGUAGES=LANGUAGES,
                error="Provide a valid public Pinterest URL.",
            )
        )
        return

    await message.edit(get_text("Pinterest", "searching", LANGUAGES=LANGUAGES))

    try:
        html_text = await asyncio.to_thread(_download_page, pin_url)
        video_url, image_url = await asyncio.to_thread(_extract_media, html_text)

        if video_url:
            await client.send_video(
                message.chat.id,
                video=video_url,
                caption=get_text("Pinterest", "video", LANGUAGES=LANGUAGES),
                message_thread_id=message.message_thread_id,
            )
            await message.delete()
            return

        if image_url:
            await client.send_photo(
                message.chat.id,
                photo=image_url,
                caption=get_text("Pinterest", "image", LANGUAGES=LANGUAGES),
                message_thread_id=message.message_thread_id,
            )
            await message.delete()
            return

        await message.edit(
            get_text(
                "Pinterest",
                "error",
                LANGUAGES=LANGUAGES,
                error="No downloadable image or video was found.",
            )
        )
    except Exception as exc:
        await message.edit(
            get_text(
                "Pinterest",
                "error",
                LANGUAGES=LANGUAGES,
                error=str(exc),
            )
        )
