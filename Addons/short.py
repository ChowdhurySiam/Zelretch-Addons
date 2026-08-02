"""Zelretch Addon: URL Shortener

Creates a shortened link from supplied or replied text.

Category: Utilities
Maintainer: Siam Chowdhury
GitHub: https://github.com/ChowdhurySiam
Telegram: @Ch0wdhury_Siam
"""

ZELRETCH_MODULE_INFO = {'title': 'URL Shortener', 'icon': '✂️', 'category': 'Utilities', 'description': 'Creates a shortened link from supplied or replied text.', 'developer': 'Siam Chowdhury', 'github': 'https://github.com/ChowdhurySiam', 'telegram': 'https://t.me/Ch0wdhury_Siam'}

from pyrogram import Client, filters
from command import zel_command, zel_sudo, who_message
from requirements_installer import install_library
import os

install_library("requests")
import requests

@Client.on_message(zel_command("short", "ShortURL", os.path.basename(__file__), "[Reply/Link]") & zel_sudo())
async def shorten_link_command(client, message):
    message = await who_message(client, message)
    try:
        await message.edit("Shorting...")
        if message.reply_to_message:
            link = message.reply_to_message.text
        else:
            link = message.command[1]

        full_url = link.replace("https://", "").replace("http://", "")
        response = requests.get('https://tinyurl.com/api-create.php?url=' + full_url)

        short_url = response.text
        await message.edit(f"Short URL: {short_url}")
    except Exception as error:
        await message.edit(f"Error: {error}")
