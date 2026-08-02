"""Zelretch Addon: Bulk Messaging

Sends repeated text or sticker messages with configurable count and delay.

Category: Restricted Tools
Maintainer: Siam Chowdhury
GitHub: https://github.com/ChowdhurySiam
Telegram: @Ch0wdhury_Siam
"""

ZELRETCH_MODULE_INFO = {'title': 'Bulk Messaging', 'icon': '📣', 'category': 'Restricted Tools', 'description': 'Sends repeated text or sticker messages with configurable count and delay.', 'developer': 'Siam Chowdhury', 'github': 'https://github.com/ChowdhurySiam', 'telegram': 'https://t.me/Ch0wdhury_Siam', 'undo': '.undo removes one selected output; already sent messages are not restored'}
import asyncio
from pyrogram import Client, filters
from command import zel_command, zel_sudo, who_message
import os

@Client.on_message(zel_command("stspam", "Spam", os.path.basename(__file__), "[count] [delay] [sticker_id]") & zel_sudo())
async def sticker_spam(client, message):
    message = await who_message(client, message)
    if not message.text.split("stspam", maxsplit=1)[1]:
        await message.edit("<i>Error</i>")

    sticker = message.command[3]
    count = int(message.command[1])
    sleep = int(message.command[2])
    await message.delete()

    for _ in range(count):
        await client.send_sticker(message.chat.id, sticker)
        await asyncio.sleep(sleep)

@Client.on_message(zel_command("spam", "Spam", os.path.basename(__file__), "[count] [delay] [text]") & zel_sudo())
async def spam(client, message):
    message = await who_message(client, message)
    if not message.text.split("spam", maxsplit=1)[1]:
        await message.edit("<i>Error</i>")
        return
    count = message.command[1]
    text = " ".join(message.command[3:])
    count = int(count)
    try:
        sleep = int(message.command[2])
    except Exception as error:
        await message.edit(error)
        sleep = float(message.command[2])
    await message.delete()

    for _ in range(count):
        await client.send_message(message.chat.id, text)
        await asyncio.sleep(sleep)

@Client.on_message(zel_command("help_spam", "Spam", os.path.basename(__file__)) & zel_sudo())
async def help_spam(client, message):
    message = await who_message(client, message)
    await message.edit(f""".stspam [ID] [Count] [Delay] - Start sticker spam.
```.spam [Count] [Delay] [Text]``` -Start message spam.""")
