"""Zelretch Addon: Gemini AI

Connects to Google Gemini for prompts, persistent conversations, model selection,
and local history control through the supported Google Gen AI SDK.

Category: AI & Automation
Maintainer: Siam Chowdhury
GitHub: https://github.com/ChowdhurySiam
Telegram: @Ch0wdhury_Siam
"""

from __future__ import annotations

import asyncio
import json
import os
from pathlib import Path
from typing import Any

from pyrogram import Client
from pyrogram.enums import ParseMode

from command import who_message, zel_command, zel_sudo
from requirements_installer import install_library

ZELRETCH_MODULE_INFO = {
    "title": "Gemini AI",
    "icon": "✨",
    "category": "AI & Automation",
    "description": "Uses the supported Google Gen AI SDK for prompts, conversations, model selection, and history control.",
    "undo": '.gemini_clear / .gemini_reset',
    "developer": "Siam Chowdhury",
    "github": "https://github.com/ChowdhurySiam",
    "telegram": "https://t.me/Ch0wdhury_Siam",
}

install_library("google-genai>=1,<2")
from google import genai  # noqa: E402
from google.genai import types  # noqa: E402

DATA_DIRECTORY = Path("userdata")
API_KEY_FILE = DATA_DIRECTORY / "gemini_api_key"
MODEL_FILE = DATA_DIRECTORY / "gemini_model"
HISTORY_FILE = DATA_DIRECTORY / "gemini_chat_history.json"
DEFAULT_MODEL = "gemini-2.5-flash"
MAX_TELEGRAM_TEXT = 3900


def _read_text(path: Path, default: str = "") -> str:
    try:
        value = path.read_text(encoding="utf-8").strip()
        return value or default
    except OSError:
        return default


def load_config() -> dict[str, str]:
    return {
        "api_key": (os.environ.get("GEMINI_API_KEY") or _read_text(API_KEY_FILE)).strip(),
        "model": _read_text(MODEL_FILE, DEFAULT_MODEL),
    }


