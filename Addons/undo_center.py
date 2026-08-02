"""Zelretch Addon: Undo Center

Provides a universal way to remove the output of any Addon command.

Category: Utilities
Maintainer: Siam Chowdhury
GitHub: https://github.com/ChowdhurySiam
Telegram: @Ch0wdhury_Siam
"""

ZELRETCH_MODULE_INFO = {
    "title": "Undo Center",
    "icon": "↩️",
    "category": "Utilities",
    "description": "Removes a replied-to Addon output or a selected outgoing message.",
    "undo": ".undo (reply to the message)",
    "developer": "Siam Chowdhury",
    "github": "https://github.com/ChowdhurySiam",
    "telegram": "https://t.me/Ch0wdhury_Siam",
}

import os

from pyrogram import Client
from command import my_prefix, who_message, zel_command, zel_sudo


async def _resolve_target(client, message):
    if message.reply_to_message:
        return message.reply_to_message

    parts = (message.text or "").split(maxsplit=1)
    argument = parts[1].strip() if len(parts) > 1 else ""
    if argument.isdigit():
        return await client.get_messages(message.chat.id, int(argument))

    if argument.casefold() == "last":
        async for candidate in client.get_chat_history(message.chat.id, limit=25):
            if candidate.id == message.id:
                continue
            if getattr(candidate, "outgoing", False):
                return candidate
    return None


@Client.on_message(
    zel_command(
        ["undo", "revert"],
        "UndoCenter",
        os.path.basename(__file__),
        "[reply/message_id/last]",
    )
    & zel_sudo()
)
async def undo_command(client, message):
    message = await who_message(client, message)
    target = await _resolve_target(client, message)
    if target is None:
        return await message.edit(
            "↩️ <b>Undo usage</b>\n"
            f"• Reply: <code>{my_prefix()}undo</code>\n"
            f"• Message ID: <code>{my_prefix()}undo 12345</code>\n"
            f"• Previous outgoing message: <code>{my_prefix()}undo last</code>\n\n"
            "This removes Addon output. Telegram-side actions such as deleted messages, "
            "kicked members, sent spam, or redeemed promotions cannot be restored."
        )

    target_id = getattr(target, "id", None)
    try:
        await target.delete()
    except Exception as exc:
        return await message.edit(f"❌ Unable to undo that message: <code>{exc}</code>")

    if target_id != message.id:
        try:
            await message.delete()
        except Exception:
            await message.edit("✅ Addon output removed.")
