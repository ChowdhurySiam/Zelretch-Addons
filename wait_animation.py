"""Zelretch Addon: Wait Animation

Displays a short animated waiting sequence.

Category: Fun
Maintainer: Siam Chowdhury
GitHub: https://github.com/ChowdhurySiam
Telegram: @Ch0wdhury_Siam
"""

ZELRETCH_MODULE_INFO = {'title': 'Wait Animation', 'icon': '⏳', 'category': 'Fun', 'description': 'Displays a short animated waiting sequence.', 'developer': 'Siam Chowdhury', 'github': 'https://github.com/ChowdhurySiam', 'telegram': 'https://t.me/Ch0wdhury_Siam'}

from pyrogram import Client, filters
from command import zel_command, zel_sudo, who_message
import os

@Client.on_message(zel_command("wait", "WaitDoksBlyaaa", os.path.basename(__file__)) & zel_sudo())
async def wait_command(client, message):
    message = await who_message(client, message)
    video_url = "https://0x0.st/X9S-.mp4"
    if message.reply_to_message:
        id_m = message.reply_to_message.id
    else:
        id_m = message.id
    try:
        await message.delete()
        await client.send_video(
        chat_id=message.chat.id,
        video=video_url,
        reply_to_message_id=id_m,
        message_thread_id=message.message_thread_id)
    except Exception as e:
        message.reply(f"Error | {e}")
