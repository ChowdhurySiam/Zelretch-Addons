"""Zelretch Addon: Systemd Manager

Safely manages systemd units on compatible Linux hosts and reports a clear
compatibility diagnosis inside Docker/Hugging Face environments.
"""

from __future__ import annotations

import asyncio
import html
import io
import json
import os
import platform
import re
import shutil
import subprocess
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from pyrogram import Client

from command import who_message, zel_command, zel_sudo
from requirements_installer import install_library

install_library("psutil>=6,<8")
import psutil


ZELRETCH_MODULE_INFO = {
    "title": "Systemd Manager",
    "icon": "⚙️",
    "category": "System",
    "description": (
        "Lists and manages systemd units on compatible Linux hosts, with "
        "clear Docker and Hugging Face compatibility diagnostics."
    ),
    "developer": "Siam Chowdhury",
    "github": "https://github.com/ChowdhurySiam",
    "telegram": "https://t.me/Ch0wdhury_Siam",
    "undo": ".delunit or .unit <unit> stop",
}

_CONFIG_PATH = Path("userdata/systemd_services.json")
_UNIT_PATTERN = re.compile(r"^[A-Za-z0-9_.@:-]{1,180}$")
_ALLOWED_ACTIONS = {
    "status",
    "start",
    "stop",
    "restart",
    "enable",
    "disable",
    "logs",
    "tail",
}


@dataclass(frozen=True)
class CommandResult:
    returncode: int
    stdout: str
    stderr: str

    @property
    def ok(self) -> bool:
        return self.returncode == 0


@dataclass(frozen=True)
class SystemdAvailability:
    available: bool
    reason: str
    systemctl: str | None
    journalctl: str | None


def _safe(value: Any, fallback: str = "Unavailable") -> str:
    text = str(value or "").strip() or fallback
    return html.escape(text)


def _normalize_unit(value: str) -> str:
    unit = value.strip()
    if not _UNIT_PATTERN.fullmatch(unit):
        raise ValueError("The unit name contains unsupported characters.")
    if "." not in unit.rsplit("/", 1)[-1]:
        unit += ".service"
    return unit


