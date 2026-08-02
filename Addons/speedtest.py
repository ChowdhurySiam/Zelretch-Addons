"""Zelretch Addon: Speed Test

Runs a lightweight network test that works in Docker and Hugging Face Spaces.
"""

from __future__ import annotations

import asyncio
import html
import os
import statistics
import time
import uuid
from datetime import datetime, timezone
from typing import Any

from pyrogram import Client

from command import who_message, zel_command, zel_sudo
from requirements_installer import install_library

install_library("aiohttp>=3.10,<4")
import aiohttp


ZELRETCH_MODULE_INFO = {
    "title": "Speed Test",
    "icon": "🚀",
    "category": "System",
    "description": (
        "Measures latency, download speed, upload speed, network provider, and "
        "test duration using container-friendly HTTP endpoints."
    ),
    "developer": "Siam Chowdhury",
    "github": "https://github.com/ChowdhurySiam",
    "telegram": "https://t.me/Ch0wdhury_Siam",
    "undo": ".undo (reply to the Addon output)",
}

_CLOUDFLARE_BASE = "https://speed.cloudflare.com"
_DOWNLOAD_BYTES = 5 * 1024 * 1024
_UPLOAD_BYTES = 2 * 1024 * 1024
_HEADERS = {
    "User-Agent": "Zelretch-SpeedTest/2.0",
    "Cache-Control": "no-cache",
}


def _format_rate(bytes_per_second: float | None) -> str:
    if not bytes_per_second or bytes_per_second <= 0:
        return "Unavailable"
    megabits = bytes_per_second * 8 / 1_000_000
    if megabits >= 1:
        return f"{megabits:.2f} Mbps"
    return f"{megabits * 1000:.1f} Kbps"


def _safe(value: Any, fallback: str = "Unavailable") -> str:
    text = str(value or "").strip() or fallback
    return html.escape(text)


async def _request_latency(session: aiohttp.ClientSession) -> float:
    samples: list[float] = []
    for _ in range(3):
        started = time.perf_counter()
        url = f"{_CLOUDFLARE_BASE}/__down?bytes=1&cache={uuid.uuid4().hex}"
        async with session.get(url) as response:
            response.raise_for_status()
            await response.read()
        samples.append((time.perf_counter() - started) * 1000)
    return statistics.median(samples)


async def _download_test(session: aiohttp.ClientSession) -> float:
    url = (
        f"{_CLOUDFLARE_BASE}/__down?bytes={_DOWNLOAD_BYTES}"
        f"&cache={uuid.uuid4().hex}"
    )
    received = 0
    started = time.perf_counter()
    async with session.get(url) as response:
        response.raise_for_status()
        async for chunk in response.content.iter_chunked(128 * 1024):
            received += len(chunk)
    elapsed = time.perf_counter() - started
    return received / elapsed if received and elapsed > 0 else 0.0


async def _upload_test(session: aiohttp.ClientSession) -> float:
    payload = b"0" * _UPLOAD_BYTES
    started = time.perf_counter()
    async with session.post(
        f"{_CLOUDFLARE_BASE}/__up",
        data=payload,
        headers={"Content-Type": "application/octet-stream"},
    ) as response:
        response.raise_for_status()
        await response.read()
    elapsed = time.perf_counter() - started
    return len(payload) / elapsed if elapsed > 0 else 0.0


async def _network_info(session: aiohttp.ClientSession) -> dict[str, str]:
    result = {
        "ip": "Unavailable",
        "provider": "Unavailable",
        "location": "Unavailable",
    }

    try:
        async with session.get("https://ipinfo.io/json") as response:
            response.raise_for_status()
            data = await response.json(content_type=None)
        result["ip"] = str(data.get("ip") or result["ip"])
        organization = str(data.get("org") or result["provider"])
        if organization.startswith("AS") and " " in organization:
            organization = organization.split(" ", 1)[1]
        result["provider"] = organization
        city = str(data.get("city") or "").strip()
        region = str(data.get("region") or "").strip()
        country = str(data.get("country") or "").strip()
        result["location"] = ", ".join(
            part for part in (city, region, country) if part
        ) or result["location"]
        return result
    except Exception:
        pass

    try:
        async with session.get("https://www.cloudflare.com/cdn-cgi/trace") as response:
            response.raise_for_status()
            trace = await response.text()
        values = dict(
            line.split("=", 1)
            for line in trace.splitlines()
            if "=" in line
        )
        result["ip"] = values.get("ip", result["ip"])
        result["location"] = values.get("loc", result["location"])
    except Exception:
        pass
    return result


