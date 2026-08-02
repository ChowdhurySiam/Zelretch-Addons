"""Zelretch Addon: Message Cleanup

Deletes a replied message or a selected message range.

Category: Administration
Maintainer: Siam Chowdhury
GitHub: https://github.com/ChowdhurySiam
Telegram: @Ch0wdhury_Siam
"""

ZELRETCH_MODULE_INFO = {'title': 'Message Cleanup', 'icon': '🗑️', 'category': 'Administration', 'description': 'Deletes a replied message or a selected message range.', 'developer': 'Siam Chowdhury', 'github': 'https://github.com/ChowdhurySiam', 'telegram': 'https://t.me/Ch0wdhury_Siam', 'undo': '.undo removes only the status output; deleted messages cannot be restored'}
from pyrogram import Client, filters
from command import zel_command, zel_sudo, who_message
import os

@Client.on_message(zel_command("del", "Purge", os.path.basename(__file__), "[reply]") & zel_sudo())
async def delete_messages(client, message):
    message = await who_message(client, message)
    if message.reply_to_message:
        message_id = message.reply_to_message.id
        await client.delete_messages(message.chat.id, message_id)
    await message.delete()

@Client.on_message(zel_command("purge", "Purge", os.path.basename(__file__), "[reply/group_id] [start_id] [stop_id]") & zel_sudo())
async def purge(client, message):
    message = await who_message(client, message)
    try:
        try:
            g = message.command[1]
            try:
                g = int(g)
            except:
                g = str(g)
            r = int(message.command[2])
            m = int(message.command[3])
        except:
            if message.reply_to_message:
                r = message.reply_to_message.id
                m = message.id
                g = message.chat.id
            else:
                await message.edit("<i>I don't see reply</i>")

        await message.delete()
        while r != m:
            try:
                await client.delete_messages(g, int(r))
            except:
                pass
            r += 1

        await client.send_message(message.chat.id, f"<b>Messages deleted!</b>")
    except Exception as f:
        await message.edit(f"<i>Don't have permision.</i>{f}")
