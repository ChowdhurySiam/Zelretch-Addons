"""Zelretch Addon: Patriot Text

Applies an English leetspeak style to supplied or outgoing text.
"""

ZELRETCH_MODULE_INFO = {"title": "Patriot Text", "icon": "🦅", "category": "Creative", "description": "Applies an English leetspeak style to replied or outgoing text.", "developer": "Siam Chowdhury", "github": "https://github.com/ChowdhurySiam", "telegram": "https://t.me/Ch0wdhury_Siam"}

import os
from pyrogram import Client, filters
from command import zel_command, zel_sudo, who_message

translate_map = str.maketrans({"a": "4", "e": "3", "i": "1", "o": "0", "s": "5", "t": "7", "A": "4", "E": "3", "I": "1", "O": "0", "S": "5", "T": "7"})
patriot_enabled = False

@Client.on_message(zel_command("patriot", "Patriot Text", os.path.basename(__file__)) & zel_sudo())
async def patriotcmd(client, message):
    message = await who_message(client, message)
    global patriot_enabled
    patriot_enabled = not patriot_enabled
    state = "enabled" if patriot_enabled else "disabled"
    await message.edit(f"🦅 <b>Patriot Text is {state}.</b>")

@Client.on_message(zel_command("pat", "Patriot Text", os.path.basename(__file__), "[reply]") & zel_sudo())
async def patcmd(client, message):
    message = await who_message(client, message)
    reply = message.reply_to_message
    if not reply or not reply.text:
        return await message.edit("<b>Reply to a text message and use </b><code>pat</code>.")
    await message.edit(f"🦅 <b>Styled text</b>:\n\n{reply.text.translate(translate_map)}")

@Client.on_message(filters.outgoing & filters.text & zel_sudo())
async def watcher(client, message):
    if patriot_enabled and message.text:
        translated = message.text.translate(translate_map)
        if message.text != translated:
            await message.edit(translated)
