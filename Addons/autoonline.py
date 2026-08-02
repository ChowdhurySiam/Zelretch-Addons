"""Zelretch Addon: Presence Control

Keeps the account online or returns it to normal presence behavior.

Category: Automation
Maintainer: Siam Chowdhury
GitHub: https://github.com/ChowdhurySiam
Telegram: @Ch0wdhury_Siam
"""

ZELRETCH_MODULE_INFO = {'title': 'Presence Control', 'icon': '🟢', 'category': 'Automation', 'description': 'Keeps the account online or returns it to normal presence behavior.', 'developer': 'Siam Chowdhury', 'github': 'https://github.com/ChowdhurySiam', 'telegram': 'https://t.me/Ch0wdhury_Siam'}

import asyncio
from pyrogram import Client, filters
from modules.core.restarter import restart
from command import zel_command, zel_sudo, who_message
import os

@Client.on_message(zel_command("online", "AutoOnline", os.path.basename(__file__)) & zel_sudo())
async def online_now(client, message):
    message = await who_message(client, message)
    await message.edit("AutoOnline activated")
    while True:
        iii = await client.send_message("me", "bruh")
        await client.delete_messages("me", iii.id)
        await asyncio.sleep(45)

@Client.on_message(zel_command("offline", "AutoOnline", os.path.basename(__file__)) & zel_sudo())
async def offline_now(client, message):
    message = await who_message(client, message)
    await message.edit("AutoOnline deactivated")
