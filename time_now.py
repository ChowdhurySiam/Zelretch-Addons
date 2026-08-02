"""Zelretch Addon: Current Time

Shows the current date and time.

Category: Utilities
Maintainer: Siam Chowdhury
GitHub: https://github.com/ChowdhurySiam
Telegram: @Ch0wdhury_Siam
"""

ZELRETCH_MODULE_INFO = {'title': 'Current Time', 'icon': '🕒', 'category': 'Utilities', 'description': 'Shows the current date and time.', 'developer': 'Siam Chowdhury', 'github': 'https://github.com/ChowdhurySiam', 'telegram': 'https://t.me/Ch0wdhury_Siam'}

import datetime
from pyrogram import Client, filters
from command import zel_command, zel_sudo, who_message
import os

@Client.on_message(zel_command("time", "TimeNow", os.path.basename(__file__)) & zel_sudo())
async def time(client, message):
    message = await who_message(client, message)
    now = datetime.datetime.now()
    now = now.strftime("%Y-%m-%d - %H:%M:%S")
    now = datetime.datetime.now().strftime("Date: %d/%m/%Y\nTime: %H:%M:%S")
    await message.edit(now)
