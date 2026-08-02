"""Zelretch Addon: Direct Sender

Sends replied content to a Telegram ID or username.

Category: Telegram Tools
Maintainer: Siam Chowdhury
GitHub: https://github.com/ChowdhurySiam
Telegram: @Ch0wdhury_Siam
"""

ZELRETCH_MODULE_INFO = {'title': 'Direct Sender', 'icon': '📨', 'category': 'Telegram Tools', 'description': 'Sends replied content to a Telegram ID or username.', 'developer': 'Siam Chowdhury', 'github': 'https://github.com/ChowdhurySiam', 'telegram': 'https://t.me/Ch0wdhury_Siam', 'undo': '.undo (reply to the Addon output)'}
from pyrogram import Client, filters
from command import zel_command, zel_sudo, who_message
import os

@Client.on_message(zel_command("send", "SendToId", os.path.basename(__file__), "[ID/Username]") & zel_sudo())
async def sendtoid(client, message):
    message = await who_message(client, message)
    try:
        await client.unblock_user(message.command[1])
        await client.send_message(message.command[1], "Hi")
        await message.edit(f"Message send to {message.command[1]}")
    except:
        await message.edit("I can't send message!")
