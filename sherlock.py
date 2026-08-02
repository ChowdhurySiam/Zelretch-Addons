"""Zelretch Addon: Username Search

Checks a username or identifier across supported public services.

Category: Information
Maintainer: Siam Chowdhury
GitHub: https://github.com/ChowdhurySiam
Telegram: @Ch0wdhury_Siam
"""

ZELRETCH_MODULE_INFO = {'title': 'Username Search', 'icon': '🕵️', 'category': 'Information', 'description': 'Checks a username or identifier across supported public services.', 'developer': 'Siam Chowdhury', 'github': 'https://github.com/ChowdhurySiam', 'telegram': 'https://t.me/Ch0wdhury_Siam'}

import asyncio
from pyrogram import Client, filters
from command import zel_command, zel_sudo, who_message
import os
import re

bot_tag = "shdjkwemnenennnbot"

def normalize_query(query: str) -> str:
    """
    Обрабатывает запрос:
    - если это Telegram ID без tgID — добавляет tgID
    - если пользователь уже указал tgID или tg — не трогаем
    """
    query = query.strip()

    # Не обрабатываем, если уже указан tgID или tg
    if re.match(r"^(tgID|tg)\s?\d{7,12}$", query, re.IGNORECASE):
        return query

    # Если просто ID (7-12 цифр), добавим tgID
    if re.fullmatch(r"\d{7,12}", query):
        return f"tgID {query}"

    return query

@Client.on_message(zel_command("sher", "Sherlock", os.path.basename(__file__), "[query]") & zel_sudo())
async def sherlock_search(client, message):
    message = await who_message(client, message)
    if len(message.command) < 2:
        await message.edit(
            "❗ | Укажите запрос для поиска.\n\n"
            "**Примеры:**\n"
            "`Навальный Алексей Анатольевич 04.06.1976`\n"
            "`79637829051`\n"
            "`ceo@vkontakte.ru`\n"
            "`В395ОК199`\n"
            "`@sherlock`\n"
            "`tgID 5811749427`\n"
        )
        return

    raw_query = " ".join(message.command[1:])
    normalized_query = normalize_query(raw_query)

    await message.edit(f"🕵️ | Поиск по запросу: `{normalized_query}`. Пожалуйста, подождите...")

    try:
        await client.unblock_user(bot_tag)
        await client.send_message(bot_tag, normalized_query)
        await asyncio.sleep(20)
    except Exception as e:
        await message.edit(f"⚠️ | Ошибка при отправке запроса: `{e}`")
        return

    async for reply in client.get_chat_history(bot_tag, limit=1):
        await message.edit("📄 | Вот что удалось найти:")
        await client.forward_messages(message.chat.id, bot_tag, reply.id)
        return

    await message.edit("❌ | Ничего не найдено или бот не ответил.")