def _load_config() -> list[dict[str, str]]:
    try:
        data = json.loads(_CONFIG_PATH.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return []

    services: list[dict[str, str]] = []
    if not isinstance(data, list):
        return services
    seen: set[str] = set()
    for item in data:
        if not isinstance(item, dict):
            continue
        formal = str(item.get("formal") or "").strip()
        name = str(item.get("name") or formal).strip()
        if not formal or formal in seen:
            continue
        try:
            formal = _normalize_unit(formal)
        except ValueError:
            continue
        services.append({"formal": formal, "name": name or formal})
        seen.add(formal)
    return services


def _save_config(services: list[dict[str, str]]) -> None:
    _CONFIG_PATH.parent.mkdir(parents=True, exist_ok=True)
    temporary = _CONFIG_PATH.with_suffix(".json.tmp")
    temporary.write_text(
        json.dumps(services, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    temporary.replace(_CONFIG_PATH)


def _run(command: list[str], timeout: int = 20) -> CommandResult:
    try:
        completed = subprocess.run(
            command,
            check=False,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            timeout=timeout,
            env={**os.environ, "SYSTEMD_PAGER": "", "PAGER": "cat"},
        )
        return CommandResult(
            completed.returncode,
            completed.stdout.strip(),
            completed.stderr.strip(),
        )
    except subprocess.TimeoutExpired as exc:
        return CommandResult(124, (exc.stdout or "").strip(), "Command timed out.")
    except OSError as exc:
        return CommandResult(127, "", str(exc))


def _detect_systemd() -> SystemdAvailability:
    if platform.system() != "Linux":
        return SystemdAvailability(
            False,
            "Systemd is supported only on Linux hosts.",
            None,
            None,
        )

    systemctl = shutil.which("systemctl")
    journalctl = shutil.which("journalctl")
    if not systemctl:
        return SystemdAvailability(
            False,
            "The systemctl executable is not installed.",
            None,
            journalctl,
        )

    if not Path("/run/systemd/system").is_dir():
        environment = "Hugging Face Spaces/Docker" if os.environ.get("SPACE_ID") or os.environ.get("DOCKER") else "this environment"
        return SystemdAvailability(
            False,
            f"Systemd is not PID 1 in {environment}.",
            systemctl,
            journalctl,
        )

    result = _run([systemctl, "is-system-running"], timeout=8)
    accepted_states = {"running", "degraded", "starting", "maintenance"}
    state = result.stdout.strip().lower()
    if state in accepted_states:
        return SystemdAvailability(True, f"Systemd state: {state}", systemctl, journalctl)

    detail = result.stderr or result.stdout or "systemctl could not communicate with systemd."
    return SystemdAvailability(False, detail, systemctl, journalctl)


def _unsupported_text(availability: SystemdAvailability) -> str:
    return (
        "<b>⚙️ Systemd Manager</b>\n\n"
        "<b>Systemd is unavailable in this runtime.</b>\n"
        f"Reason: <code>{_safe(availability.reason)}</code>\n\n"
        "Hugging Face Spaces run inside Docker containers without systemd as PID 1. "
        "The manager works on a VPS or VM that boots with systemd. Restart the Space "
        "from the Hugging Face interface instead of using <code>systemctl</code>.\n\n"
        "Run <code>.systemdcheck</code> for environment details."
    )


def _systemctl(availability: SystemdAvailability, *arguments: str, timeout: int = 20) -> CommandResult:
    if not availability.available or not availability.systemctl:
        return CommandResult(1, "", availability.reason)
    return _run([availability.systemctl, "--no-pager", *arguments], timeout=timeout)


def _unit_exists(availability: SystemdAvailability, unit: str) -> tuple[bool, str]:
    result = _systemctl(availability, "show", unit, "--property=LoadState", "--value", timeout=10)
    state = result.stdout.strip().lower()
    if result.ok and state not in {"", "not-found"}:
        return True, state
    return False, result.stderr or result.stdout or "Unit not found."


def _unit_state(availability: SystemdAvailability, unit: str) -> str:
    result = _systemctl(availability, "is-active", unit, timeout=10)
    return result.stdout.strip().lower() or "unknown"


def _unit_pid(availability: SystemdAvailability, unit: str) -> int | None:
    result = _systemctl(
        availability,
        "show",
        unit,
        "--property=MainPID",
        "--value",
        timeout=10,
    )
    try:
        pid = int(result.stdout.strip())
        return pid if pid > 0 else None
    except ValueError:
        return None


def _resource_text(availability: SystemdAvailability, unit: str) -> str:
    pid = _unit_pid(availability, unit)
    if not pid:
        return ""
    try:
        process = psutil.Process(pid)
        memory = process.memory_info().rss / (1024 ** 2)
        cpu = process.cpu_percent(interval=0.1)
        return f" · {memory:.1f} MiB · {cpu:.1f}% CPU"
    except (psutil.Error, OSError):
        return ""


def _status_icon(status: str) -> str:
    return {
        "active": "🟢",
        "inactive": "⚪",
        "failed": "🔴",
        "activating": "🟡",
        "deactivating": "🟠",
    }.get(status, "❔")


def _diagnostic_text(availability: SystemdAvailability) -> str:
    pid_one = "Unavailable"
    try:
        pid_one = Path("/proc/1/comm").read_text(encoding="utf-8").strip()
    except OSError:
        pass
    return (
        "<b>⚙️ Systemd Compatibility Check</b>\n\n"
        f"• Available: <code>{'Yes' if availability.available else 'No'}</code>\n"
        f"• Platform: <code>{_safe(platform.platform())}</code>\n"
        f"• PID 1: <code>{_safe(pid_one)}</code>\n"
        f"• systemctl: <code>{_safe(availability.systemctl)}</code>\n"
        f"• journalctl: <code>{_safe(availability.journalctl)}</code>\n"
        f"• Detail: <code>{_safe(availability.reason)}</code>"
    )


@Client.on_message(
    zel_command("systemdcheck", "Systemd", os.path.basename(__file__))
    & zel_sudo()
)
async def systemd_check_handler(client, message):
    message = await who_message(client, message)
    availability = await asyncio.to_thread(_detect_systemd)
    await message.edit(_diagnostic_text(availability))


@Client.on_message(
    zel_command("units", "Systemd", os.path.basename(__file__))
    & zel_sudo()
)
async def units_handler(client, message):
    message = await who_message(client, message)
    availability = await asyncio.to_thread(_detect_systemd)
    if not availability.available:
        await message.edit(_unsupported_text(availability))
        return

    services = await asyncio.to_thread(_load_config)
    if not services:
        await message.edit(
            "<b>⚙️ Systemd Manager</b>\n\n"
            "No units are configured.\n"
            "Add one with <code>.addunit &lt;unit&gt; [display name]</code>."
        )
        return

    lines = ["<b>⚙️ Configured systemd units</b>", ""]
    for service in services:
        status = await asyncio.to_thread(_unit_state, availability, service["formal"])
        resources = await asyncio.to_thread(_resource_text, availability, service["formal"])
        lines.append(
            f"{_status_icon(status)} <b>{_safe(service['name'])}</b>\n"
            f"   <code>{_safe(service['formal'])}</code> · {_safe(status)}{_safe(resources, '')}"
        )
    await message.edit("\n".join(lines)[:4090])


@Client.on_message(
    zel_command(
        "addunit",
        "Systemd",
        os.path.basename(__file__),
        "[unit] [display name]",
    )
    & zel_sudo()
)
async def addunit_handler(client, message):
    message = await who_message(client, message)
    availability = await asyncio.to_thread(_detect_systemd)
    if not availability.available:
        await message.edit(_unsupported_text(availability))
        return

    raw = (getattr(message, "text", "") or "").split(maxsplit=1)
    if len(raw) < 2:
        await message.edit("Usage: <code>.addunit &lt;unit&gt; [display name]</code>")
        return
    pieces = raw[1].split(maxsplit=1)
    try:
        unit = _normalize_unit(pieces[0])
    except ValueError as exc:
        await message.edit(f"<b>❌ Invalid unit</b>\n<code>{_safe(exc)}</code>")
        return
    name = pieces[1].strip() if len(pieces) > 1 else unit

    exists, detail = await asyncio.to_thread(_unit_exists, availability, unit)
    if not exists:
        await message.edit(
            f"<b>❌ Unit not found</b>\n<code>{_safe(unit)}</code>\n\n"
            f"<code>{_safe(detail)}</code>"
        )
        return

    services = await asyncio.to_thread(_load_config)
    services = [item for item in services if item["formal"] != unit]
    services.append({"name": name, "formal": unit})
    services.sort(key=lambda item: item["name"].casefold())
    await asyncio.to_thread(_save_config, services)
    await message.edit(
        "<b>✅ Unit saved</b>\n\n"
        f"• Name: <code>{_safe(name)}</code>\n"
        f"• Unit: <code>{_safe(unit)}</code>"
    )


@Client.on_message(
    zel_command("delunit", "Systemd", os.path.basename(__file__), "[unit]")
    & zel_sudo()
)
async def delunit_handler(client, message):
    message = await who_message(client, message)
    raw = (getattr(message, "text", "") or "").split(maxsplit=1)
    if len(raw) < 2:
        await message.edit("Usage: <code>.delunit &lt;unit&gt;</code>")
        return
    try:
        unit = _normalize_unit(raw[1])
    except ValueError as exc:
        await message.edit(f"<b>❌ Invalid unit</b>\n<code>{_safe(exc)}</code>")
        return

    services = await asyncio.to_thread(_load_config)
    updated = [item for item in services if item["formal"] != unit]
    if len(updated) == len(services):
        await message.edit(f"Unit <code>{_safe(unit)}</code> is not saved.")
        return
    await asyncio.to_thread(_save_config, updated)
    await message.edit(f"<b>✅ Removed from the panel</b>\n<code>{_safe(unit)}</code>")


@Client.on_message(
    zel_command(
        "unit",
        "Systemd",
        os.path.basename(__file__),
        "[unit] [status|start|stop|restart|enable|disable|logs|tail]",
    )
    & zel_sudo()
)
async def unit_handler(client, message):
    message = await who_message(client, message)
    availability = await asyncio.to_thread(_detect_systemd)
    if not availability.available:
        await message.edit(_unsupported_text(availability))
        return

    raw = (getattr(message, "text", "") or "").split(maxsplit=1)
    if len(raw) < 2 or len(raw[1].split()) < 2:
        await message.edit(
            "Usage: <code>.unit &lt;unit&gt; "
            "&lt;status|start|stop|restart|enable|disable|logs|tail&gt;</code>"
        )
        return

    unit_raw, action = raw[1].split(maxsplit=1)
    action = action.strip().casefold()
    try:
        unit = _normalize_unit(unit_raw)
    except ValueError as exc:
        await message.edit(f"<b>❌ Invalid unit</b>\n<code>{_safe(exc)}</code>")
        return
    if action not in _ALLOWED_ACTIONS:
        await message.edit(
            f"<b>❌ Unsupported action:</b> <code>{_safe(action)}</code>\n"
            "Allowed: <code>status, start, stop, restart, enable, disable, logs, tail</code>"
        )
        return

    exists, detail = await asyncio.to_thread(_unit_exists, availability, unit)
    if not exists:
        await message.edit(
            f"<b>❌ Unit not found</b>\n<code>{_safe(unit)}</code>\n\n"
            f"<code>{_safe(detail)}</code>"
        )
        return

    if action == "status":
        result = await asyncio.to_thread(
            _systemctl,
            availability,
            "status",
            unit,
            "--lines=20",
            timeout=20,
        )
        output = result.stdout or result.stderr or "No status output."
        await message.edit(
            f"<b>⚙️ { _safe(unit) }</b>\n\n<pre>{_safe(output[-3500:])}</pre>"
        )
        return

    if action in {"logs", "tail"}:
        if not availability.journalctl:
            await message.edit("<b>❌ journalctl is not installed on this host.</b>")
            return
        lines = "40" if action == "tail" else "250"
        result = await asyncio.to_thread(
            _run,
            [
                availability.journalctl,
                "--no-pager",
                "--output=short-iso",
                "-u",
                unit,
                "-n",
                lines,
            ],
            25,
        )
        output = result.stdout or result.stderr or "No journal entries were returned."
        if action == "tail":
            await message.edit(
                f"<b>📜 { _safe(unit) } — recent logs</b>\n\n"
                f"<pre>{_safe(output[-3500:])}</pre>"
            )
            return

        document = io.BytesIO(output.encode("utf-8", errors="replace"))
        document.name = f"{unit}-logs.txt"
        await client.send_document(
            message.chat.id,
            document,
            caption=f"Systemd logs for {unit}",
            message_thread_id=getattr(message, "message_thread_id", None),
        )
        await message.edit(f"<b>✅ Exported logs for</b> <code>{_safe(unit)}</code>")
        return

    await message.edit(
        f"<b>⚙️ Running { _safe(action) } on { _safe(unit) }…</b>"
    )
    result = await asyncio.to_thread(
        _systemctl,
        availability,
        action,
        unit,
        timeout=35,
    )
    if not result.ok:
        await message.edit(
            f"<b>❌ systemctl { _safe(action) } failed</b>\n"
            f"Unit: <code>{_safe(unit)}</code>\n\n"
            f"<code>{_safe(result.stderr or result.stdout or 'Unknown error')}</code>"
        )
        return

    status = await asyncio.to_thread(_unit_state, availability, unit)
    await message.edit(
        f"<b>✅ Action completed</b>\n\n"
        f"• Unit: <code>{_safe(unit)}</code>\n"
        f"• Action: <code>{_safe(action)}</code>\n"
        f"• State: <code>{_safe(status)}</code>"
    )


@Client.on_message(
    zel_command(
        "nameunit",
        "Systemd",
        os.path.basename(__file__),
        "[unit] [new name]",
    )
    & zel_sudo()
)
async def nameunit_handler(client, message):
    message = await who_message(client, message)
    raw = (getattr(message, "text", "") or "").split(maxsplit=1)
    if len(raw) < 2 or len(raw[1].split()) < 2:
        await message.edit("Usage: <code>.nameunit &lt;unit&gt; &lt;new name&gt;</code>")
        return

    unit_raw, new_name = raw[1].split(maxsplit=1)
    try:
        unit = _normalize_unit(unit_raw)
    except ValueError as exc:
        await message.edit(f"<b>❌ Invalid unit</b>\n<code>{_safe(exc)}</code>")
        return

    services = await asyncio.to_thread(_load_config)
    found = False
    for service in services:
        if service["formal"] == unit:
            service["name"] = new_name.strip() or unit
            found = True
            break
    if not found:
        await message.edit(f"Unit <code>{_safe(unit)}</code> is not saved.")
        return

    services.sort(key=lambda item: item["name"].casefold())
    await asyncio.to_thread(_save_config, services)
    await message.edit(
        f"<b>✅ Unit renamed</b>\n"
        f"<code>{_safe(unit)}</code> → <code>{_safe(new_name)}</code>"
    )
