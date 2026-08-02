"""Zelretch Addon: Client Detector

Estimates which Telegram client a user is using from public message data.

Category: Telegram Tools
Maintainer: Siam Chowdhury
GitHub: https://github.com/ChowdhurySiam
Telegram: @Ch0wdhury_Siam
"""
ZELRETCH_MODULE_INFO = {'title': 'Client Detector', 'icon': '📱', 'category': 'Telegram Tools', 'description': 'Estimates which Telegram client a user is using from public message data.', 'developer': 'Siam Chowdhury', 'github': 'https://github.com/ChowdhurySiam', 'telegram': 'https://t.me/Ch0wdhury_Siam', 'undo': '.undo (reply to the Addon output)'}
import asyncio
import os
from pyrogram import Client
from pyrogram.types import Message
from command import zel_command, zel_sudo, who_message
from requirements_installer import install_library
install_library('requests -U')
import requests
CALLS_BASE_URL = 'https://calls.okcdn.ru'
CALLS_API_KEY = os.environ.get('TELEGA_CALLS_API_KEY', '').strip()
SESSION_DATA = '{"device_id":"telega_alert","version":2,"client_version":"android_8","client_type":"SDK_ANDROID"}'

def is_telega_user(user_id: int) -> bool | None:
    if not CALLS_API_KEY:
        return None
    try:
        user_id = int(user_id)
        if user_id <= 0:
            return False
        auth_response = requests.post(f'{CALLS_BASE_URL}/api/auth/anonymLogin', data={'application_key': CALLS_API_KEY, 'session_data': SESSION_DATA}, headers={'Accept': 'application/json'}, timeout=12)
        auth_response.raise_for_status()
        session_key = str((auth_response.json() or {}).get('session_key') or '').strip()
        if not session_key:
            return False
        lookup_response = requests.post(f'{CALLS_BASE_URL}/api/vchat/getOkIdsByExternalIds', data={'application_key': CALLS_API_KEY, 'session_key': session_key, 'externalIds': f'[{{"id":"{user_id}","ok_anonym":false}}]'}, headers={'Accept': 'application/json'}, timeout=12)
        lookup_response.raise_for_status()
        ids = (lookup_response.json() or {}).get('ids') or []
        for item in ids:
            external = (item or {}).get('external_user_id') or {}
            if str(external.get('id') or '') == str(user_id):
                return True
        return False
    except Exception:
        return False

@Client.on_message(zel_command('telega', 'TelegaDetector', os.path.basename(__file__), '[reply/@username/id]') & zel_sudo())
async def telega_handler(client, message):
    message = await who_message(client, message)
    parts = message.text.split(maxsplit=1)
    if len(parts) >= 2:
        target = parts[1].strip()
        try:
            if target.startswith('@'):
                user = await client.get_users(target)
                user_id = user.id
            else:
                user_id = int(target)
                user = await client.get_users(user_id)
        except Exception:
            return await message.edit('Enter a user ID or username, or reply to a message.')
    elif message.reply_to_message and message.reply_to_message.from_user:
        user_id = message.reply_to_message.from_user.id
        user = await client.get_users(user_id)
    else:
        return await message.edit('Enter a user ID or username, or reply to a message.')
    first_name = user.first_name or ''
    last_name = user.last_name or ''
    full_name = f'{first_name} {last_name}'.strip()
    telega_check = await asyncio.to_thread(is_telega_user, user_id)
    if telega_check is None:
        return await message.edit('⚠️ <b>Client detection is not configured.</b>\nSet <code>TELEGA_CALLS_API_KEY</code> in the deployment environment.')
    if telega_check:
        await message.edit(f'🚨 <b>{full_name}</b> uses Telega or has used it previously')
    else:
        await message.edit(f'✅ <b>{full_name}</b> does not use Telega')
