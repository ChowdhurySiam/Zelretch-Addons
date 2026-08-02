"""Zelretch Addon: QR Generator

Generates a QR code from supplied text or a link.

Category: Utilities
Maintainer: Siam Chowdhury
GitHub: https://github.com/ChowdhurySiam
Telegram: @Ch0wdhury_Siam
"""

ZELRETCH_MODULE_INFO = {'title': 'QR Generator', 'icon': '🔳', 'category': 'Utilities', 'description': 'Generates a QR code from supplied text or a link.', 'developer': 'Siam Chowdhury', 'github': 'https://github.com/ChowdhurySiam', 'telegram': 'https://t.me/Ch0wdhury_Siam'}

from pyrogram import Client, filters
from command import zel_command, zel_sudo, who_message
import os

@Client.on_message(zel_command("qr", "QRcode", os.path.basename(__file__), "[text]") & zel_sudo())
async def qr(client, message):
    message = await who_message(client, message)
    try:
        texts = ""
        if message.reply_to_message:
            texts = message.reply_to_message.text
        elif len(message.text.split(maxsplit=1)) == 2:
            texts = message.text.split(maxsplit=1)[1]
        text = texts.replace(' ', '%20')
        QRcode = f"https://api.qrserver.com/v1/create-qr-code/?size=300x300&data={text}"
        await message.delete()
        await client.send_photo(message.chat.id, QRcode)
    except Exception as e:
        await message.edit(f'Error: {e}')
