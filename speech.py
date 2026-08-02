"""Zelretch Addon: Text to Speech

Converts supplied text into an audio message in supported languages.

Category: Files & Media
Maintainer: Siam Chowdhury
GitHub: https://github.com/ChowdhurySiam
Telegram: @Ch0wdhury_Siam
"""

ZELRETCH_MODULE_INFO = {'title': 'Text to Speech', 'icon': '🔊', 'category': 'Files & Media', 'description': 'Converts supplied text into an audio message in supported languages.', 'developer': 'Siam Chowdhury', 'github': 'https://github.com/ChowdhurySiam', 'telegram': 'https://t.me/Ch0wdhury_Siam'}

import random
import os
from pyrogram import Client, filters
from command import zel_command, zel_sudo, who_message
from requirements_installer import install_library

install_library("gTTS") 
from gtts import gTTS

@Client.on_message(zel_command("voice", "TextToVoice", os.path.basename(__file__), "[text]") & zel_sudo())
async def voice(client, message):
    message = await who_message(client, message)
    lang_code = os.environ.get("lang_code", "en")
    rnd = random.randint(10000, 99999)
    await message.delete()
    text = message.text.split(None, 1)[1]
    tts = gTTS(text, lang=lang_code)
    tts.save(f"temp/voice{rnd}.mp3")
    if message.reply_to_message:
        await client.send_voice(
            message.chat.id,
            voice=f"temp/voice{rnd}.mp3",
            reply_to_message_id=message.reply_to_message.id,
        )
    else:
        await client.send_voice(message.chat.id, voice=f"temp/voice{rnd}.mp3")
    os.remove(f"temp/voice{rnd}.mp3")

@Client.on_message(zel_command("voice_ru", "TextToVoice", os.path.basename(__file__), "[text]") & zel_sudo())
async def ru_voice(client, message):
    message = await who_message(client, message)
    lang_code = os.environ.get("lang_code", "ru")
    rnd = random.randint(10000, 99999)
    await message.delete()
    text = message.text.split(None, 1)[1]
    tts = gTTS(text, lang=lang_code)
    tts.save(f"temp/voice{rnd}.mp3")
    if message.reply_to_message:
        await client.send_voice(
            message.chat.id,
            voice=f"temp/voice{rnd}.mp3",
            reply_to_message_id=message.reply_to_message.id,
        )
    else:
        await client.send_voice(message.chat.id, voice=f"temp/voice{rnd}.mp3")
    os.remove(f"temp/voice{rnd}.mp3")
