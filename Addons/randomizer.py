"""Zelretch Addon: Random Number

Generates a random number using configurable minimum and maximum values.

Category: Utilities
Maintainer: Siam Chowdhury
GitHub: https://github.com/ChowdhurySiam
Telegram: @Ch0wdhury_Siam
"""
ZELRETCH_MODULE_INFO = {'title': 'Random Number', 'icon': '🎲', 'category': 'Utilities', 'description': 'Generates a random number using configurable minimum and maximum values.', 'developer': 'Siam Chowdhury', 'github': 'https://github.com/ChowdhurySiam', 'telegram': 'https://t.me/Ch0wdhury_Siam'}
import asyncio
import os
import random
from pyrogram import Client, filters
from command import zel_command, zel_sudo, who_message, my_prefix

def load_config():
    try:
        with open('userdata/randomizer_min', 'r', encoding='utf-8') as f:
            min_value = f.read().strip()
    except FileNotFoundError:
        min_value = None
    try:
        with open('userdata/randomizer_max', 'r', encoding='utf-8') as f:
            max_value = f.read().strip()
    except FileNotFoundError:
        max_value = None
    return {'min_value': int(min_value) if min_value else None, 'max_value': int(max_value) if max_value else None}

@Client.on_message(zel_command('rnd', 'Randomizer', os.path.basename(__file__), '[min] [max]') & zel_sudo())
async def rnd_handler(client, message):
    message = await who_message(client, message)
    args = message.text.split()[1:]
    if len(args) == 2:
        try:
            min_value = int(args[0])
            max_value = int(args[1])
        except ValueError:
            return await message.edit('🚫 Enter two integers.')
    else:
        config = load_config()
        min_value = config['min_value']
        max_value = config['max_value']
    if min_value is None or max_value is None:
        return await message.edit('🚫 Specify a number range in the command or module configuration.')
    if min_value > max_value:
        return await message.edit('🚫 The minimum value cannot exceed the maximum value.')
    random_number = random.randint(min_value, max_value)
    await message.edit(f'✅ Random number between <code>{min_value}</code> and <code>{max_value}</code>: <code>{random_number}</code>')

@Client.on_message(zel_command('randomizer_config', 'Randomizer', os.path.basename(__file__), '[min] [max]') & zel_sudo())
async def randomizer_config_handler(client, message):
    message = await who_message(client, message)
    args = message.text.split()[1:]
    if len(args) != 2:
        return await message.edit(f'🚫 Usage: <code>{my_prefix()}randomizer_config [MIN] [MAX]</code>')
    try:
        min_value = int(args[0])
        max_value = int(args[1])
    except ValueError:
        return await message.edit('🚫 Enter two integers.')
    if min_value > max_value:
        return await message.edit('🚫 The minimum value cannot exceed the maximum value.')
    with open('userdata/randomizer_min', 'w', encoding='utf-8') as f:
        f.write(str(min_value))
    with open('userdata/randomizer_max', 'w', encoding='utf-8') as f:
        f.write(str(max_value))
    await message.edit(f'✅ Configuration saved: <code>{min_value} - {max_value}</code>')
