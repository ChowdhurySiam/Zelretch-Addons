"""Zelretch Addon: Systemd Manager

Lists and manages systemd units on compatible Linux hosts.

Category: System
Maintainer: Siam Chowdhury
GitHub: https://github.com/ChowdhurySiam
Telegram: @Ch0wdhury_Siam
"""

ZELRETCH_MODULE_INFO = {'title': 'Systemd Manager', 'icon': '⚙️', 'category': 'System', 'description': 'Lists and manages systemd units on compatible Linux hosts.', 'developer': 'Siam Chowdhury', 'github': 'https://github.com/ChowdhurySiam', 'telegram': 'https://t.me/Ch0wdhury_Siam'}

import asyncio
import io
import os
import subprocess
from pyrogram import Client, filters
from command import zel_command, zel_sudo, who_message

def human_readable_size(size: float, decimal_places: int = 2) -> str:
    for unit in ["B", "K", "M", "G", "T", "P"]:
        if size < 1024.0 or unit == "P":
            break
        size /= 1024.0
    return f"{size:.{decimal_places}f} {unit}"

def load_config():
    try:
        with open("userdata/systemd_services.json", "r", encoding="utf-8") as f:
            import json
            return json.load(f)
    except FileNotFoundError:
        return []

def save_config(services):
    import json
    with open("userdata/systemd_services.json", "w", encoding="utf-8") as f:
        json.dump(services, f, ensure_ascii=False, indent=2)

def get_unit_status_text(unit: str) -> str:
    return (
        subprocess.run(
            [
                "sudo",
                "-S",
                "systemctl",
                "is-active",
                unit,
            ],
            check=False,
            stdout=subprocess.PIPE,
        )
        .stdout.decode()
        .strip()
    )

def is_running(unit: str) -> bool:
    return get_unit_status_text(unit) == "active"

def unit_exists(unit: str) -> bool:
    return (
        subprocess.run(
            [
                "sudo",
                "-S",
                "systemctl",
                "cat",
                unit,
            ],
            check=False,
            stdout=subprocess.PIPE,
        ).returncode
        == 0
    )

def get_unit_pid(unit: str) -> str:
    return (
        subprocess.run(
            [
                "sudo",
                "-S",
                "systemctl",
                "show",
                unit,
                "--property=MainPID",
                "--value",
            ],
            check=False,
            stdout=subprocess.PIPE,
        )
        .stdout.decode()
        .strip()
    )

def get_unit_resources_consumption(unit: str) -> str:
    if not is_running(unit):
        return ""

    try:
        pid = get_unit_pid(unit)
        ram_raw = subprocess.run(
            [
                "ps",
                "-p",
                pid,
                "-o",
                "rss",
            ],
            check=False,
            stdout=subprocess.PIPE,
        ).stdout.decode().strip().split("\n")[1]
        
        ram = human_readable_size(int(ram_raw) * 1024)
        
        cpu = (
            subprocess.run(
                [
                    "ps",
                    "-p",
                    pid,
                    "-o",
                    r"%cpu",
                ],
                check=False,
                stdout=subprocess.PIPE,
            )
            .stdout.decode()
            .strip()
            .split("\n")[1]
            + "%"
        )

        return f" | 📟 <code>{ram}</code> | 🗃 <code>{cpu}</code>"
    except Exception:
        return ""

def get_unit_status_emoji(unit: str) -> str:
    status = get_unit_status_text(unit)
    if status == "active":
        return "🍏"
    elif status == "inactive":
        return "🍎"
    elif status == "failed":
        return "🚫"
    elif status == "activating":
        return "🔄"
    else:
        return "❓"

@Client.on_message(zel_command("units", "Systemd", os.path.basename(__file__)) & zel_sudo())
async def units_handler(client, message):
    message = await who_message(client, message)
    services = load_config()
    
    if not services:
        await message.edit("<emoji id=5771858080664915483>🎛</emoji> <b>No units configured</b>")
        return
        
    panel_text = "<emoji id=5771858080664915483>🎛</emoji> <b>Here you can control your systemd units</b>\n\n"
    for service in services:
        status = get_unit_status_text(service["formal"])
        resources = get_unit_resources_consumption(service["formal"])
        panel_text += f"{get_unit_status_emoji(service['formal'])} <b>{service['name']}</b> (<code>{service['formal']}</code>): {status}{resources}\n"
    
    await message.edit(panel_text)

@Client.on_message(zel_command("addunit", "Systemd", os.path.basename(__file__), "[unit] [name]") & zel_sudo())
async def addunit_handler(client, message):
    message = await who_message(client, message)
    args = message.text.split(maxsplit=1)
    if len(args) < 2:
        await message.edit("<emoji id=5312526098750252863>🚫</emoji> <b>No arguments specified</b>")
        return

    try:
        unit, name = args[1].split(maxsplit=1)
    except ValueError:
        unit = args[1]
        name = args[1]

    if not unit_exists(unit):
        await message.edit(f"<emoji id=5312526098750252863>🚫</emoji> <b>Unit</b> <code>{unit}</code> <b>doesn't exist!</b>")
        return

    services = load_config()
    services.append({"name": name, "formal": unit})
    save_config(services)
    
    await message.edit(f"<emoji id=5314250708508220914>✅</emoji> <b>Unit </b><code>{unit}</code><b> with name </b><code>{name}</code><b> added</b>")

