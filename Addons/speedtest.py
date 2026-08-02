"""Zelretch Addon: Speed Test

Measures network upload speed and latency with an English-only interface.
"""

ZELRETCH_MODULE_INFO = {"title": "Speed Test", "icon": "🚀", "category": "System", "description": "Measures network upload speed, latency, server location, and provider information.", "developer": "Siam Chowdhury", "github": "https://github.com/ChowdhurySiam", "telegram": "https://t.me/Ch0wdhury_Siam"}

import os
import time
from datetime import datetime
from pyrogram import Client
from command import zel_command, zel_sudo, who_message
from requirements_installer import install_library
install_library("aiohttp")
import aiohttp

@Client.on_message(zel_command("speedconfig", "SpeedTest", os.path.basename(__file__)) & zel_sudo())
async def speed_config(client, message):
    message = await who_message(client, message)
    await message.edit("✅ Speed Test uses English automatically. No language configuration is required.")

def format_speed(bytes_per_sec):
    if bytes_per_sec <= 0:
        return "0 Mbps"
    mbits = bytes_per_sec * 8 / (1024 * 1024)
    return f"{mbits:.1f} Mbps" if mbits >= 1 else f"{mbits * 1000:.1f} Kbps"

async def upload_test(session):
    data = b"0" * (1024 * 1024 * 10)
    start = time.time()
    async with session.post("https://speed.cloudflare.com/__up", data=data) as response:
        await response.read()
    duration = time.time() - start
    return len(data) / duration if duration > 0 else 0

async def measure_ping(session):
    start = time.time()
    async with session.get("https://www.google.com") as response:
        await response.read()
    return int((time.time() - start) * 1000)

async def get_network_info(session):
    try:
        async with session.get("https://ipinfo.io/json") as response:
            data = await response.json()
            return {"location": f"{data.get('city', 'N/A')}, {data.get('country', 'N/A')}", "org": data.get('org', 'N/A').removeprefix('AS')}
    except Exception:
        return {"location": "N/A", "org": "N/A"}

@Client.on_message(zel_command("speedtest", "SpeedTest", os.path.basename(__file__)) & zel_sudo())
async def speedtest_handler(client, message):
    message = await who_message(client, message)
    await message.edit("🔄 <b>Testing upload speed...</b>")
    start_time = time.time()
    try:
        timeout = aiohttp.ClientTimeout(total=30)
        async with aiohttp.ClientSession(timeout=timeout) as session:
            network = await get_network_info(session)
            ping = await measure_ping(session)
            upload_speed = await upload_test(session)
        duration = time.time() - start_time
        await message.edit(
            "<b>📊 Internet Upload Test</b>\n\n"
            f"<b>📤 Upload:</b> <code>{format_speed(upload_speed)}</code>\n"
            f"<b>🕒 Ping:</b> <code>{ping} ms</code>\n\n"
            f"<b>🌐 Server:</b> <code>{network['location']}</code>\n"
            f"<b>📡 Provider:</b> <code>{network['org']}</code>\n\n"
            f"<b>⌚ Test duration:</b> <code>{duration:.1f} sec</code>\n"
            f"<b>📅 Time:</b> <code>{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</code>"
        )
    except Exception as exc:
        await message.edit(f"❌ <b>Speed test failed:</b>\n<code>{exc}</code>")
