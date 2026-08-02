"""Zelretch Addon: Public OSINT Lookup

Queries supported public OSINT sources for a supplied phone number.

Category: Information
Maintainer: Siam Chowdhury
GitHub: https://github.com/ChowdhurySiam
Telegram: @Ch0wdhury_Siam
"""
ZELRETCH_MODULE_INFO = {'title': 'Public OSINT Lookup', 'icon': '🔎', 'category': 'Information', 'description': 'Queries supported public OSINT sources for a supplied phone number.', 'developer': 'Siam Chowdhury', 'github': 'https://github.com/ChowdhurySiam', 'telegram': 'https://t.me/Ch0wdhury_Siam', 'undo': '.undo (reply to the Addon output)'}
import asyncio
from pyrogram import Client, filters
from command import zel_command, zel_sudo, who_message
import os
bot_tag = 'thojkrpthrptbot'

@Client.on_message(zel_command(['eye', 'osint'], 'LeakOsint', os.path.basename(__file__), '[phone]') & zel_sudo())
async def LeakOsint(client, message):
    message = await who_message(client, message)
    number = message.command[1]
    await message.edit(f'⏳ | Checking account {number} for available data. This may take a moment...')
    await client.unblock_user(bot_tag)
    await client.send_message(bot_tag, number)
    await asyncio.sleep(20)
    await message.edit('Search results:')
    async for iii in client.get_chat_history(bot_tag, limit=1):
        await client.forward_messages(message.chat.id, bot_tag, iii.id)
