"""Zelretch Addon: Aurora Bull

Creates randomized playful text sequences and timed message loops.

Category: Fun
Maintainer: Siam Chowdhury
GitHub: https://github.com/ChowdhurySiam
Telegram: @Ch0wdhury_Siam
"""

ZELRETCH_MODULE_INFO = {'title': 'Aurora Bull', 'icon': '🎲', 'category': 'Fun', 'description': 'Creates randomized playful text sequences and timed message loops.', 'developer': 'Siam Chowdhury', 'github': 'https://github.com/ChowdhurySiam', 'telegram': 'https://t.me/Ch0wdhury_Siam'}

# Licensed under GNU AGPLv3.

import asyncio
import json
import os
from random import choice
from pyrogram import Client, filters
from command import zel_command, zel_sudo, who_message, my_prefix
from requirements_installer import install_library
install_library("aiohttp -U")
import aiohttp

@Client.on_message(zel_command("abull", "AuroraBull", os.path.basename(__file__)) & zel_sudo())
async def abull(client, message):
    message = await who_message(client, message)
    url = "https://raw.githubusercontent.com/KorenbZla/HikkaModules/main/AuroraBull.json"
    
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            if response.status == 200:
                response_text = await response.text()
                try:
                    data = json.loads(response_text)
                    if "BullText" in data and isinstance(data["BullText"], list) and data["BullText"]:
                        text = choice(data["BullText"])
                        await message.edit(text)
                    else:
                        await message.edit("<b><i>Error: Key 'BullText' not found.</i></b>")
                except json.JSONDecodeError:
                    await message.edit("<b><i>Error: The JSON could not be decoded.</i></b>")
            else:
                await message.edit(f"<b><i>Error loading data</i></b>: {response.status}")

@Client.on_message(zel_command("abullspam", "AuroraBull", os.path.basename(__file__), "[time] [text]") & zel_sudo())
async def abullspam(client, message):
    message = await who_message(client, message)
    url = "https://raw.githubusercontent.com/KorenbZla/HikkaModules/main/AuroraBull.json"
    args = message.text.split()[1:]

    if not args:
        await message.edit("<b><i>Please enter valid arguments!</i></b>")
        return
    
    with open("userdata/aurorabull_state", "w", encoding="utf-8") as f:
        f.write("1")

    try:
        time = float(args[0])
        text = ' '.join(args[1:]) + " " if len(args) > 1 else ""
    except ValueError:
        await message.edit("<b><i>Please enter valid arguments!</i></b>")
        return

    await message.edit(f"<b><i>AuroraBull launched!</i></b>\n\n<b><i>Use <code>{my_prefix()}abulloff</code> to stop the attack.</i></b>")
    
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            if response.status == 200:
                response_text = await response.text()
                
                data = json.loads(response_text)
                if "BullText" in data and isinstance(data["BullText"], list) and data["BullText"]:
                    while True:
                        try:
                            with open("userdata/aurorabull_state", "r", encoding="utf-8") as f:
                                state = f.read().strip()
                        except FileNotFoundError:
                            state = "0"
                        
                        if state != "1":
                            break
                            
                        bull_text = choice(data["BullText"])
                        await message.reply(text + bull_text)
                        await asyncio.sleep(time)
                    return
                else:
                    await message.edit("<b><i>Error: Key 'BullText' not found.</i></b>")
                    return
            else:
                await message.edit(f"<b><i>Error loading data</i></b>: {response.status}")
                return

@Client.on_message(zel_command("abulloff", "AuroraBull", os.path.basename(__file__)) & zel_sudo())
async def abulloff(client, message):
    message = await who_message(client, message)
    with open("userdata/aurorabull_state", "w", encoding="utf-8") as f:
        f.write("0")
    await message.edit("<b><i>AuroraBull has stopped.</i></b>")
