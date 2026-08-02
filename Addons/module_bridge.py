"""Zelretch Addon: Module Bridge

Converts compatible legacy modules into the Zelretch addon format.

Category: Developer Tools
Maintainer: Siam Chowdhury
GitHub: https://github.com/ChowdhurySiam
Telegram: @Ch0wdhury_Siam
"""

ZELRETCH_MODULE_INFO = {'title': 'Module Bridge', 'icon': '🧩', 'category': 'Developer Tools', 'description': 'Converts compatible legacy modules into the Zelretch addon format.', 'developer': 'Siam Chowdhury', 'github': 'https://github.com/ChowdhurySiam', 'telegram': 'https://t.me/Ch0wdhury_Siam', 'undo': '.module_bridge_reset'}
from pyrogram import Client
from command import zel_command, zel_sudo, who_message, my_prefix, get_text
import os
import shutil
from requirements_installer import install_library
install_library('openai requests')
from openai import AsyncOpenAI
from openai import RateLimitError, APIError, APIConnectionError, APITimeoutError
import requests
import asyncio
import time

filename = os.path.basename(__file__)
Module_Name = 'ModuleBridge'

LANGUAGES = {'en': {'loading_reply': '✨ | Loading module from reply...',
        'loading_url': '✨ | Loading module from URL: {url}',
        'error_status': '✨ | Error loading module from URL: {status}',
        'error_request': '✨ | Error loading module from URL: {error}',
        'no_input': '✨ | Reply to a module file or provide a link!',
        'no_content': '✨ | Failed to get module content.',
        'generating': '✨ | Generating module...',
        'generated': '✨ | Generated module: <code>{module_name}</code>',
        'error_generate': '✨ | Error generating module :(',
        'rate_limit': '✨ | Rate limit exceeded. Please try again later or add your own API key.',
        'api_error': '✨ | API error: {error}',
        'connection_error': '✨ | Connection error. Please check your internet connection.',
        'timeout_error': '✨ | Request timeout. Please try again.',
        'current_model': '✨ | **Current model:** `{model}`\n'
                         '\n'
                         '**Usage:**\n'
                         '`{prefix}module_bridge_config [model_name]`\n'
                         '\n'
                         '**Example models:**\n'
                         '• `qwen/qwen2.5-72b-instruct`\n'
                         '• `anthropic/claude-3.5-sonnet`\n'
                         '• `meta-llama/llama-3.1-8b-instruct`\n'
                         '• `google/gemini-pro-1.5`\n'
                         '\n'
                         " <a href='https://openrouter.ai/models?max_price=0'><b>You can get "
                         'models here</b></a>',
        'no_model': '✨ | <b>Please specify a model name! \n'
                    ' You can get models <a '
                    "href='https://openrouter.ai/models?max_price=0'>here</a></b>",
        'not_free': '✨ | <b>Please specify a free model! \n'
                    ' You can get models <a '
                    "href='https://openrouter.ai/models?max_price=0'>here</a></b>",
        'success': '✨ | **Model successfully changed!**\n'
                   '\n'
                   '**New model:** `{model}`\n'
                   '\n'
                   'Now all requests will use this model.',
        'error_save': '✨ | **Error saving model:**\n`{error}`'}}

def get_bridge_model():
    try:
        with open("userdata/module_bridge_model", "r+", encoding="utf-8") as f:
            model = f.read().strip()
            if model:
                return model
    except:
        return "qwen/qwen3-coder:free"

def save_bridge_model(model):
    with open("userdata/module_bridge_model", "w+", encoding="utf-8") as f:
        f.write(model)


async def create_module(module_text, module_name):
    prompt = (
        f"""
{requests.get("https://pastebin.com/raw/uT0MjKCY").text}
{module_name}.py
========
Module source: 
```python
{module_text}
```
"""
    )
    
    api_key = (os.environ.get("OPENROUTER_API_KEY") or "").strip()
    if not api_key:
        raise RuntimeError("OPENROUTER_API_KEY is required for Module Bridge")
    client_ai = AsyncOpenAI(
        base_url="https://openrouter.ai/api/v1",
        api_key=api_key,
    )
    
    max_retries = 5
    base_delay = 1
    
    for attempt in range(max_retries):
        try:
            response = await client_ai.chat.completions.create(
                model=get_bridge_model(),
                messages=[{"role": "user", "content": prompt}]
            )
            return response.choices[0].message.content.replace("```python", "").replace("```", "")
        
        except RateLimitError as e:
            if attempt < max_retries - 1:
                delay = base_delay * (2 ** attempt) + (time.time() % 1)
                await asyncio.sleep(delay)
                continue
            else:
                return None
        
        except APIConnectionError as e:
            if attempt < max_retries - 1:
                delay = base_delay * (2 ** attempt)
                await asyncio.sleep(delay)
                continue
            else:
                return None
        
        except APITimeoutError as e:
            if attempt < max_retries - 1:
                delay = base_delay * (2 ** attempt)
                await asyncio.sleep(delay)
                continue
            else:
                return None
    
    return None 

