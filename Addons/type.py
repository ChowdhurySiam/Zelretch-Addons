"""Zelretch Addon: Typing Animation

Animates supplied text as though it is being typed.

Category: Fun
Maintainer: Siam Chowdhury
GitHub: https://github.com/ChowdhurySiam
Telegram: @Ch0wdhury_Siam
"""

ZELRETCH_MODULE_INFO = {'title': 'Typing Animation', 'icon': '⌨️', 'category': 'Fun', 'description': 'Animates supplied text as though it is being typed.', 'developer': 'Siam Chowdhury', 'github': 'https://github.com/ChowdhurySiam', 'telegram': 'https://t.me/Ch0wdhury_Siam', 'undo': '.undo (reply to the Addon output)'}
import asyncio
from pyrogram import Client, filters
from command import zel_command, zel_sudo, who_message
import os

@Client.on_message(zel_command("type", "Type", os.path.basename(__file__), "[text]") & zel_sudo())
async def types(client, message):
    message = await who_message(client, message)
    try:
        orig_text = ' '.join(message.text.split()[1:])
        text = orig_text
        tbp = ""
        typing_symbol = "▒"
        while tbp != orig_text:
            await message.edit(str(tbp + typing_symbol))
            await asyncio.sleep(0.10)
            tbp = tbp + text[0]
            text = text[1:]
            await message.edit(str(tbp))
            await asyncio.sleep(0.10)
    except IndexError:
        message.edit('No text here!')
