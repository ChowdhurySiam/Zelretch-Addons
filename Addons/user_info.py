"""Zelretch Addon: User Information

Displays concise or detailed public information about a Telegram user.

Category: Telegram Tools
Maintainer: Siam Chowdhury
GitHub: https://github.com/ChowdhurySiam
Telegram: @Ch0wdhury_Siam
"""

ZELRETCH_MODULE_INFO = {'title': 'User Information', 'icon': '👤', 'category': 'Telegram Tools', 'description': 'Displays concise or detailed public information about a Telegram user.', 'developer': 'Siam Chowdhury', 'github': 'https://github.com/ChowdhurySiam', 'telegram': 'https://t.me/Ch0wdhury_Siam', 'undo': '.undo (reply to the Addon output)'}
from pyrogram import Client, filters
from pyrogram.types import Message
from command import zel_command, zel_sudo, who_message
import os

@Client.on_message(zel_command("user_info", "Userinfo", os.path.basename(__file__), "[user_id/@username]") & zel_sudo())
async def get_user_inf(client: Client, message: Message):
    message = await who_message(client, message)
    await message.edit("<code>Receiving the information...</code>")

    if len(message.text.split()) >= 2:
        if message.text.split()[1][0] == '@':
            us = message.text.split()[1]
            user = await client.get_users(us)
            user = user.id
        else:
            try:
                user = message.text.split()[1]
                user = int(user)
            except:
                try:
                    user = message.reply_to_message.from_user.id
                except:
                    user = message.from_user.id
    else:
        try:
            user = message.reply_to_message.from_user.id
        except:
            user = message.from_user.id
    user_info = await client.get_users(user)
    try:
        username = f"@{user_info.username}"
    except:
        username = "None"

    user_info = f"""==========
[$] Username: <b>{username}</b>
[$] Id: <code>{str(user_info.id)}</code>
[$] Bot: <code>{str(user_info.is_bot)}</code>
[$] Scam: <code>{str(user_info.is_scam)}</code>
[$] Name: <code>{str(user_info.first_name)}</code>
</b>"""
    await message.edit(user_info)

@Client.on_message(zel_command("user_info_full", "Userinfo", os.path.basename(__file__), "[user_id/@username]") & zel_sudo())
async def get_full_user_inf(client: Client, message: Message):
    message = await who_message(client, message)
    await message.edit("<code>Receiving the information...</code>")

    if len(message.text.split()) >= 2:
        if message.text.split()[1][0] == '@':
            us = message.text.split()[1]
            user = await client.get_users(us)
            user = user.id
        else:
            try:
                user = message.text.split()[1]
                user = int(user)
            except:
                try:
                    user = message.reply_to_message.from_user.id
                except:
                    user = message.from_user.id
    else:
        try:
            user = message.reply_to_message.from_user.id
        except:
            user = message.from_user.id

    try:
        user_info = await client.get_users(user)

        try:
            username = f"@{user_info.username}"
        except:
            username = "None"

        user_info = f"""==========
[$] Username: <b>{username}</b>
[$] Mention: <b>{user_info.mention}</b>
[$] Id: <code>{str(user_info.id)}</code>
[$] Bot: <code>{str(user_info.is_bot)}</code>
[$] Scam: <code>{str(user_info.is_scam)}</code>
[$] Name: <code>{str(user_info.first_name)}</code>
[$] Deleted: <code>{str(user_info.is_deleted)}</code>
[$] Contact: <code>{str(user_info.is_contact)}</code>
[$] Mutual contact: <code>{str(user_info.is_mutual_contact)}</code>
[$] Verified: <code>{str(user_info.is_verified)}</code>
[$] DC: <code>{str(user_info.dc_id)}</code>"""
        await message.edit(user_info)
    except Exception as f:
        await message.edit(f"**An error occured...**\n\n{f}")
