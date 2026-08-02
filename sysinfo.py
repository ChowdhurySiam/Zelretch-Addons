"""Zelretch Addon: System Information

Displays CPU, memory, disk, platform, and runtime information.

Category: System
Maintainer: Siam Chowdhury
GitHub: https://github.com/ChowdhurySiam
Telegram: @Ch0wdhury_Siam
"""

ZELRETCH_MODULE_INFO = {'title': 'System Information', 'icon': '🖥️', 'category': 'System', 'description': 'Displays CPU, memory, disk, platform, and runtime information.', 'developer': 'Siam Chowdhury', 'github': 'https://github.com/ChowdhurySiam', 'telegram': 'https://t.me/Ch0wdhury_Siam'}

from pyrogram import Client, filters
from command import zel_command, zel_sudo, who_message
from requirements_installer import install_library
import os , socket
install_library("psutil -U") 

import psutil


@Client.on_message(zel_command("sysinfo", "SystemInfo", os.path.basename(__file__), "") & zel_sudo())
async def sysinfo(client, message):
    message = await who_message(client, message)
    try:
        memory_info = psutil.virtual_memory()
        total_memory = memory_info.total / (1024 ** 3)  
        used_memory = memory_info.used / (1024 ** 3)   
        free_memory = memory_info.free / (1024 ** 3)   

        cpu_count = psutil.cpu_count(logical=True)

        disk_info = psutil.disk_usage('/')
        total_disk = disk_info.total / (1024 ** 3) 
        used_disk = disk_info.used / (1024 ** 3) 
        free_disk = disk_info.free / (1024 ** 3) 

        hostname = socket.gethostname()
        ip_address = socket.gethostbyname(hostname)
        sys_info = (
            "<b>🖥 Информация о системе:</b>\n"
            f"<b>📍 Хост:</b> <code>{hostname}</code>\n"
            f"<b>🌐 IP-адрес:</b> <code>{ip_address}</code>\n"
            f"<b>🧠 Оперативная память:</b>\n"
            f" - Всего: <code>{total_memory:.2f} GB</code>\n"
            f" - Используется: <code>{used_memory:.2f} GB</code>\n"
            f" - Свободно: <code>{free_memory:.2f} GB</code>\n"
            f"<b>🔢 Количество ядер процессора:</b> <code>{cpu_count}</code>\n"
            f"<b>💽 Диск:</b>\n"
            f" - Всего: <code>{total_disk:.2f} GB</code>\n"
            f" - Используется: <code>{used_disk:.2f} GB</code>\n"
            f" - Свободно: <code>{free_disk:.2f} GB</code>"
        )

        await message.edit(sys_info)
    except Exception as e:
        await message.edit(f"<code>Ошибка при получении информации: {str(e)}</code>")
