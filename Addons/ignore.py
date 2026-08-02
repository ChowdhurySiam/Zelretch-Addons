"""Zelretch Addon: Ignore User

Suppresses selected incoming messages from a specified user or chat.

Category: Administration
Maintainer: Siam Chowdhury
GitHub: https://github.com/ChowdhurySiam
Telegram: @Ch0wdhury_Siam
"""

ZELRETCH_MODULE_INFO = {'title': 'Ignore User', 'icon': '🙈', 'category': 'Administration', 'description': 'Suppresses selected incoming messages from a specified user or chat.', 'developer': 'Siam Chowdhury', 'github': 'https://github.com/ChowdhurySiam', 'telegram': 'https://t.me/Ch0wdhury_Siam', 'undo': '.unignore'}
from pyrogram import Client, filters
from command import zel_command, zel_sudo, who_message
import os

i = filters.user([])

@Client.on_message(i & ~filters.me)
async def ignored(client, message):
    await message.delete()

@Client.on_message(zel_command("ignore", "IgnoreUser", os.path.basename(__file__), "[user_id/@username]") & zel_sudo())
async def add_ignore(client, message):
    message = await who_message(client, message)
    try:
        try:
            users = int(message.command[1])
        except:
            users = str(message.command[1]).replace("@", "")
            users = int((await client.get_users(str(users))).id)
    except:
        users = message.reply_to_message.from_user.id

    print(users)

    if users in i:
        i.remove(int(users))
        await message.edit(f"`{str(users)}` no longer ignored")
    else:
        i.add(int(users))
        await message.edit(f"`{str(users)}` ignored")

@Client.on_message(zel_command("unignore", "IgnoreUser", os.path.basename(__file__), "[user_id/@username/reply]") & zel_sudo())
async def remove_ignore(client, message):
    message = await who_message(client, message)
    try:
        if len(message.command) > 1:
            raw = str(message.command[1]).replace("@", "")
            user_id = int(raw) if raw.lstrip("-").isdigit() else int((await client.get_users(raw)).id)
        elif message.reply_to_message and message.reply_to_message.from_user:
            user_id = int(message.reply_to_message.from_user.id)
        else:
            return await message.edit("Usage: <code>.unignore [user_id/@username/reply]</code>")
    except Exception as exc:
        return await message.edit(f"Unable to resolve user: <code>{exc}</code>")

    try:
        i.remove(user_id)
    except Exception:
        return await message.edit(f"<code>{user_id}</code> was not ignored.")
    await message.edit(f"✅ <code>{user_id}</code> is no longer ignored.")
