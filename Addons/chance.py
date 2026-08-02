"""Zelretch Addon: Chance Meter

Generates a playful probability score for any question or phrase.

Category: Fun
Maintainer: Siam Chowdhury
GitHub: https://github.com/ChowdhurySiam
Telegram: @Ch0wdhury_Siam
"""

ZELRETCH_MODULE_INFO = {'title': 'Chance Meter', 'icon': '🎯', 'category': 'Fun', 'description': 'Generates a playful probability score for any question or phrase.', 'developer': 'Siam Chowdhury', 'github': 'https://github.com/ChowdhurySiam', 'telegram': 'https://t.me/Ch0wdhury_Siam', 'undo': '.undo (reply to the Addon output)'}
import random
from pyrogram import Client, filters
from command import zel_command, zel_sudo, who_message
import os

@Client.on_message(zel_command("chance", "Chance", os.path.basename(__file__), "[text]") & zel_sudo())
async def chance(client, message):
    message = await who_message(client, message)
    text = ' '.join(message.text.split()[1:])
    await message.edit(f"{text}\nChance: {random.randint(1, 100)}%")
