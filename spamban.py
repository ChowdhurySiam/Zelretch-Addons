"""Zelretch Addon: Spam Protection Check

Checks the current account against supported Telegram spam restrictions.

Category: Telegram Tools
Maintainer: Siam Chowdhury
GitHub: https://github.com/ChowdhurySiam
Telegram: @Ch0wdhury_Siam
"""

ZELRETCH_MODULE_INFO = {'title': 'Spam Protection Check', 'icon': '🛡️', 'category': 'Telegram Tools', 'description': 'Checks the current account against supported Telegram spam restrictions.', 'developer': 'Siam Chowdhury', 'github': 'https://github.com/ChowdhurySiam', 'telegram': 'https://t.me/Ch0wdhury_Siam'}

from pyrogram import Client, filters
from command import zel_command, zel_sudo, who_message
import os

@Client.on_message(zel_command("spamban", "SpamBan", os.path.basename(__file__)) & zel_sudo())
async def spamban(client, message):
    message = await who_message(client, message)
    await message.edit("Checking your account for Spamban...")
    await client.unblock_user("spambot")
    await client.send_message("spambot", "/start")
    async for iii in client.get_chat_history("spambot", limit=1):
        await message.edit(iii.text)