def _load_history() -> list[types.Content]:
    try:
        raw = json.loads(HISTORY_FILE.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return []
    if not isinstance(raw, list):
        return []

    history: list[types.Content] = []
    for item in raw[-40:]:
        if not isinstance(item, dict):
            continue
        role = str(item.get("role") or "").strip().lower()
        if role not in {"user", "model"}:
            continue
        text = str(item.get("text") or "").strip()
        if not text:
            # Migrate the legacy {parts: [text]} representation.
            parts = item.get("parts")
            if isinstance(parts, list) and parts:
                first = parts[0]
                text = str(first.get("text") if isinstance(first, dict) else first).strip()
        if text:
            history.append(
                types.Content(
                    role=role,
                    parts=[types.Part.from_text(text=text)],
                )
            )
    return history


def _save_history(history: list[dict[str, str]]) -> None:
    DATA_DIRECTORY.mkdir(parents=True, exist_ok=True)
    HISTORY_FILE.write_text(
        json.dumps(history[-40:], ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )


def _history_records() -> list[dict[str, str]]:
    try:
        raw = json.loads(HISTORY_FILE.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return []
    records: list[dict[str, str]] = []
    if not isinstance(raw, list):
        return records
    for item in raw:
        if not isinstance(item, dict):
            continue
        role = str(item.get("role") or "").strip().lower()
        text = str(item.get("text") or "").strip()
        if not text:
            parts = item.get("parts")
            if isinstance(parts, list) and parts:
                first = parts[0]
                text = str(first.get("text") if isinstance(first, dict) else first).strip()
        if role in {"user", "model"} and text:
            records.append({"role": role, "text": text})
    return records[-40:]


async def _deliver_text(message: Any, text: str) -> None:
    clean = str(text or "").strip() or "Gemini returned an empty response."
    chunks = [clean[index : index + MAX_TELEGRAM_TEXT] for index in range(0, len(clean), MAX_TELEGRAM_TEXT)]
    if len(chunks) == 1:
        await message.edit(chunks[0], parse_mode=ParseMode.DISABLED)
        return
    await message.edit(chunks[0], parse_mode=ParseMode.DISABLED)
    for chunk in chunks[1:]:
        await message.reply(chunk, parse_mode=ParseMode.DISABLED)
        await asyncio.sleep(0.35)


async def _error(message: Any, error: BaseException) -> None:
    await message.edit(
        f"Gemini request failed: {type(error).__name__}: {error}",
        parse_mode=ParseMode.DISABLED,
    )


@Client.on_message(zel_command("gemini", "Gemini", os.path.basename(__file__), "[text]") & zel_sudo())
async def gemini_handler(client, message):
    message = await who_message(client, message)
    config = load_config()
    if not config["api_key"]:
        return await message.edit(
            "Gemini API key is not configured. Use .gemini_api [api_key] or set GEMINI_API_KEY.",
            parse_mode=ParseMode.DISABLED,
        )

    args = (message.text or "").split(maxsplit=1)
    if len(args) < 2:
        return await message.edit("Usage: .gemini [text]", parse_mode=ParseMode.DISABLED)

    try:
        async with genai.Client(api_key=config["api_key"]).aio as api_client:
            response = await api_client.models.generate_content(
                model=config["model"],
                contents=args[1],
            )
        await _deliver_text(message, response.text)
    except Exception as exc:
        await _error(message, exc)


@Client.on_message(zel_command("gemini_api", "Gemini", os.path.basename(__file__), "[api_key]") & zel_sudo())
async def gemini_api_handler(client, message):
    message = await who_message(client, message)
    args = (message.text or "").split(maxsplit=1)
    if len(args) < 2:
        return await message.edit("Usage: .gemini_api [api_key]", parse_mode=ParseMode.DISABLED)

    DATA_DIRECTORY.mkdir(parents=True, exist_ok=True)
    API_KEY_FILE.write_text(args[1].strip(), encoding="utf-8")
    await message.edit("Gemini API key saved securely in the MongoDB-synchronized runtime state.", parse_mode=ParseMode.DISABLED)


@Client.on_message(zel_command("gemini_model", "Gemini", os.path.basename(__file__), "[model]") & zel_sudo())
async def gemini_model_handler(client, message):
    message = await who_message(client, message)
    args = (message.text or "").split(maxsplit=1)
    if len(args) < 2:
        return await message.edit("Usage: .gemini_model [model]", parse_mode=ParseMode.DISABLED)

    model_name = args[1].strip()
    DATA_DIRECTORY.mkdir(parents=True, exist_ok=True)
    MODEL_FILE.write_text(model_name, encoding="utf-8")
    await message.edit(f"Gemini model set to: {model_name}", parse_mode=ParseMode.DISABLED)


@Client.on_message(zel_command("gemini_chat", "Gemini", os.path.basename(__file__), "[text]") & zel_sudo())
async def gemini_chat_handler(client, message):
    message = await who_message(client, message)
    config = load_config()
    if not config["api_key"]:
        return await message.edit(
            "Gemini API key is not configured. Use .gemini_api [api_key] or set GEMINI_API_KEY.",
            parse_mode=ParseMode.DISABLED,
        )

    args = (message.text or "").split(maxsplit=1)
    if len(args) < 2:
        return await message.edit("Usage: .gemini_chat [text]", parse_mode=ParseMode.DISABLED)

    query = args[1]
    try:
        history = _load_history()
        async with genai.Client(api_key=config["api_key"]).aio as api_client:
            chat = api_client.chats.create(model=config["model"], history=history)
            response = await chat.send_message(query)
        response_text = str(response.text or "").strip()
        records = _history_records()
        records.extend(
            [
                {"role": "user", "text": query},
                {"role": "model", "text": response_text},
            ]
        )
        _save_history(records)
        await _deliver_text(message, response_text)
    except Exception as exc:
        await _error(message, exc)


@Client.on_message(zel_command("gemini_clear", "Gemini", os.path.basename(__file__)) & zel_sudo())
async def gemini_clear_handler(client, message):
    message = await who_message(client, message)
    try:
        HISTORY_FILE.unlink()
        await message.edit("Gemini conversation history cleared.", parse_mode=ParseMode.DISABLED)
    except FileNotFoundError:
        await message.edit("Gemini conversation history is already empty.", parse_mode=ParseMode.DISABLED)
    except Exception as exc:
        await _error(message, exc)

@Client.on_message(zel_command("gemini_reset", "Gemini", os.path.basename(__file__)) & zel_sudo())
async def gemini_reset(client, message):
    message = await who_message(client, message)
    removed = []
    for path in (API_KEY_FILE, MODEL_FILE, HISTORY_FILE):
        if path.exists():
            path.unlink()
            removed.append(path.name)
    if removed:
        await message.edit("✅ Gemini saved configuration and chat history reset.")
    else:
        await message.edit("Gemini had no saved local configuration to reset.")
