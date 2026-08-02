"""Zelretch Addon: Password Generator

Generates a random password with the requested length.

Category: Utilities
Maintainer: Siam Chowdhury
GitHub: https://github.com/ChowdhurySiam
Telegram: @Ch0wdhury_Siam
"""

ZELRETCH_MODULE_INFO = {'title': 'Password Generator', 'icon': '🔐', 'category': 'Utilities', 'description': 'Generates a random password with the requested length.', 'developer': 'Siam Chowdhury', 'github': 'https://github.com/ChowdhurySiam', 'telegram': 'https://t.me/Ch0wdhury_Siam'}

import string
from random import choice
from pyrogram import Client, filters
from command import zel_command, zel_sudo, who_message
import os

@Client.on_message(zel_command('gen_password', 'GeneratePassword', os.path.basename(__file__), "[length]") & zel_sudo())
async def gen_pass(client, message):
    message = await who_message(client, message)
    try:
        char = message.command[1]
        alphabet = string.ascii_letters + string.digits
        password = ''
        for _ in range(int(char)):
            password = password + choice(alphabet)
        await message.edit(f"**Generated password:** {password}`")
    except ValueError:
        await message.edit(f'Input a number!')
    except IndexError:
        await message.edit(f'Not input a argument!')
