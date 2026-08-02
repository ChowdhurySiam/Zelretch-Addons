"""Zelretch Addon: Quote Maker

Creates a quote image from a replied Telegram message.

Category: Files & Media
Maintainer: Siam Chowdhury
GitHub: https://github.com/ChowdhurySiam
Telegram: @Ch0wdhury_Siam
"""

ZELRETCH_MODULE_INFO = {'title': 'Quote Maker', 'icon': '💬', 'category': 'Files & Media', 'description': 'Creates a quote image from a replied Telegram message.', 'developer': 'Siam Chowdhury', 'github': 'https://github.com/ChowdhurySiam', 'telegram': 'https://t.me/Ch0wdhury_Siam', 'undo': '.undo (reply to the Addon output)'}
import asyncio
from pyrogram import Client, filters
from command import zel_command, zel_sudo, who_message
import os

@Client.on_message(zel_command("q", "Quotes", os.path.basename(__file__), "[reply]") & zel_sudo())
async def quotly(client, message):
    message = await who_message(client, message)
    if not message.reply_to_message:
        await message.edit("Reply to message")
        return

    await client.unblock_user("QuotLyBot")
    await message.edit("Create quotes... wait...")
    await message.reply_to_message.forward("QuotLyBot")

    is_sticker = False

    while not is_sticker:
        try:
            async for iii in client.get_chat_history("QuotLyBot", limit=1):
                await client.send_sticker(message.chat.id, iii.sticker.file_id)
            is_sticker = True
            await message.delete()
        except:
            await asyncio.sleep(1)