async def _run_speed_test() -> dict[str, Any]:
    timeout = aiohttp.ClientTimeout(total=55, connect=10, sock_read=35)
    connector = aiohttp.TCPConnector(ssl=True, limit=4, ttl_dns_cache=300)
    result: dict[str, Any] = {
        "latency_ms": None,
        "download_bps": None,
        "upload_bps": None,
        "network": {},
        "warnings": [],
    }

    async with aiohttp.ClientSession(
        timeout=timeout,
        connector=connector,
        headers=_HEADERS,
    ) as session:
        result["network"] = await _network_info(session)

        for key, operation, label in (
            ("latency_ms", _request_latency, "Latency"),
            ("download_bps", _download_test, "Download"),
            ("upload_bps", _upload_test, "Upload"),
        ):
            try:
                result[key] = await operation(session)
            except Exception as exc:
                result["warnings"].append(f"{label}: {type(exc).__name__}")

    return result


@Client.on_message(
    zel_command("speedconfig", "SpeedTest", os.path.basename(__file__))
    & zel_sudo()
)
async def speed_config(client, message):
    message = await who_message(client, message)
    await message.edit(
        "<b>🚀 Speed Test</b>\n\n"
        "The Addon uses lightweight Cloudflare test endpoints and automatically "
        "falls back to partial results when one measurement is unavailable.\n\n"
        "Command: <code>.speedtest</code>"
    )


@Client.on_message(
    zel_command("speedtest", "SpeedTest", os.path.basename(__file__))
    & zel_sudo()
)
async def speedtest_handler(client, message):
    message = await who_message(client, message)
    await message.edit(
        "<b>🚀 Running network test…</b>\n"
        "<i>This usually takes 10–30 seconds.</i>"
    )

    started = time.perf_counter()
    try:
        result = await _run_speed_test()
    except asyncio.CancelledError:
        raise
    except Exception as exc:
        await message.edit(
            "<b>❌ Speed test failed</b>\n\n"
            f"<code>{_safe(type(exc).__name__ + ': ' + str(exc))}</code>"
        )
        return

    duration = time.perf_counter() - started
    latency = result.get("latency_ms")
    latency_text = f"{latency:.0f} ms" if isinstance(latency, (int, float)) else "Unavailable"
    network = result.get("network") or {}
    warnings = result.get("warnings") or []

    text = (
        "<b>🚀 Network Speed Test</b>\n\n"
        "<b>Performance</b>\n"
        f"• Ping: <code>{_safe(latency_text)}</code>\n"
        f"• Download: <code>{_safe(_format_rate(result.get('download_bps')))}</code>\n"
        f"• Upload: <code>{_safe(_format_rate(result.get('upload_bps')))}</code>\n\n"
        "<b>Connection</b>\n"
        f"• Public IP: <code>{_safe(network.get('ip'))}</code>\n"
        f"• Provider: <code>{_safe(network.get('provider'))}</code>\n"
        f"• Location: <code>{_safe(network.get('location'))}</code>\n\n"
        "<b>Test details</b>\n"
        f"• Duration: <code>{duration:.1f} seconds</code>\n"
        f"• Time: <code>{datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M:%S UTC')}</code>"
    )

    if warnings:
        text += "\n\n<b>Partial-result notice</b>\n<code>" + _safe(
            "; ".join(warnings)
        ) + "</code>"

    await message.edit(text)
