"""Zelretch Addon: Member Cleanup

Performs bulk member cleanup actions in chats where you have permission.
Every cleanup action requires an explicit CONFIRM message before it starts.

Category: Administration
Maintainer: Siam Chowdhury
GitHub: https://github.com/ChowdhurySiam
Telegram: @Ch0wdhury_Siam
"""

from __future__ import annotations

import asyncio
import os
import time
from dataclasses import dataclass
from datetime import datetime, timedelta
from typing import Any

from pyrogram import Client, filters
from pyrogram.errors import FloodWait

from command import who_message, zel_command, zel_sudo


ZELRETCH_MODULE_INFO = {
    "title": "Member Cleanup",
    "icon": "🧹",
    "category": "Administration",
    "description": (
        "Performs bulk member cleanup actions after an explicit CONFIRM step."
    ),
    "developer": "Siam Chowdhury",
    "github": "https://github.com/ChowdhurySiam",
    "telegram": "https://t.me/Ch0wdhury_Siam",
    "undo": (
        ".undo removes only the status output; removed members cannot be restored"
    ),
    "confirmation": "Type CONFIRM in the same chat within 60 seconds",
}

MODULE_NAME = "MemberCleanup"
FILENAME = os.path.basename(__file__)
CONFIRMATION_TIMEOUT_SECONDS = 60


@dataclass
class PendingCleanup:
    action: str
    requester_key: str
    status_message: Any
    expires_at: float
    token: int


_PENDING_CLEANUPS: dict[int, PendingCleanup] = {}
_PENDING_LOCK = asyncio.Lock()
_TOKEN_COUNTER = 0

_ACTION_LABELS = {
    "kickall": "Remove all removable members",
    "kickall_hide": "Remove all removable members and hide the result",
    "kickall_withbot": "Send moderation-bot ban commands for members",
    "kickdeleted": "Remove deleted accounts",
}


def _chat_id(message: Any) -> int:
    return int(message.chat.id)


def _actor_key(message: Any) -> str:
    from_user = getattr(message, "from_user", None)
    if from_user is not None and getattr(from_user, "id", None) is not None:
        return f"user:{int(from_user.id)}"
    sender_chat = getattr(message, "sender_chat", None)
    if sender_chat is not None and getattr(sender_chat, "id", None) is not None:
        return f"chat:{int(sender_chat.id)}"
    return f"chat:{_chat_id(message)}"


async def _safe_edit(message: Any, text: str) -> None:
    try:
        await message.edit(text)
    except Exception:
        try:
            await message.reply(text)
        except Exception:
            pass


async def _safe_delete(client: Client, message: Any) -> None:
    try:
        await client.delete_messages(_chat_id(message), message.id)
    except Exception:
        try:
            await message.delete()
        except Exception:
            pass


async def _expire_confirmation(chat_id: int, token: int) -> None:
    await asyncio.sleep(CONFIRMATION_TIMEOUT_SECONDS)
    async with _PENDING_LOCK:
        pending = _PENDING_CLEANUPS.get(chat_id)
        if pending is None or pending.token != token:
            return
        _PENDING_CLEANUPS.pop(chat_id, None)
    await _safe_edit(
        pending.status_message,
        "⌛ Member Cleanup confirmation expired.\n\nRun the cleanup command again if it is still required.",
    )


async def _request_confirmation(client: Client, original_message: Any, action: str) -> None:
    global _TOKEN_COUNTER

    requester_key = _actor_key(original_message)
    status_message = await who_message(client, original_message)
    chat_id = _chat_id(original_message)

    async with _PENDING_LOCK:
        _TOKEN_COUNTER += 1
        token = _TOKEN_COUNTER
        previous = _PENDING_CLEANUPS.get(chat_id)
        _PENDING_CLEANUPS[chat_id] = PendingCleanup(
            action=action,
            requester_key=requester_key,
            status_message=status_message,
            expires_at=time.monotonic() + CONFIRMATION_TIMEOUT_SECONDS,
            token=token,
        )

    if previous is not None and previous.status_message is not status_message:
        await _safe_edit(
            previous.status_message,
            "Cancelled because a newer Member Cleanup request replaced it.",
        )

    await _safe_edit(
        status_message,
        (
            "⚠️ MEMBER CLEANUP CONFIRMATION\n\n"
            f"Action: {_ACTION_LABELS[action]}\n\n"
            "This can remove many members and cannot be undone.\n"
            f"Type the exact text CONFIRM in this chat within "
            f"{CONFIRMATION_TIMEOUT_SECONDS} seconds to continue.\n\n"
            "Anything else leaves the chat unchanged."
        ),
    )
    asyncio.create_task(_expire_confirmation(chat_id, token))


async def _ban_member(client: Client, chat_id: int, user_id: int, until_date: Any = 0) -> bool:
    for attempt in range(2):
        try:
            await client.ban_chat_member(chat_id, user_id, until_date)
            return True
        except FloodWait as exc:
            if attempt == 0:
                await asyncio.sleep(max(1, int(getattr(exc, "value", 1))))
                continue
            return False
        except Exception:
            return False
    return False


