"""Zelretch Addon: Subscription Key Extractor

Parses supported subscription links and extracts available connection keys.

Category: Utilities
Maintainer: Siam Chowdhury
GitHub: https://github.com/ChowdhurySiam
Telegram: @Ch0wdhury_Siam
"""

ZELRETCH_MODULE_INFO = {'title': 'Subscription Key Extractor', 'icon': '🗝️', 'category': 'Utilities', 'description': 'Parses supported subscription links and extracts available connection keys.', 'developer': 'Siam Chowdhury', 'github': 'https://github.com/ChowdhurySiam', 'telegram': 'https://t.me/Ch0wdhury_Siam'}

import asyncio

from pyrogram import Client
from command import zel_command, zel_sudo, who_message , get_text
import base64
import os 

from requirements_installer import install_library

install_library('requests -U')
import requests

headers = { 
    "User-Agent": "Happ/3.9.1",
}

LANGUAGES = {'en': {'need_link': "<b><emoji id='5210952531676504517'>❌</emoji> Give me a subscription "
                     'link!</b>',
        'searching': "<b><emoji id='5264727218734524899'>🔄</emoji> Searching subscription...</b>",
        'decrypting': "<b><emoji id='5264727218734524899'>🔄</emoji> Decrypting happ:// link...</b>",
        'empty_response': "<b><emoji id='5210952531676504517'>❌</emoji> Empty response from the "
                          'link.</b>',
        'decrypt_fail': "<b><emoji id='5210952531676504517'>❌</emoji> Failed to decrypt happ:// "
                        'link.</b>',
        'fetch_decode_fail': "<b><emoji id='5210952531676504517'>❌</emoji> Failed to fetch or "
                             'decode subscription.</b>',
        'caption': "<emoji id='5267392860122006833'>📝</emoji> | Zelretch"}}



@Client.on_message(zel_command("get_keys", "GetKeys", os.path.basename(__file__), "[link to sub]") & zel_sudo())
async def get_config(client, message):
    message = await who_message(client, message)
    args = (message.text or "").split(maxsplit=1)
    arg = args[1].strip() if len(args) > 1 else None
    if not arg:
        await message.edit(get_text("get_keys", "need_link", LANGUAGES=LANGUAGES))
        return
    await message.edit(get_text("get_keys", "searching", LANGUAGES=LANGUAGES))

    if arg.startswith("happ://crypt"):
        await message.edit(get_text("get_keys", "decrypting", LANGUAGES=LANGUAGES))
        try:
            unhapp_headers = {"Content-Type": "application/json"}
            resp = await asyncio.to_thread(
                requests.post,
                "https://unhapp.xyz/api.php",
                headers=unhapp_headers,
                json={"url": arg},
                timeout=30,
            )
            resp.raise_for_status()
            decrypted = (resp.text or "").strip()
            if not decrypted.startswith("http"):
                await message.edit(get_text("get_keys", "decrypt_fail", LANGUAGES=LANGUAGES))
                return
            arg = decrypted
            await message.edit(get_text("get_keys", "searching", LANGUAGES=LANGUAGES))
        except Exception:
            await message.edit(get_text("get_keys", "decrypt_fail", LANGUAGES=LANGUAGES))
            return

    try:
        req = await asyncio.to_thread(requests.get, arg, headers=headers, timeout=30)
        req.raise_for_status()
        ans = (req.text or "").strip()
        if not ans:
            await message.edit(get_text("get_keys", "empty_response", LANGUAGES=LANGUAGES))
            return

        padded = ans + ("=" * (-len(ans) % 4))
        decoded = base64.b64decode(padded).decode("utf-8", errors="replace")
    except Exception:
        await message.edit(get_text("get_keys", "fetch_decode_fail", LANGUAGES=LANGUAGES))
        return
    file_path = 'temp/keys.txt'
    with open(file_path, 'w', encoding='utf-8') as file:
        file.write(decoded)

    await client.send_document(message.chat.id, file_path, caption=get_text("get_keys", "caption", LANGUAGES=LANGUAGES), message_thread_id=message.message_thread_id)
    try:
        os.remove(file_path)
    except OSError:
        pass
