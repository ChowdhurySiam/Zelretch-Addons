"""Zelretch Addon: Weather

Shows a text forecast and weather image for a city.

Category: Information
Maintainer: Siam Chowdhury
GitHub: https://github.com/ChowdhurySiam
Telegram: @Ch0wdhury_Siam
"""

ZELRETCH_MODULE_INFO = {'title': 'Weather', 'icon': '🌦️', 'category': 'Information', 'description': 'Shows a text forecast and weather image for a city.', 'developer': 'Siam Chowdhury', 'github': 'https://github.com/ChowdhurySiam', 'telegram': 'https://t.me/Ch0wdhury_Siam', 'undo': '.undo (reply to the Addon output)'}
from pyrogram import Client, filters
from command import zel_command, zel_sudo, who_message
from requirements_installer import install_library
import os

install_library("requests") 
import requests

def get_pic(city):
    city = city.lower()
    file_name = f"{city}.png"
    with open(file_name, "wb") as pic:
        response = requests.get(f"http://wttr.in/{city}_2&lang=en.png", stream=True)
        if not response.ok:
            print(response)
        for block in response.iter_content(1024):
            if not block:
                break
            pic.write(block)
        return file_name

@Client.on_message(zel_command("weather", "Weather", os.path.basename(__file__), "[city]") & zel_sudo())
async def weather(client, message):
    message = await who_message(client, message)
    try:
        city = message.command[1]
        await message.edit("Check weather...")
        r = requests.get(f"https://wttr.in/{city}?m?M?0?q?T&lang=en")
        await message.edit(f"🗺 You sity/village: {city}\n{r.text}")
        await client.send_photo(
        chat_id=message.chat.id,
        photo=get_pic(city),
        reply_to_message_id=message.id)
        os.remove(f"{city}.png")
    except Exception as e:
        await message.edit(f"Error | {e}")
