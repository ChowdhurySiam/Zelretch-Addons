"""Zelretch Addon: Text to Speech

Converts English text into an audio message.
"""
ZELRETCH_MODULE_INFO = {"title": "Text to Speech", "icon": "🔊", "category": "Files & Media", "description": "Converts supplied English text into an audio message.", "developer": "Siam Chowdhury", "github": "https://github.com/ChowdhurySiam", "telegram": "https://t.me/Ch0wdhury_Siam"}

import os
import random
from pyrogram import Client
from command import zel_command, zel_sudo, who_message
from requirements_installer import install_library
install_library("gTTS")
from gtts import gTTS

@Client.on_message(zel_command("voice", "TextToVoice", os.path.basename(__file__), "[English text]") & zel_sudo())
async def voice(client, message):
    message = await who_message(client, message)
    parts = message.text.split(None, 1)
    if len(parts) < 2 or not parts[1].strip():
        return await message.edit("Enter English text to convert to speech.")
    path = f"temp/voice{random.randint(10000, 99999)}.mp3"
    gTTS(parts[1].strip(), lang="en").save(path)
    try:
        await client.send_voice(message.chat.id, voice=path, reply_to_message_id=message.reply_to_message.id if message.reply_to_message else None)
        await message.delete()
    finally:
        if os.path.exists(path):
            os.remove(path)