async def _update_progress(status_message: Any, action: str, processed: int, changed: int) -> None:
    if processed % 50 != 0:
        return
    await _safe_edit(
        status_message,
        (
            "🧹 MEMBER CLEANUP IN PROGRESS\n\n"
            f"Action: {_ACTION_LABELS[action]}\n"
            f"Processed: {processed}\n"
            f"Completed: {changed}"
        ),
    )


async def _execute_cleanup(client: Client, pending: PendingCleanup, chat_id: int) -> tuple[int, int, int]:
    me = await client.get_me()
    processed = changed = skipped = 0

    members = client.get_chat_members(chat_id)
    async for member in members:
        user = getattr(member, "user", None)
        user_id = getattr(user, "id", None)
        if user_id is None:
            skipped += 1
            continue
        if int(user_id) == int(me.id):
            skipped += 1
            continue

        if pending.action == "kickdeleted" and not bool(getattr(user, "is_deleted", False)):
            continue

        processed += 1
        success = False
        if pending.action == "kickall_withbot":
            try:
                mention = getattr(user, "mention", None) or str(user_id)
                await client.send_message(chat_id, f"/ban {mention}")
                success = True
            except FloodWait as exc:
                await asyncio.sleep(max(1, int(getattr(exc, "value", 1))))
                try:
                    mention = getattr(user, "mention", None) or str(user_id)
                    await client.send_message(chat_id, f"/ban {mention}")
                    success = True
                except Exception:
                    success = False
            except Exception:
                success = False
        else:
            until_date = (
                datetime.now() + timedelta(days=1)
                if pending.action == "kickdeleted"
                else 0
            )
            success = await _ban_member(client, chat_id, int(user_id), until_date)

        if success:
            changed += 1
        else:
            skipped += 1

        await _update_progress(
            pending.status_message,
            pending.action,
            processed,
            changed,
        )
        await asyncio.sleep(0.05)

    return processed, changed, skipped


async def _begin_cleanup(client: Client, confirmation_message: Any) -> None:
    chat_id = _chat_id(confirmation_message)
    actor_key = _actor_key(confirmation_message)

    async with _PENDING_LOCK:
        pending = _PENDING_CLEANUPS.get(chat_id)
        if pending is None:
            return
        if pending.expires_at <= time.monotonic():
            _PENDING_CLEANUPS.pop(chat_id, None)
            expired = True
        elif pending.requester_key != actor_key:
            expired = False
            pending = None
        else:
            _PENDING_CLEANUPS.pop(chat_id, None)
            expired = False

    if pending is None:
        return
    if expired:
        await _safe_edit(
            pending.status_message,
            "⌛ Member Cleanup confirmation expired. Run the command again.",
        )
        return

    await _safe_delete(client, confirmation_message)
    await _safe_edit(
        pending.status_message,
        (
            "✅ CONFIRMED\n\n"
            f"Starting: {_ACTION_LABELS[pending.action]}\n"
            "Do not repeat the command while this operation is running."
        ),
    )

    try:
        processed, changed, skipped = await _execute_cleanup(client, pending, chat_id)
        result = (
            "✅ MEMBER CLEANUP COMPLETE\n\n"
            f"Action: {_ACTION_LABELS[pending.action]}\n"
            f"Processed: {processed}\n"
            f"Completed: {changed}\n"
            f"Skipped/failed: {skipped}\n\n"
            "Removed members cannot be restored automatically."
        )
        await _safe_edit(pending.status_message, result)
        if pending.action == "kickall_hide":
            await asyncio.sleep(5)
            await _safe_delete(client, pending.status_message)
    except Exception as exc:
        await _safe_edit(
            pending.status_message,
            f"❌ Member Cleanup stopped because of an error:\n{exc}",
        )


@Client.on_message(
    zel_command("kickall", MODULE_NAME, FILENAME) & zel_sudo()
)
async def request_kickall(client: Client, message: Any) -> None:
    await _request_confirmation(client, message, "kickall")


@Client.on_message(
    zel_command("kickall_hide", MODULE_NAME, FILENAME) & zel_sudo()
)
async def request_kickall_hidden(client: Client, message: Any) -> None:
    await _request_confirmation(client, message, "kickall_hide")


@Client.on_message(
    zel_command("kickall_withbot", MODULE_NAME, FILENAME) & zel_sudo()
)
async def request_kickall_with_bot(client: Client, message: Any) -> None:
    await _request_confirmation(client, message, "kickall_withbot")


@Client.on_message(
    zel_command("kickdeleted", MODULE_NAME, FILENAME) & zel_sudo()
)
async def request_deleted_cleanup(client: Client, message: Any) -> None:
    await _request_confirmation(client, message, "kickdeleted")


@Client.on_message(filters.regex(r"^CONFIRM$") & zel_sudo())
async def confirm_member_cleanup(client: Client, message: Any) -> None:
    """Start the pending cleanup only after the exact uppercase confirmation."""

    await _begin_cleanup(client, message)