@Client.on_message(zel_command("delunit", "Systemd", os.path.basename(__file__), "[unit]") & zel_sudo())
async def delunit_handler(client, message):
    message = await who_message(client, message)
    args = message.text.split(maxsplit=1)
    if len(args) < 2:
        await message.edit("<emoji id=5312526098750252863>🚫</emoji> <b>No arguments specified</b>")
        return

    unit = args[1]
    services = load_config()
    
    if not any(s["formal"] == unit for s in services):
        await message.edit(f"<emoji id=5312526098750252863>🚫</emoji> <b>Unit</b> <code>{unit}</code> <b>doesn't exist!</b>")
        return

    services = [s for s in services if s["formal"] != unit]
    save_config(services)
    
    await message.edit(f"<emoji id=5314250708508220914>✅</emoji> <b>Unit </b><code>{unit}</code><b> removed</b>")

@Client.on_message(zel_command("unit", "Systemd", os.path.basename(__file__), "[unit] [action]") & zel_sudo())
async def unit_handler(client, message):
    message = await who_message(client, message)
    args = message.text.split(maxsplit=1)
    if len(args) < 2 or len(args[1].split()) < 2:
        await message.edit("<emoji id=5312526098750252863>🚫</emoji> <b>No arguments specified</b>")
        return

    unit, action = args[1].split(maxsplit=1)
    
    if not unit_exists(unit):
        await message.edit(f"<emoji id=5312526098750252863>🚫</emoji> <b>Unit</b> <code>{unit}</code> <b>doesn't exist!</b>")
        return

    if action in {"start", "stop", "restart", "logs", "tail"}:
        if action == "start":
            subprocess.run(["sudo", "-S", "systemctl", "start", unit], check=True)
        elif action == "stop":
            subprocess.run(["sudo", "-S", "systemctl", "stop", unit], check=True)
        elif action == "restart":
            subprocess.run(["sudo", "-S", "systemctl", "restart", unit], check=True)
        elif action in {"logs", "tail"}:
            logs = subprocess.run(
                [
                    "sudo",
                    "-S",
                    "journalctl",
                    "-u",
                    unit,
                    "-n",
                    "1000",
                ],
                check=True,
                stdout=subprocess.PIPE,
            ).stdout.decode().strip()

            hostname = subprocess.run(["hostname"], check=True, stdout=subprocess.PIPE).stdout.decode().strip()
            logs = logs.replace(f"{hostname} ", "")
            logs = logs.replace("[" + str(get_unit_pid(unit)) + "]", "")

            if action == "logs":
                log_file = io.BytesIO(logs.encode())
                log_file.name = f"{unit}-logs.txt"
                await client.send_document(message.chat.id, log_file, message_thread_id=message.message_thread_id)
            else:
                actual_logs = ""
                logs_list = list(reversed(logs.splitlines()))
                while logs_list:
                    chunk = f"{logs_list.pop()}\n"
                    if len(actual_logs + chunk) >= 4096:
                        break
                    actual_logs += chunk
                
                await message.edit(f"<code>{actual_logs}</code>")
                return
        
        await message.edit(f"<emoji id=5314250708508220914>✅</emoji> <b>Action </b><code>{action}</code><b> performed on unit </b><code>{unit}</code>")
    else:
        await message.edit(f"<emoji id=5312526098750252863>🚫</emoji> <b>Action </b><code>{action}</code><b> not found</b>")

@Client.on_message(zel_command("nameunit", "Systemd", os.path.basename(__file__), "[unit] [new_name]") & zel_sudo())
async def nameunit_handler(client, message):
    message = await who_message(client, message)
    args = message.text.split(maxsplit=1)
    if len(args) < 2 or len(args[1].split()) < 2:
        await message.edit("<emoji id=5312526098750252863>🚫</emoji> <b>No arguments specified</b>")
        return

    unit, new_name = args[1].split(maxsplit=1)
    services = load_config()
    
    if not any(s["formal"] == unit for s in services):
        await message.edit(f"<emoji id=5312526098750252863>🚫</emoji> <b>Unit</b> <code>{unit}</code> <b>doesn't exist!</b>")
        return

    services = [s for s in services if s["formal"] != unit] + [{"name": new_name, "formal": unit}]
    save_config(services)
    
    await message.edit(f"<emoji id=5314250708508220914>✅</emoji> <b>Unit </b><code>{unit}</code><b> renamed to </b><code>{new_name}</code>")
