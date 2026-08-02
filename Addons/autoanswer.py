"""Zelretch Addon: Auto Answer

Configures automatic replies using a selected message or post.

Category: Automation
Maintainer: Siam Chowdhury
GitHub: https://github.com/ChowdhurySiam
Telegram: @Ch0wdhury_Siam
"""

ZELRETCH_MODULE_INFO = {'title': 'Auto Answer', 'icon': '💬', 'category': 'Automation', 'description': 'Configures automatic replies using a selected message or post.', 'developer': 'Siam Chowdhury', 'github': 'https://github.com/ChowdhurySiam', 'telegram': 'https://t.me/Ch0wdhury_Siam', 'undo': '.unaws'}
import os
from pathlib import Path
from pyrogram import Client, filters
from command import zel_command, zel_sudo, who_message

if not os.path.exists("userdata/autoanswer_DB"):
    os.mkdir("userdata/autoanswer_DB")

def users():
    ignore = []
    i = os.listdir("userdata/autoanswer_DB")
    for list in i:
        ignore.append(int(list))
    return ignore

@Client.on_message(filters.private & ~filters.me & ~filters.bot)
async def aws(client, message):
    ids = message.from_user.id
    if Path(f"userdata/autoanswer").is_file():
        if not ids in users():
            with open(f"userdata/autoanswer", encoding="utf-8") as f:
                fromuser = str(ids)
                status = f.read().split()
                chat_ids = status[0]
                message_ids = status[1]
                await client.forward_messages(message.chat.id, str(chat_ids), int(message_ids))
                with open(f"userdata/autoanswer_DB/{fromuser}", "w+", encoding='utf-8') as w:
                    w.write(str(f"0"))
                    w.close()
            f.close()
    else:
        pass

@Client.on_message(zel_command("aws", "AutoAnswer", os.path.basename(__file__), "[ID/Username] [Post ID]") & zel_sudo())
async def aws_start(client, message):
    message = await who_message(client, message)
    try:
        chat_ids = message.text.split()[1]
        message_ids = message.text.split()[2]
        await message.edit(f"❕ AutoAnswer activated!.\n<b>💬 Chat id/tag:</b> {chat_ids}\n🆔 Message id: {message_ids}")
        with open(f"userdata/autoanswer", "w+", encoding='utf-8') as f:
            f.write(str(f"{chat_ids} {message_ids}"))
            f.close()
    except Exception as f:
        await message.edit(f"error {f}")

@Client.on_message(zel_command(["unaws", "aws_off"], "AutoAnswer", os.path.basename(__file__)) & zel_sudo())
async def aws_stop(client, message):
    message = await who_message(client, message)
    config_path = Path("userdata/autoanswer")
    database_path = Path("userdata/autoanswer_DB")
    changed = False
    if config_path.exists():
        config_path.unlink()
        changed = True
    if database_path.exists():
        for entry in database_path.iterdir():
            if entry.is_file():
                entry.unlink()
                changed = True
    await message.edit("✅ Auto Answer disabled and its handled-user cache cleared." if changed else "Auto Answer was already disabled.")
