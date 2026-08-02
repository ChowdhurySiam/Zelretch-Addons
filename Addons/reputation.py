"""Zelretch Addon: Reputation

Tracks simple positive and negative reputation reactions in a chat.

Category: Community
Maintainer: Siam Chowdhury
GitHub: https://github.com/ChowdhurySiam
Telegram: @Ch0wdhury_Siam
"""

ZELRETCH_MODULE_INFO = {'title': 'Reputation', 'icon': '⭐', 'category': 'Community', 'description': 'Tracks simple positive and negative reputation reactions in a chat.', 'developer': 'Siam Chowdhury', 'github': 'https://github.com/ChowdhurySiam', 'telegram': 'https://t.me/Ch0wdhury_Siam'}

from pathlib import Path
from pyrogram import Client, filters
from command import zel_command, zel_sudo, who_message
import os

@Client.on_message(filters.text & filters.incoming & filters.regex(r"^\-$") & filters.reply)
async def repDown(client, message):
    try:
        if message.reply_to_message.from_user.is_self:
            if Path(f"temp/reputation").is_file():
                with open("temp/reputation", "r+") as f:
                    NowReputation = int(f.read())
                    f.close()
            else:
                NowReputation = 0
            with open("temp/reputation", "w+") as f:
                reputation = str(NowReputation - 1)
                f.write(reputation)
                f.close()
            await message.reply_text(f"❎ Reputation lowered (-1)\n🌐 Your reputation: {str(reputation)}")
    except:
        pass

@Client.on_message(filters.text & filters.incoming & filters.regex(r"^\+$") & filters.reply)
async def repUp(client, message):
    try:
        if message.reply_to_message.from_user.is_self:
            if Path(f"temp/reputation").is_file():
                with open("temp/reputation", "r+") as f:
                    NowReputation = int(f.read())
                    f.close()
            else:
                NowReputation = 0
            with open("temp/reputation", "w+") as f:
                reputation = str(NowReputation + 1)
                f.write(reputation)
                f.close()
            await message.reply_text(f"✅ Reputation increased (+1)\n🌐 Your reputation: {str(reputation)}")
    except:
        pass

@Client.on_message(zel_command("rep", "Reputation", os.path.basename(__file__), "[number]") & zel_sudo())
async def repNakrutka(client, message):
    message = await who_message(client, message)
    try:
        with open("temp/reputation", "w+") as f:
            rep = str(int(message.command[1]))
            f.write(rep)
            f.close()
            text = f"Reputation edited.\nReputation: {str(rep)}"
            await message.edit(text)

    except Exception as error:
        await message.edit(
            f"Error! Reputation edited to '0'\n\nLog: {error}")
        with open("temp/reputation", "w+") as f:
            f.write(str(int(0)))
            f.close()
