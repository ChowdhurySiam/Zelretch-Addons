"""Zelretch Addon: Detailed Statistics

Provides an expanded summary of account and dialog statistics.

Category: Telegram Tools
Maintainer: Siam Chowdhury
GitHub: https://github.com/ChowdhurySiam
Telegram: @Ch0wdhury_Siam
"""

ZELRETCH_MODULE_INFO = {'title': 'Detailed Statistics', 'icon': '📊', 'category': 'Telegram Tools', 'description': 'Provides an expanded summary of account and dialog statistics.', 'developer': 'Siam Chowdhury', 'github': 'https://github.com/ChowdhurySiam', 'telegram': 'https://t.me/Ch0wdhury_Siam', 'undo': '.undo (reply to the Addon output)'}
import asyncio
import os
from pyrogram import Client
from pyrogram.enums import ChatType
from command import zel_command, zel_sudo, who_message, get_text

filename = os.path.basename(__file__)
Module_Name = "Stats"

LANGUAGES = {'en': {'stats': '\n'
                 '<emoji id=5774022692642492953>✅</emoji><b> Account Statistics</b>\n'
                 '\n'
                 '</b><emoji id=5208454037531280484>💜</emoji><b> Total chats: '
                 '</b><code>{all_chats}</code><b>\n'
                 '\n'
                 '</b><emoji id=6035084557378654059>👤</emoji><b> Private chats: '
                 '</b><code>{users}</code><b>\n'
                 '</b><emoji id=6030400221232501136>🤖</emoji><b> Bots: </b><code>{bots}</code><b>\n'
                 '</b><emoji id=6032609071373226027>👥</emoji><b> Groups: '
                 '</b><code>{groups}</code><b>\n'
                 '</b><emoji id=5870886806601338791>👥</emoji><b> Channels: '
                 '</b><code>{channels}</code><b>\n'
                 '</b><emoji id=5870563425628721113>📨</emoji><b> Archived chats: '
                 '</b><code>{archived}</code>',
        'loading_stats': '<b><emoji id=5309893756244206277>🫥</emoji> Loading statistics...</b>'}}

@Client.on_message(zel_command("stats_xdesai", Module_Name, filename) & zel_sudo())
async def stats_handler(client, message):
    message = await who_message(client, message)

    loading_text = get_text(Module_Name, "loading_stats", LANGUAGES=LANGUAGES)
    await message.edit(loading_text)
    
    users = 0
    bots = 0
    groups = 0
    channels = 0
    all_chats = 0
    archived = 0
    

    async for dialog in client.get_dialogs():
        chat = dialog.chat
        if chat.is_forum and dialog.top_message and dialog.top_message.id == 0:
            archived += 1
        if chat.type == ChatType.BOT:
            bots += 1
            all_chats += 1
        elif chat.type == ChatType.PRIVATE:
            users += 1
            all_chats += 1
        elif chat.type == ChatType.GROUP or chat.type == ChatType.SUPERGROUP:
            groups += 1
            all_chats += 1
        elif chat.type == ChatType.CHANNEL:
            channels += 1
            all_chats += 1
    
    stats_text = get_text(Module_Name, "stats", LANGUAGES=LANGUAGES,
                         users=users, bots=bots, channels=channels, groups=groups,
                         all_chats=all_chats, archived=archived)
    
    await message.edit(stats_text)
