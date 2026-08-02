"""Zelretch Addon: AI Gateway

Sends prompts to supported OpenRouter models from a single command.

Category: AI & Automation
Maintainer: Siam Chowdhury
GitHub: https://github.com/ChowdhurySiam
Telegram: @Ch0wdhury_Siam
"""
ZELRETCH_MODULE_INFO = {'title': 'AI Gateway', 'icon': '🤖', 'category': 'AI & Automation', 'description': 'Sends prompts to supported OpenRouter models from a single command.', 'developer': 'Siam Chowdhury', 'github': 'https://github.com/ChowdhurySiam', 'telegram': 'https://t.me/Ch0wdhury_Siam'}
import base64
import asyncio
from pyrogram import Client
from command import zel_command, zel_sudo, who_message, my_prefix
from requirements_installer import install_library
import os
install_library('requests')
import requests
public_key = 'c2stb3ItdjEtNjg1YzZiMDc2YjJhNDE4M2VkNTUzOWIyMTk3ZWY4MTk3YjkxYTE1ZDMxOTAxZjQ2YTQ5MTk0NTFjYzkxYzRmZQ=='
modules = {'deepseek': 'deepseek/deepseek-chat-v3-0324:free', 'gemini': 'google/gemini-2.0-flash-exp:free', 'qwen': 'qwen/qwen3-235b-a22b:free'}

@Client.on_message(zel_command('ai', 'AI', os.path.basename(__file__), '[Gemini/DeepSeek/Qwen] [message]') & zel_sudo())
async def ai(client, message):
    message = await who_message(client, message)
    try:
        module = message.text.split()[1].lower()
        model = modules.get(module)
        if not model:
            await message.edit('❌ Incorrect model indicated!')
            return
        await message.edit('🤖 Processing request...')
        message_for_da = ' '.join(message.text.split()[2:])
        key = str(base64.b64decode(public_key).decode('utf-8'))
        url = 'https://openrouter.ai/api/v1/chat/completions'
        payload = {'model': model, 'messages': [{'role': 'user', 'content': message_for_da}]}
        headers = {'Authorization': f'Bearer {key}', 'Content-Type': 'application/json'}

        def do_call():
            r = requests.post(url, json=payload, headers=headers, timeout=25)
            r.raise_for_status()
            return r.json()
        data = await asyncio.to_thread(do_call)
        result = data['choices'][0]['message']['content']
        await message.edit(f'👤 Prompt: {message_for_da}\n📔 Model: {module}\n🤖 Answer: {result}\n')
    except IndexError:
        await message.edit(f'❌ Missing input. Usage: {my_prefix()}ai <model> <prompt>')
    except requests.exceptions.RequestException as e:
        await message.edit(f'❌ OpenRouter API error: {e}')
    except Exception as e:
        await message.edit(f'❌ Unexpected error: {e}')
