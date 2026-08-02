"""Zelretch Addon: Neko Media

Fetches a random neko-themed image.

Category: Media
Maintainer: Siam Chowdhury
GitHub: https://github.com/ChowdhurySiam
Telegram: @Ch0wdhury_Siam
"""

ZELRETCH_MODULE_INFO = {'title': 'Neko Media', 'icon': '🐾', 'category': 'Media', 'description': 'Fetches a random neko-themed image.', 'developer': 'Siam Chowdhury', 'github': 'https://github.com/ChowdhurySiam', 'telegram': 'https://t.me/Ch0wdhury_Siam'}

from pyrogram import Client, filters
from command import zel_command, zel_sudo, who_message
from requirements_installer import install_library
import os

install_library("requests -U") 

import requests

@Client.on_message(zel_command("neko", "Neko", os.path.basename(__file__)) & zel_sudo())
async def neko(client, message):
    message = await who_message(client, message)
    await message.edit("Neko tyan..~")
    try:
        resp = requests.get("https://nekos.best/api/v2/neko")
        data = resp.json()
        url = data["results"][0]["url"]
        await client.send_photo(message.chat.id, photo=str(url),message_thread_id=message.message_thread_id)
        await message.delete()
    except Exception as f:
        await message.edit(f"Oops..~\n{f}")
