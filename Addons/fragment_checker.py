"""Zelretch Addon: Fragment Checker

Checks supported Telegram Fragment username information.

Category: Telegram Tools
Maintainer: Siam Chowdhury
GitHub: https://github.com/ChowdhurySiam
Telegram: @Ch0wdhury_Siam
"""

ZELRETCH_MODULE_INFO = {'title': 'Fragment Checker', 'icon': '💎', 'category': 'Telegram Tools', 'description': 'Checks supported Telegram Fragment username information.', 'developer': 'Siam Chowdhury', 'github': 'https://github.com/ChowdhurySiam', 'telegram': 'https://t.me/Ch0wdhury_Siam', 'undo': '.undo (reply to the Addon output)'}
from pyrogram import Client, filters
from command import zel_command, zel_sudo, who_message
from requirements_installer import install_library
import os

install_library("bs4 requests -U") 

import requests
from bs4 import BeautifulSoup

@Client.on_message(zel_command("fcheck", "FragmentChecker", os.path.basename(__file__), "[username]") & zel_sudo())
async def fcheck_handler(client, message):
    message = await who_message(client, message)
    args = " ".join(message.command[1:]) if len(message.command) > 1 else ""
    if not args:
        await message.edit("<emoji id=5212926868012935693>❌</emoji> <b>Please specify username</b>")
        return

    response = requests.get(f"https://fragment.com/username/{args}")
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, "html.parser")
        elements = soup.select(".table-cell-value.tm-value.icon-before.icon-ton")
        if elements:
            text = elements[0].text.strip()
            await message.edit(f"<emoji id=5215219508670638513>💎</emoji> <b>Username Found!</b>\n<emoji id=5467626799556992380>✈️</emoji> <b>Username:</b> <code>{args}</code>\n<emoji id=5460720028288557729>🪙</emoji> <b>Cost:</b> <code>{text}</code> TON")
        else:
            await message.edit(f"<emoji id=5212926868012935693>❌</emoji> <b>Username <code>{args}</code> not found!</b>")
