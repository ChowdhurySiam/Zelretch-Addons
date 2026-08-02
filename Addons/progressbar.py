"""Zelretch Addon: Progress Animation

Displays an animated progress bar with optional custom text.

Category: Fun
Maintainer: Siam Chowdhury
GitHub: https://github.com/ChowdhurySiam
Telegram: @Ch0wdhury_Siam
"""

ZELRETCH_MODULE_INFO = {'title': 'Progress Animation', 'icon': '📊', 'category': 'Fun', 'description': 'Displays an animated progress bar with optional custom text.', 'developer': 'Siam Chowdhury', 'github': 'https://github.com/ChowdhurySiam', 'telegram': 'https://t.me/Ch0wdhury_Siam', 'undo': '.undo (reply to the Addon output)'}
import time
from pyrogram import Client, filters
from command import zel_command, zel_sudo, who_message
import os

@Client.on_message(zel_command("progressbar", "Progressbar", os.path.basename(__file__), "[text]") & zel_sudo())
async def progressbar(client, message):
    message = await who_message(client, message)
    try:
        text = ' '.join(message.text.split()[1:])

        total = 100
        bar_length = 10
        for i in range(total + 1):
            percent = 100.0 * i / total
            time.sleep(0.1)
            await message.edit(
                text + "\n[{:{}}] {:>3}%".format("█" * int(percent / (100.0 / bar_length)), bar_length, int(percent)))
    except IndexError:
        message.edit('No text here!')
