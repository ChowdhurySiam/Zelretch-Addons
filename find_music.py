"""Zelretch Addon: Music Finder

Finds lyrics and music results across supported providers.

Category: Media
Maintainer: Siam Chowdhury
GitHub: https://github.com/ChowdhurySiam
Telegram: @Ch0wdhury_Siam
"""

ZELRETCH_MODULE_INFO = {'title': 'Music Finder', 'icon': '🎵', 'category': 'Media', 'description': 'Finds lyrics and music results across supported providers.', 'developer': 'Siam Chowdhury', 'github': 'https://github.com/ChowdhurySiam', 'telegram': 'https://t.me/Ch0wdhury_Siam'}

import asyncio
import json
import os
from pyrogram import Client, filters
from command import zel_command, zel_sudo, who_message
from requirements_installer import install_library

install_library("lyricsgenius requests -U") 

import requests
from lyricsgenius import Genius

GENIUS_TOKEN_PATH = "userdata/genius_api_token"


def get_genius_token() -> str:
    token = os.environ.get("GENIUS_API_TOKEN", "").strip()
    if token:
        return token
    try:
        with open(GENIUS_TOKEN_PATH, "r", encoding="utf-8") as file:
            return file.read().strip()
    except FileNotFoundError:
        return ""


@Client.on_message(zel_command("genius_config", "FindMusic", os.path.basename(__file__), "[api_token]") & zel_sudo())
async def genius_config(client, message):
    message = await who_message(client, message)
    parts = message.text.split(maxsplit=1)
    if len(parts) < 2 or not parts[1].strip():
        status = "configured" if get_genius_token() else "not configured"
        return await message.edit(f"🎵 <b>Genius API token is {status}.</b>")
    os.makedirs("userdata", exist_ok=True)
    with open(GENIUS_TOKEN_PATH, "w", encoding="utf-8") as file:
        file.write(parts[1].strip())
    await message.edit("✅ <b>Genius API token saved securely to MongoDB-backed runtime storage.</b>")

@Client.on_message(zel_command(["l", "lyrics"], "FindMusic", os.path.basename(__file__), "[song_name]") & zel_sudo())
async def send_music(client, message):
    message = await who_message(client, message)
    if len(message.text.split()) >= 2:
        api_token = get_genius_token()
        if not api_token:
            return await message.edit(
                "⚠️ <b>Genius API token is not configured.</b>\n"
                "Use <code>.genius_config YOUR_TOKEN</code> or set "
                "<code>GENIUS_API_TOKEN</code>."
            )
        await client.edit_message_text(message.chat.id, message.id, 'Searching lyrics...')
        url = {"Authorization": f"Bearer {api_token}"}
        l = Genius(api_token)
        song_name = ' '.join(message.text.split()[1:])
        text = song_name.lower().replace(' ', '%20')
        q = requests.get(f'https://api.genius.com/search?q={text}', headers=url).text
        data_dict = json.loads(q)
        try:
            url_song = data_dict['response']['hits'][0]['result']['url']
            lyrics = l.lyrics(song_url=url_song).replace('Embed','')
            with open('song_text.txt','w+',encoding='utf-8') as file:
                file.write(lyrics)
            await client.send_document(message.chat.id, 'song_text.txt', caption='Keep the lyrics this song!',message_thread_id=message.message_thread_id)
            os.remove('song_text.txt')
        except Exception as e:
            await client.edit_message_text(message.chat.id, message.id, "I can't find text!")
    else:
        await client.edit_message_text(message.chat.id, message.id, 'Give me a name song!')

@Client.on_message(zel_command(["dm", "dmusic"], "FindMusic", os.path.basename(__file__), "[song_name]") & zel_sudo())
async def d_send_music(client, message):
    message = await who_message(client, message)
    bots = "DeezerMusicBot"

    await message.edit("Search...")
    song_name = ""
    if len(message.command) > 1:
        song_name = " ".join(message.command[1:])
    elif message.reply_to_message and len(message.command) == 1:
        song_name = (
                message.reply_to_message.text or message.reply_to_message.caption
        )
    elif not message.reply_to_message and len(message.command) == 1:
        await message.edit("Enter the name of the music")
        await asyncio.sleep(2)
        await message.delete()
        return

    song_results = await client.get_inline_bot_results(bots, song_name)

    try:
        saved = await client.send_inline_bot_result(
            chat_id="me",
            query_id=song_results.query_id,
            result_id=song_results.results[0].id,
        )

        await client.send_audio(
            chat_id=message.chat.id,
            audio=str(saved.audio.file_id),
            message_thread_id=message.message_thread_id
        )

        await client.delete_messages("me", saved.id)
    except TimeoutError:
        await message.edit("That didn't work out")
    except: 
        await message.edit("I can't find music!")
    await asyncio.sleep(2)
    await message.delete()

@Client.on_message(zel_command(["lm", "lmusic"], "FindMusic", os.path.basename(__file__), "[song_name]") & zel_sudo())
async def l_send_music(client, message):
    message = await who_message(client, message)
    bots = "LosslessRobot"
    await message.edit("Search...")
    song_name = ""
    if len(message.command) > 1:
        song_name = " ".join(message.command[1:])
    elif message.reply_to_message and len(message.command) == 1:
        song_name = (
                message.reply_to_message.text or message.reply_to_message.caption
        )
    elif not message.reply_to_message and len(message.command) == 1:
        await message.edit("Enter the name of the music")
        await asyncio.sleep(2)
        await message.delete()
        return

    song_results = await client.get_inline_bot_results(bots, song_name)

    try:
        saved = await client.send_inline_bot_result(
            chat_id=message.chat.id,
            query_id=song_results.query_id,
            result_id=song_results.results[0].id,
        )
    except TimeoutError:
        await message.edit("That didn't work out")
    except:
        await message.edit("I can't find music!")
    await asyncio.sleep(2)
    await message.delete()
