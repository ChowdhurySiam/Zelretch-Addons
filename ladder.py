"""Zelretch Addon: Text Ladder

Builds an animated ladder pattern from custom text.

Category: Fun
Maintainer: Siam Chowdhury
GitHub: https://github.com/ChowdhurySiam
Telegram: @Ch0wdhury_Siam
"""

ZELRETCH_MODULE_INFO = {'title': 'Text Ladder', 'icon': '🪜', 'category': 'Fun', 'description': 'Builds an animated ladder pattern from custom text.', 'developer': 'Siam Chowdhury', 'github': 'https://github.com/ChowdhurySiam', 'telegram': 'https://t.me/Ch0wdhury_Siam'}

from pyrogram import Client, filters
from command import zel_command, zel_sudo, who_message
import os

@Client.on_message(zel_command("ladder", "Ladder", os.path.basename(__file__), "[text]") & zel_sudo())
async def ladder(client, message):
    message = await who_message(client, message)
    try:
        orig_text = ' '.join(message.text.split()[1:])
        text = orig_text
        output = []
        for i in range(len(text) + 1):
            output.append(text[:i])
        ot = "\n".join(output)
        await message.edit(ot)
    except:
        await message.edit('Error in processing your request.')
