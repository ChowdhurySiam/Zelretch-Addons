"""Zelretch Addon: System Information

Displays container-aware CPU, memory, disk, platform, and runtime information.
"""

from __future__ import annotations

import asyncio
import html
import os
import platform
import socket
import sys
import time
from pathlib import Path
from typing import Any

from pyrogram import Client

from command import who_message, zel_command, zel_sudo
from requirements_installer import install_library

install_library("psutil>=6,<8")
import psutil


ZELRETCH_MODULE_INFO = {
    "title": "System Information",
    "icon": "🖥️",
    "category": "System",
    "description": (
        "Displays container-aware CPU, memory, disk, platform, process, and "
        "runtime information."
    ),
    "developer": "Siam Chowdhury",
    "github": "https://github.com/ChowdhurySiam",
    "telegram": "https://t.me/Ch0wdhury_Siam",
    "undo": ".undo (reply to the Addon output)",
}

_GIB = 1024 ** 3


def _safe(value: Any, fallback: str = "Unavailable") -> str:
    text = str(value or "").strip() or fallback
    return html.escape(text)


def _format_bytes(value: int | float | None) -> str:
    if value is None or value < 0:
        return "Unavailable"
    size = float(value)
    units = ("B", "KiB", "MiB", "GiB", "TiB")
    for unit in units:
        if size < 1024 or unit == units[-1]:
            return f"{size:.2f} {unit}" if unit != "B" else f"{int(size)} B"
        size /= 1024
    return f"{size:.2f} TiB"


def _read_int(path: str) -> int | None:
    try:
        value = Path(path).read_text(encoding="utf-8").strip()
        if value in {"", "max"}:
            return None
        return int(value)
    except (OSError, ValueError):
        return None


def _container_memory() -> tuple[int | None, int | None]:
    # cgroup v2
    limit = _read_int("/sys/fs/cgroup/memory.max")
    used = _read_int("/sys/fs/cgroup/memory.current")
    if limit is not None and limit >= 1 << 60:
        limit = None
    if limit is not None or used is not None:
        return limit, used

    # cgroup v1
    limit = _read_int("/sys/fs/cgroup/memory/memory.limit_in_bytes")
    used = _read_int("/sys/fs/cgroup/memory/memory.usage_in_bytes")
    if limit is not None and limit >= 1 << 60:
        limit = None
    return limit, used


def _container_cpu_limit() -> float | None:
    try:
        quota_raw, period_raw = Path("/sys/fs/cgroup/cpu.max").read_text(
            encoding="utf-8"
        ).split(maxsplit=1)
        if quota_raw != "max":
            quota = int(quota_raw)
            period = int(period_raw)
            if quota > 0 and period > 0:
                return quota / period
    except (OSError, ValueError):
        pass

    quota = _read_int("/sys/fs/cgroup/cpu/cpu.cfs_quota_us")
    period = _read_int("/sys/fs/cgroup/cpu/cpu.cfs_period_us")
    if quota and period and quota > 0 and period > 0:
        return quota / period
    return None


def _local_ip() -> str:
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        sock.connect(("1.1.1.1", 80))
        return str(sock.getsockname()[0])
    except OSError:
        try:
            return socket.gethostbyname(socket.gethostname())
        except OSError:
            return "Unavailable"
    finally:
        sock.close()


def _cpu_model() -> str:
    model = platform.processor().strip()
    if model:
        return model
    try:
        for line in Path("/proc/cpuinfo").read_text(
            encoding="utf-8", errors="replace"
        ).splitlines():
            if line.lower().startswith("model name") and ":" in line:
                return line.split(":", 1)[1].strip()
    except OSError:
        pass
    return "Unavailable"


def _format_uptime(seconds: float) -> str:
    total = max(0, int(seconds))
    days, remainder = divmod(total, 86400)
    hours, remainder = divmod(remainder, 3600)
    minutes, secs = divmod(remainder, 60)
    if days:
        return f"{days}d {hours:02d}:{minutes:02d}:{secs:02d}"
    return f"{hours:02d}:{minutes:02d}:{secs:02d}"


