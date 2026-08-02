"""Zelretch Addon: Rich Link Builder

Creates clickable text using a supplied URL and label.

Category: Utilities
Maintainer: Siam Chowdhury
GitHub: https://github.com/ChowdhurySiam
Telegram: @Ch0wdhury_Siam
"""

from __future__ import annotations

import html
import os
from urllib.parse import urlparse

from pyrogram import Client
from pyrogram.types import LinkPreviewOptions

from command import who_message, zel_command, zel_sudo

ZELRETCH_MODULE_INFO = {
    "title": "Rich Link Builder",
    "icon": "🔗",
    "category": "Utilities",
    "description": "Creates clickable text using a supplied HTTP or HTTPS URL and label.",
    "undo": '.undo (reply to the Addon output)',
    "developer": "Siam Chowdhury",
    "github": "https://github.com/ChowdhurySiam",
    "telegram": "https://t.me/Ch0wdhury_Siam",
}


@Client.on_message(
    zel_command("link", "LinkInText", os.path.basename(__file__), "[url] [text]")
    & zel_sudo()
)
async def link(client, message):
    message = await who_message(client, message)
    args = (message.text or "").split(maxsplit=2)
    if len(args) < 3:
        return await message.edit("Usage: .link [url] [text]")

    target_url = args[1].strip()
    label = args[2].strip()
    parsed = urlparse(target_url)
    if parsed.scheme.lower() not in {"http", "https"} or not parsed.netloc:
        return await message.edit("The link must be a valid HTTP or HTTPS URL.")

    rendered = (
        f'<a href="{html.escape(target_url, quote=True)}">'
        f"{html.escape(label)}</a>"
    )
    await message.delete()
    await client.send_message(
        message.chat.id,
        rendered,
        link_preview_options=LinkPreviewOptions(is_disabled=True),
    )
