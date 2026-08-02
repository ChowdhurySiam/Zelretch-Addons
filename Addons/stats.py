"""Zelretch Addon: Account Statistics

Shows Telegram dialog, contact, group, and channel statistics.

Category: Telegram Tools
Maintainer: Siam Chowdhury
GitHub: https://github.com/ChowdhurySiam
Telegram: @Ch0wdhury_Siam
"""

ZELRETCH_MODULE_INFO = {'title': 'Account Statistics', 'icon': '📈', 'category': 'Telegram Tools', 'description': 'Shows Telegram dialog, contact, group, and channel statistics.', 'developer': 'Siam Chowdhury', 'github': 'https://github.com/ChowdhurySiam', 'telegram': 'https://t.me/Ch0wdhury_Siam'}

from datetime import datetime
import asyncio
from pyrogram import Client, filters
from pyrogram.enums import ChatType
from command import zel_command, zel_sudo, who_message
import os

@Client.on_message(zel_command(["stat", "stats"], "Statistic", os.path.basename(__file__)) & zel_sudo())
async def stats(client, message):
    message = await who_message(client, message)
    await message.edit("Parsing stats...")
    start = datetime.now()
    u = 0
    g = 0
    sg = 0
    c = 0
    b = 0
    group = ["supergroup", "group"]
    iter_dialog = client.get_dialogs()
    async for dialog in iter_dialog:
        if dialog.chat.type == ChatType.PRIVATE:
            u += 1
        elif dialog.chat.type == ChatType.BOT:
            b += 1
        elif dialog.chat.type == ChatType.GROUP:
            g += 1
        elif dialog.chat.type == ChatType.SUPERGROUP:
            sg += 1
        elif dialog.chat.type == ChatType.CHANNEL:
            c += 1
    end = datetime.now()
    ms = (end - start).seconds

    private_chat = f"**Privates:** {u}\n"
    group_chat = f"**Groups:** {g}\n"
    supergroup_chat = f"**Supergroups:** {sg}\n"
    channel_chat = f"**Channels:** {c}\n"
    bot_chat = f"**Bots:** {b}\n"
    statistic = private_chat + group_chat + supergroup_chat + channel_chat + bot_chat
    await message.edit(f"You stats:\n{statistic}\nParsed {ms} seconds")
