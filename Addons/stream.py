"""Zelretch Addon: Stream Utilities

Provides supported streaming and media-link utilities.

Category: Files & Media
Maintainer: Siam Chowdhury
GitHub: https://github.com/ChowdhurySiam
Telegram: @Ch0wdhury_Siam
"""
ZELRETCH_MODULE_INFO = {'title': 'Stream Utilities', 'icon': '📡', 'category': 'Files & Media', 'description': 'Provides supported streaming and media-link utilities.', 'developer': 'Siam Chowdhury', 'github': 'https://github.com/ChowdhurySiam', 'telegram': 'https://t.me/Ch0wdhury_Siam', 'undo': '.undo (reply to the Addon output)'}
from random import randint, choice
from time import sleep
from pyrogram import Client, filters
from command import zel_command, zel_sudo, who_message
import os

@Client.on_message(zel_command('stream', 'Stream', os.path.basename(__file__)) & zel_sudo())
async def stream_kangel(client, message):
    message = await who_message(client, message)
    actions = ['💵 Receiving a donation!', '🛍 Reviewing a product...', '💻 Playing a game...', '🍰 Taking a snack break...', '☕ Taking a short break...']
    try:
        await message.edit('💅 Preparing the stream layout...')
        sleep(2)
        await message.edit('⌨️ Starting the stream...')
        for _ in range(2):
            sleep(2)
            c = choice(actions)
            await message.edit(c)
            actions.remove(c)
        num_subs = randint(100, 1000)
        await message.edit('❤️ Ending the stream and saying goodbye...')
        sleep(2)
        await message.edit(f'\n\t\t\t👋 Stream ended!\n\t\t\tYou gained {num_subs} new subscribers.\n\t\t\t')
    except Exception as e:
        await client.send_message(message.chat.id, f'❌ An error occurred! | {e}')
