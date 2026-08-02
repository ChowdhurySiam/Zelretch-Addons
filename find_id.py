"""Zelretch Addon: Chat ID Finder

Shows the current chat identifier and related Telegram IDs.

Category: Telegram Tools
Maintainer: Siam Chowdhury
GitHub: https://github.com/ChowdhurySiam
Telegram: @Ch0wdhury_Siam
"""

ZELRETCH_MODULE_INFO = {'title': 'Chat ID Finder', 'icon': '🆔', 'category': 'Telegram Tools', 'description': 'Shows the current chat identifier and related Telegram IDs.', 'developer': 'Siam Chowdhury', 'github': 'https://github.com/ChowdhurySiam', 'telegram': 'https://t.me/Ch0wdhury_Siam'}

from pyrogram import Client, filters
from command import zel_command, zel_sudo, who_message
import os

@Client.on_message(zel_command('id', 'FindIDThisChat', os.path.basename(__file__)) & zel_sudo())
async def find_id(client, message):
    message = await who_message(client, message)
    if message.reply_to_message is None:
        await message.edit(f"Chat ID: `{message.chat.id}`")
    else:
        await message.edit(f"User ID: `{message.reply_to_message.from_user.id}`\nChat ID: `{message.chat.id}`")