@Client.on_message(zel_command("module_bridge", Module_Name, filename, "[Link/Reply]") & zel_sudo())
async def module_bridge(client, message):
    message = await who_message(client, message)
    file_content = None
    module_name = None
    if message.reply_to_message and message.reply_to_message.document:
        loading_text = get_text("module_bridge", "loading_reply", LANGUAGES=LANGUAGES)
        await message.edit(loading_text)
        file = await client.download_media(message.reply_to_message.document)
        with open(file, "r", encoding="utf-8") as f:
            file_content = f.read()
        os.remove(file)
        if os.path.exists("downloads"):
            shutil.rmtree("downloads")
        module_name = message.reply_to_message.document.file_name.replace(".py", "")
    elif len(message.command) > 1 and (message.text.split()[1].startswith("http") or message.text.split()[1].startswith("https")):
        url = message.text.split()[1]
        loading_text = get_text("module_bridge", "loading_url", LANGUAGES=LANGUAGES, url=url)
        await message.edit(loading_text)
        try:
            response = requests.get(url,headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"},verify=False)
            if response.status_code != 200:
                error_text = get_text("module_bridge", "error_status", LANGUAGES=LANGUAGES, status=response.status_code)
                await message.edit(error_text)
                return
            file_content = response.text
            module_name = url.split("/")[-1].replace(".py", "")
        except requests.exceptions.RequestException as e:
            error_text = get_text("module_bridge", "error_request", LANGUAGES=LANGUAGES, error=str(e))
            await message.edit(error_text)
            return
    else:
        no_input_text = get_text("module_bridge", "no_input", LANGUAGES=LANGUAGES)
        await message.edit(no_input_text)
        return

    if file_content is None:
        no_content_text = get_text("module_bridge", "no_content", LANGUAGES=LANGUAGES)
        await message.edit(no_content_text)
        return

    generating_text = get_text("module_bridge", "generating", LANGUAGES=LANGUAGES)
    await message.edit(generating_text)
    
    try:
        answer = await create_module(file_content, module_name)
    except RateLimitError:
        error_text = get_text("module_bridge", "rate_limit", LANGUAGES=LANGUAGES)
        await message.edit(error_text)
        return
    except APIConnectionError:
        error_text = get_text("module_bridge", "connection_error", LANGUAGES=LANGUAGES)
        await message.edit(error_text)
        return
    except APITimeoutError:
        error_text = get_text("module_bridge", "timeout_error", LANGUAGES=LANGUAGES)
        await message.edit(error_text)
        return
    except APIError as e:
        error_text = get_text("module_bridge", "api_error", LANGUAGES=LANGUAGES, error=str(e))
        await message.edit(error_text)
        return
    except Exception as e:
        error_text = get_text("module_bridge", "error_generate", LANGUAGES=LANGUAGES)
        await message.edit(error_text)
        return
    
    if answer is not None:
        file_path = f"modules/loaded/{module_name}.py"
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(answer)
    
        caption_text = get_text("module_bridge", "generated", LANGUAGES=LANGUAGES, module_name=module_name)
        await client.send_document(
            message.chat.id,
            file_path,
            caption=caption_text,
        )
        os.remove(file_path)
    else:
        error_text = get_text("module_bridge", "error_generate", LANGUAGES=LANGUAGES)
        await message.edit(error_text)

@Client.on_message(zel_command("module_bridge_config", Module_Name, filename, "[Model]") & zel_sudo())
async def module_bridge_config(client, message):
    message = await who_message(client, message)
    if len(message.command) < 2:
        current_model = get_bridge_model()
        current_text = get_text("module_bridge", "current_model", LANGUAGES=LANGUAGES, model=current_model, prefix=my_prefix())
        await message.edit(current_text)
        return
    
    new_model = message.text.split()[1]
    if not new_model or new_model.strip() == "":
        no_model_text = get_text("module_bridge", "no_model", LANGUAGES=LANGUAGES)
        await message.edit(no_model_text)
        return
    try:
        save_bridge_model(new_model)
        success_text = get_text("module_bridge", "success", LANGUAGES=LANGUAGES, model=new_model)
        await message.edit(success_text)
    except Exception as e:
        error_text = get_text("module_bridge", "error_save", LANGUAGES=LANGUAGES, error=str(e))
        await message.edit(error_text)

@Client.on_message(zel_command("module_bridge_reset", Module_Name, filename) & zel_sudo())
async def module_bridge_reset(client, message):
    message = await who_message(client, message)
    path = "userdata/module_bridge_model"
    if os.path.exists(path):
        os.remove(path)
        return await message.edit("✅ Module Bridge model configuration reset.")
    await message.edit("Module Bridge was already using its default model.")