def _collect_system_info() -> dict[str, Any]:
    virtual_memory = psutil.virtual_memory()
    disk = psutil.disk_usage(str(Path.cwd()))
    process = psutil.Process(os.getpid())
    cpu_percent = psutil.cpu_percent(interval=0.5)
    process_cpu = process.cpu_percent(interval=0.2)
    process_memory = process.memory_info().rss
    cgroup_limit, cgroup_used = _container_memory()
    cpu_limit = _container_cpu_limit()

    try:
        load_1, load_5, load_15 = os.getloadavg()
        load_average = f"{load_1:.2f}, {load_5:.2f}, {load_15:.2f}"
    except (AttributeError, OSError):
        load_average = "Unavailable"

    return {
        "hostname": socket.gethostname(),
        "ip": _local_ip(),
        "platform": f"{platform.system()} {platform.release()}",
        "architecture": platform.machine() or "Unavailable",
        "python": platform.python_version(),
        "cpu_model": _cpu_model(),
        "cpu_logical": psutil.cpu_count(logical=True) or 0,
        "cpu_physical": psutil.cpu_count(logical=False) or 0,
        "cpu_percent": cpu_percent,
        "cpu_limit": cpu_limit,
        "load_average": load_average,
        "memory_total": virtual_memory.total,
        "memory_used": virtual_memory.used,
        "memory_available": virtual_memory.available,
        "memory_percent": virtual_memory.percent,
        "container_memory_limit": cgroup_limit,
        "container_memory_used": cgroup_used,
        "disk_total": disk.total,
        "disk_used": disk.used,
        "disk_free": disk.free,
        "disk_percent": disk.percent,
        "system_uptime": time.time() - psutil.boot_time(),
        "process_uptime": time.time() - process.create_time(),
        "process_memory": process_memory,
        "process_cpu": process_cpu,
        "pid": process.pid,
    }


@Client.on_message(
    zel_command("sysinfo", "SystemInfo", os.path.basename(__file__))
    & zel_sudo()
)
async def sysinfo(client, message):
    message = await who_message(client, message)
    await message.edit("<b>🖥️ Collecting system information…</b>")

    try:
        info = await asyncio.to_thread(_collect_system_info)
    except asyncio.CancelledError:
        raise
    except Exception as exc:
        await message.edit(
            "<b>❌ System information failed</b>\n\n"
            f"<code>{_safe(type(exc).__name__ + ': ' + str(exc))}</code>"
        )
        return

    cpu_limit = info["cpu_limit"]
    cpu_limit_text = f"{cpu_limit:.2f} cores" if cpu_limit else "Not detected"
    container_limit = info["container_memory_limit"]
    container_used = info["container_memory_used"]

    text = (
        "<b>🖥️ System Information</b>\n\n"
        "<b>Host</b>\n"
        f"• Hostname: <code>{_safe(info['hostname'])}</code>\n"
        f"• Local IP: <code>{_safe(info['ip'])}</code>\n"
        f"• Platform: <code>{_safe(info['platform'])}</code>\n"
        f"• Architecture: <code>{_safe(info['architecture'])}</code>\n"
        f"• Python: <code>{_safe(info['python'])}</code>\n\n"
        "<b>CPU</b>\n"
        f"• Model: <code>{_safe(info['cpu_model'])}</code>\n"
        f"• Cores: <code>{info['cpu_physical']} physical / {info['cpu_logical']} logical</code>\n"
        f"• Current usage: <code>{info['cpu_percent']:.1f}%</code>\n"
        f"• Container quota: <code>{_safe(cpu_limit_text)}</code>\n"
        f"• Load average: <code>{_safe(info['load_average'])}</code>\n\n"
        "<b>Memory</b>\n"
        f"• System: <code>{_format_bytes(info['memory_used'])} / {_format_bytes(info['memory_total'])} ({info['memory_percent']:.1f}%)</code>\n"
        f"• Available: <code>{_format_bytes(info['memory_available'])}</code>\n"
    )

    if container_limit or container_used:
        text += (
            f"• Container: <code>{_format_bytes(container_used)} / "
            f"{_format_bytes(container_limit)}</code>\n"
        )

    text += (
        "\n<b>Storage</b>\n"
        f"• Used: <code>{_format_bytes(info['disk_used'])} / {_format_bytes(info['disk_total'])} ({info['disk_percent']:.1f}%)</code>\n"
        f"• Free: <code>{_format_bytes(info['disk_free'])}</code>\n\n"
        "<b>Zelretch process</b>\n"
        f"• PID: <code>{info['pid']}</code>\n"
        f"• Memory: <code>{_format_bytes(info['process_memory'])}</code>\n"
        f"• CPU: <code>{info['process_cpu']:.1f}%</code>\n"
        f"• Process uptime: <code>{_format_uptime(info['process_uptime'])}</code>\n"
        f"• System uptime: <code>{_format_uptime(info['system_uptime'])}</code>"
    )

    await message.edit(text)
