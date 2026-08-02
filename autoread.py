"""Zelretch Addon: Auto Read

Automatically marks messages as read in configured chats.

Category: Automation
Maintainer: Siam Chowdhury
GitHub: https://github.com/ChowdhurySiam
Telegram: @Ch0wdhury_Siam
"""

ZELRETCH_MODULE_INFO = {'title': 'Auto Read', 'icon': '👁️', 'category': 'Automation', 'description': 'Automatically marks messages as read in configured chats.', 'developer': 'Siam Chowdhury', 'github': 'https://github.com/ChowdhurySiam', 'telegram': 'https://t.me/Ch0wdhury_Siam'}

import re
from pyrogram import Client, filters
from command import zel_command, zel_sudo, who_message
import os

the_regex = r"^r\/([^\s\/])+"
i = filters.chat([])

@Client.on_message(i)
async def auto_read(client, message):
    await client.read_history(message.chat.id)
    message.continue_propagation()

@Client.on_message(zel_command("autoread", "AutoReadChat", os.path.basename(__file__)) & zel_sudo())
async def add_to_auto_read(client, message):
    message = await who_message(client, message)
    if message.chat.id in i:
        i.remove(message.chat.id)
        await message.edit("Autoread deactivated")
    else:
        i.add(message.chat.id)
        await message.edit("Autoread activated")
