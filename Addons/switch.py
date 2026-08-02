"""Zelretch Addon: Text Switch

Applies a reversible English letter-case transformation.
"""
ZELRETCH_MODULE_INFO = {"title": "Text Switch", "icon": "🔄", "category": "Fun", "description": "Swaps uppercase and lowercase English letters in supplied or replied text.", "developer": "Siam Chowdhury", "github": "https://github.com/ChowdhurySiam", "telegram": "https://t.me/Ch0wdhury_Siam"}

import os
from pyrogram import Client
from command import zel_command, zel_sudo, who_message

@Client.on_message(zel_command("sw", "Text Switch", os.path.basename(__file__), "[reply|text]") & zel_sudo())
async def switch(client, message):
    message = await who_message(client, message)
    supplied = " ".join(message.command[1:]).strip()
    text = supplied or (message.reply_to_message.text if message.reply_to_message else "")
    if not text:
        return await message.edit("No text was provided.")
    await message.edit(text.swapcase())
