"""Zelretch Addon: Patriot Text

Transforms text with a stylized character-substitution effect.

Category: Creative
Maintainer: Siam Chowdhury
GitHub: https://github.com/ChowdhurySiam
Telegram: @Ch0wdhury_Siam
"""

ZELRETCH_MODULE_INFO = {'title': 'Patriot Text', 'icon': '🎭', 'category': 'Creative', 'description': 'Transforms text with a stylized character-substitution effect.', 'developer': 'Siam Chowdhury', 'github': 'https://github.com/ChowdhurySiam', 'telegram': 'https://t.me/Ch0wdhury_Siam'}

import asyncio
from pyrogram import Client, filters
from command import zel_command, zel_sudo, who_message
import os

translate_map = {
    ord("з"): "Z",
    ord("З"): "Z",
    ord("z"): "Z",
    ord("о"): "O",
    ord("o"): "О",
    ord("в"): "V",
    ord("В"): "V",
    ord("v"): "V"
}

patriot_enabled = False

@Client.on_message(zel_command("patriot", "Патриот", os.path.basename(__file__)) & zel_sudo())
async def patriotcmd(client, message):
    message = await who_message(client, message)
    global patriot_enabled
    patriot_enabled = not patriot_enabled
    
    if patriot_enabled:
        return await message.edit("<b>🇷🇺 Патриот успешно включен. Страна может спать спокойно</b>")
    else:
        return await message.edit("❌ <b>Патриот выключен</b>")

@Client.on_message(zel_command("pat", "Патриот", os.path.basename(__file__), "[reply]") & zel_sudo())
async def patcmd(client, message):
    message = await who_message(client, message)
    reply = message.reply_to_message
    if not reply:
        return await message.edit("<b>Ответьте на сообщение с помощью </b><code>pat</code>")
    
    translated_text = reply.text.translate(translate_map)
    await message.edit(f"🇷🇺 <b>Патриот отредактировал сообщение</b>:\n\n{translated_text}")

@Client.on_message(filters.outgoing & zel_sudo())
async def watcher(client, message):
    if patriot_enabled:
        translated_text = message.text.translate(translate_map)
        if message.text != translated_text:
            await message.edit(translated_text)
