"""Zelretch Addon: Wikipedia Search

Searches English Wikipedia and returns a concise summary.
"""
ZELRETCH_MODULE_INFO = {"title": "Wikipedia Search", "icon": "📖", "category": "Information", "description": "Searches English Wikipedia and returns a concise summary.", "developer": "Siam Chowdhury", "github": "https://github.com/ChowdhurySiam", "telegram": "https://t.me/Ch0wdhury_Siam"}

import os
from pyrogram import Client
from command import zel_command, zel_sudo, who_message
from requirements_installer import install_library
install_library("wikipedia")
import wikipedia
wikipedia.set_lang("en")

@Client.on_message(zel_command("wiki", "Wikipedia", os.path.basename(__file__), "[query]") & zel_sudo())
async def wiki(client, message):
    message = await who_message(client, message)
    query = " ".join(message.command[1:]).strip()
    if not query:
        return await message.edit("Enter a Wikipedia search query.")
    await message.edit("<b>Searching English Wikipedia...</b>")
    try:
        result = wikipedia.summary(query)
        await message.edit(f"<b>Query:</b>\n<code>{query}</code>\n\n<b>Summary:</b>\n<code>{result}</code>")
    except Exception as exc:
        await message.edit(f"<b>Query:</b>\n<code>{query}</code>\n\n<b>Result:</b>\n<code>{exc}</code>")
