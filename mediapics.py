"""Zelretch Addon: Media Gallery

Fetches images from several supported themed media sources.

Category: Media
Maintainer: Siam Chowdhury
GitHub: https://github.com/ChowdhurySiam
Telegram: @Ch0wdhury_Siam
"""

ZELRETCH_MODULE_INFO = {'title': 'Media Gallery', 'icon': '🖼️', 'category': 'Media', 'description': 'Fetches images from several supported themed media sources.', 'developer': 'Siam Chowdhury', 'github': 'https://github.com/ChowdhurySiam', 'telegram': 'https://t.me/Ch0wdhury_Siam'}

import asyncio
import os
import logging
import random
import requests
from pyrogram import Client, filters
from command import zel_command, zel_sudo, who_message

@Client.on_message(zel_command("anime", "MediaPics", os.path.basename(__file__)) & zel_sudo())
async def anime(client, message):
    message = await who_message(client, message)
    try:
        response = requests.get("https://api.waifu.pics/nsfw/waifu")
        response.raise_for_status()
        data = response.json()
        await client.send_photo(
            chat_id=message.chat.id,
            photo=data['url'],
            reply_to_message_id=message.reply_to_message.id if message.reply_to_message else None,
            message_thread_id=message.message_thread_id
        )
        await message.delete()
    except Exception:
        await message.edit("Произошла ошибка при получении картинки.")

@Client.on_message(zel_command("cat", "MediaPics", os.path.basename(__file__)) & zel_sudo())
async def cat(client, message):
    message = await who_message(client, message)
    try:
        response = requests.get("https://api.thecatapi.com/v1/images/search")
        response.raise_for_status()
        data = response.json()
        if data:
            image_url = data[0]['url']
            await client.send_photo(
                chat_id=message.chat.id,
                photo=image_url,
                reply_to_message_id=message.reply_to_message.id if message.reply_to_message else None,
                message_thread_id=message.message_thread_id
            )
            await message.delete()
        else:
            await message.edit("Произошла ошибка при получении фото.")
    except Exception:
        await message.edit("Произошла ошибка при получении фото.")

@Client.on_message(zel_command("lolic", "MediaPics", os.path.basename(__file__)) & zel_sudo())
async def lolic(client, message):
    message = await who_message(client, message)
    await message.edit("⏳ загрузка вашей лоли фотографии...")
    await asyncio.sleep(0.5)
    chat = "hdjrkdjrkdkd"
    try:
        messages = []
        async for msg in client.get_chat_history(chat, limit=1, offset=random.choice(range(1, 851, 2))):
            messages.append(msg)
        if messages:
            media = None
            if messages[0].photo:
                media = messages[0].photo
                await client.send_photo(
                    chat_id=message.chat.id,
                    photo=media.file_id,
                    reply_to_message_id=message.reply_to_message.id if message.reply_to_message else None,
                    message_thread_id=message.message_thread_id
                )
            elif messages[0].video:
                media = messages[0].video
                await client.send_video(
                    chat_id=message.chat.id,
                    video=media.file_id,
                    reply_to_message_id=message.reply_to_message.id if message.reply_to_message else None,
                    message_thread_id=message.message_thread_id
                )
            elif messages[0].document:
                media = messages[0].document
                await client.send_document(
                    chat_id=message.chat.id,
                    document=media.file_id,
                    reply_to_message_id=message.reply_to_message.id if message.reply_to_message else None,
                    message_thread_id=message.message_thread_id
                )
            elif messages[0].animation:
                media = messages[0].animation
                await client.send_animation(
                    chat_id=message.chat.id,
                    animation=media.file_id,
                    reply_to_message_id=message.reply_to_message.id if message.reply_to_message else None,
                    message_thread_id=message.message_thread_id
                )
            if media:
                await message.delete()
            else:
                await message.edit("Не удалось получить фотографии. Пожалуйста, разблокируйте @ferganteusbot")
        else:
            await message.edit("Не удалось получить фотографии. Пожалуйста, разблокируйте @ferganteusbot")
    except Exception:
        await message.edit("Не удалось получить фотографии. Пожалуйста, разблокируйте @ferganteusbot")

@Client.on_message(zel_command("loli", "MediaPics", os.path.basename(__file__)) & zel_sudo())
async def loli(client, message):
    message = await who_message(client, message)
    await message.edit("⏳ загрузка вашей лоли фотографии...")
    bot_username = "@ferganteusbot"
    command = "/lh"
    try:
        sent_message = await client.send_message(bot_username, command)
        response = None
        for _ in range(15):
            await asyncio.sleep(1)
            async for msg in client.get_chat_history(bot_username, limit=1):
                if msg.from_user and msg.from_user.id == sent_message.from_user.id and msg.id != sent_message.id:
                    response = msg
                    break
            if response:
                break
        if response and response.media:
            await client.send_message(
                chat_id=message.chat.id,
                text=response.text if not response.media else None,
                reply_to_message_id=message.reply_to_message.id if message.reply_to_message else None,
                message_thread_id=message.message_thread_id
            )
            if response.photo:
                await client.send_photo(
                    chat_id=message.chat.id,
                    photo=response.photo.file_id,
                    message_thread_id=message.message_thread_id
                )
            elif response.video:
                await client.send_video(
                    chat_id=message.chat.id,
                    video=response.video.file_id,
                    message_thread_id=message.message_thread_id
                )
            elif response.document:
                await client.send_document(
                    chat_id=message.chat.id,
                    document=response.document.file_id,
                    message_thread_id=message.message_thread_id
                )
            elif response.animation:
                await client.send_animation(
                    chat_id=message.chat.id,
                    animation=response.animation.file_id,
                    message_thread_id=message.message_thread_id
                )
            await client.delete_messages(bot_username, [sent_message.id, response.id])
            await message.delete()
        else:
            await message.edit("Не удалось получить фотографии. Пожалуйста, разблокируйте @ferganteusbot")
            await client.delete_messages(bot_username, [sent_message.id])
    except Exception:
        await message.edit("Не удалось получить фотографии. Пожалуйста, разблокируйте @ferganteusbot")

@Client.on_message(zel_command("lolih", "MediaPics", os.path.basename(__file__)) & zel_sudo())
async def lolih(client, message):
    message = await who_message(client, message)
    await message.edit("⏳ загрузка вашей лоли фотографии...")
    bot_username = "@ferganteusbot"
    command = "/lh"
    try:
        sent_message = await client.send_message(bot_username, command)
        response = None
        for _ in range(15):
            await asyncio.sleep(1)
            async for msg in client.get_chat_history(bot_username, limit=1):
                if msg.from_user and msg.from_user.id == sent_message.from_user.id and msg.id != sent_message.id:
                    response = msg
                    break
            if response:
                break
        if response and response.media:
            await client.send_message(
                chat_id=message.chat.id,
                text=response.text if not response.media else None,
                reply_to_message_id=message.reply_to_message.id if message.reply_to_message else None,
                message_thread_id=message.message_thread_id
            )
            if response.photo:
                await client.send_photo(
                    chat_id=message.chat.id,
                    photo=response.photo.file_id,
                    message_thread_id=message.message_thread_id
                )
            elif response.video:
                await client.send_video(
                    chat_id=message.chat.id,
                    video=response.video.file_id,
                    message_thread_id=message.message_thread_id
                )
            elif response.document:
                await client.send_document(
                    chat_id=message.chat.id,
                    document=response.document.file_id,
                    message_thread_id=message.message_thread_id
                )
            elif response.animation:
                await client.send_animation(
                    chat_id=message.chat.id,
                    animation=response.animation.file_id,
                    message_thread_id=message.message_thread_id
                )
            await client.delete_messages(bot_username, [sent_message.id, response.id])
            await message.delete()
        else:
            await message.edit("Не удалось получить фотографии. Пожалуйста, разблокируйте @ferganteusbot")
            await client.delete_messages(bot_username, [sent_message.id])
    except Exception:
        await message.edit("Не удалось получить фотографии. Пожалуйста, разблокируйте @ferganteusbot")

@Client.on_message(zel_command("fem", "MediaPics", os.path.basename(__file__)) & zel_sudo())
async def fem(client, message):
    message = await who_message(client, message)
    await message.edit("🔴 загрузка вашего медиа...")
    bot_username = "@ferganteusbot"
    command = "/fm"
    try:
        sent_message = await client.send_message(bot_username, command)
        response = None
        for _ in range(15):
            await asyncio.sleep(1)
            async for msg in client.get_chat_history(bot_username, limit=1):
                if msg.from_user and msg.from_user.id == sent_message.from_user.id and msg.id != sent_message.id:
                    response = msg
                    break
            if response:
                break
        if response and response.media:
            await client.send_message(
                chat_id=message.chat.id,
                text=response.text if not response.media else None,
                reply_to_message_id=message.reply_to_message.id if message.reply_to_message else None,
                message_thread_id=message.message_thread_id
            )
            if response.photo:
                await client.send_photo(
                    chat_id=message.chat.id,
                    photo=response.photo.file_id,
                    message_thread_id=message.message_thread_id
                )
            elif response.video:
                await client.send_video(
                    chat_id=message.chat.id,
                    video=response.video.file_id,
                    message_thread_id=message.message_thread_id
                )
            elif response.document:
                await client.send_document(
                    chat_id=message.chat.id,
                    document=response.document.file_id,
                    message_thread_id=message.message_thread_id
                )
            elif response.animation:
                await client.send_animation(
                    chat_id=message.chat.id,
                    animation=response.animation.file_id,
                    message_thread_id=message.message_thread_id
                )
            await client.delete_messages(bot_username, [sent_message.id, response.id])
            await message.delete()
        else:
            await message.edit("Не удалось получить фотографии. Пожалуйста, разблокируйте @ferganteusbot")
            await client.delete_messages(bot_username, [sent_message.id])
    except Exception:
        await message.edit("Не удалось получить фотографии. Пожалуйста, разблокируйте @ferganteusbot")

@Client.on_message(zel_command("sfw", "MediaPics", os.path.basename(__file__)) & zel_sudo())
async def sfw(client, message):
    message = await who_message(client, message)
    await message.edit("🔴 загрузка вашего медиа...")
    bot_username = "@ferganteusbot"
    command = "/rc"
    try:
        sent_message = await client.send_message(bot_username, command)
        response = None
        for _ in range(15):
            await asyncio.sleep(1)
            async for msg in client.get_chat_history(bot_username, limit=1):
                if msg.from_user and msg.from_user.id == sent_message.from_user.id and msg.id != sent_message.id:
                    response = msg
                    break
            if response:
                break
        if response and response.media:
            await client.send_message(
                chat_id=message.chat.id,
                text=response.text if not response.media else None,
                reply_to_message_id=message.reply_to_message.id if message.reply_to_message else None,
                message_thread_id=message.message_thread_id
            )
            if response.photo:
                await client.send_photo(
                    chat_id=message.chat.id,
                    photo=response.photo.file_id,
                    message_thread_id=message.message_thread_id
                )
            elif response.video:
                await client.send_video(
                    chat_id=message.chat.id,
                    video=response.video.file_id,
                    message_thread_id=message.message_thread_id
                )
            elif response.document:
                await client.send_document(
                    chat_id=message.chat.id,
                    document=response.document.file_id,
                    message_thread_id=message.message_thread_id
                )
            elif response.animation:
                await client.send_animation(
                    chat_id=message.chat.id,
                    animation=response.animation.file_id,
                    message_thread_id=message.message_thread_id
                )
            await client.delete_messages(bot_username, [sent_message.id, response.id])
            await message.delete()
        else:
            await message.edit("Не удалось получить фотографии. Пожалуйста, разблокируйте @ferganteusbot")
            await client.delete_messages(bot_username, [sent_message.id])
    except Exception:
        await message.edit("Не удалось получить фотографии. Пожалуйста, разблокируйте @ferganteusbot")

@Client.on_message(zel_command("furry", "MediaPics", os.path.basename(__file__)) & zel_sudo())
async def furry(client, message):
    message = await who_message(client, message)
    await message.edit("🔴 загрузка вашего медиа...")
    await asyncio.sleep(0.5)
    chat = "furrylov"
    try:
        messages = []
        async for msg in client.get_chat_history(chat, limit=1, offset=random.choice(range(1, 12436, 2))):
            messages.append(msg)
        if messages:
            media = None
            if messages[0].photo:
                media = messages[0].photo
                await client.send_photo(
                    chat_id=message.chat.id,
                    photo=media.file_id,
                    reply_to_message_id=message.reply_to_message.id if message.reply_to_message else None,
                    message_thread_id=message.message_thread_id
                )
            elif messages[0].video:
                media = messages[0].video
                await client.send_video(
                    chat_id=message.chat.id,
                    video=media.file_id,
                    reply_to_message_id=message.reply_to_message.id if message.reply_to_message else None,
                    message_thread_id=message.message_thread_id
                )
            elif messages[0].document:
                media = messages[0].document
                await client.send_document(
                    chat_id=message.chat.id,
                    document=media.file_id,
                    reply_to_message_id=message.reply_to_message.id if message.reply_to_message else None,
                    message_thread_id=message.message_thread_id
                )
            elif messages[0].animation:
                media = messages[0].animation
                await client.send_animation(
                    chat_id=message.chat.id,
                    animation=media.file_id,
                    reply_to_message_id=message.reply_to_message.id if message.reply_to_message else None,
                    message_thread_id=message.message_thread_id
                )
            if media:
                await message.delete()
            else:
                await message.edit("Не удалось получить фотографии. Пожалуйста, разблокируйте @ferganteusbot")
        else:
            await message.edit("Не удалось получить фотографии. Пожалуйста, разблокируйте @ferganteusbot")
    except Exception:
        await message.edit("Не удалось получить фотографии. Пожалуйста, разблокируйте @ferganteusbot")

@Client.on_message(zel_command("nsfw", "MediaPics", os.path.basename(__file__)) & zel_sudo())
async def nsfw(client, message):
    message = await who_message(client, message)
    await message.edit("🔴 загрузка вашего медиа...")
    await asyncio.sleep(0.5)
    chat = "hdjrkdjrkdkd"
    try:
        messages = []
        async for msg in client.get_chat_history(chat, limit=1, offset=random.choice(range(1, 851, 2))):
            messages.append(msg)
        if messages:
            media = None
            if messages[0].photo:
                media = messages[0].photo
                await client.send_photo(
                    chat_id=message.chat.id,
                    photo=media.file_id,
                    reply_to_message_id=message.reply_to_message.id if message.reply_to_message else None,
                    message_thread_id=message.message_thread_id
                )
            elif messages[0].video:
                media = messages[0].video
                await client.send_video(
                    chat_id=message.chat.id,
                    video=media.file_id,
                    reply_to_message_id=message.reply_to_message.id if message.reply_to_message else None,
                    message_thread_id=message.message_thread_id
                )
            elif messages[0].document:
                media = messages[0].document
                await client.send_document(
                    chat_id=message.chat.id,
                    document=media.file_id,
                    reply_to_message_id=message.reply_to_message.id if message.reply_to_message else None,
                    message_thread_id=message.message_thread_id
                )
            elif messages[0].animation:
                media = messages[0].animation
                await client.send_animation(
                    chat_id=message.chat.id,
                    animation=media.file_id,
                    reply_to_message_id=message.reply_to_message.id if message.reply_to_message else None,
                    message_thread_id=message.message_thread_id
                )
            if media:
                await message.delete()
            else:
                await message.edit("Не удалось получить фотографии. Пожалуйста, разблокируйте @ferganteusbot")
        else:
            await message.edit("Не удалось получить фотографии. Пожалуйста, разблокируйте @ferganteusbot")
    except Exception:
        await message.edit("Не удалось получить фотографии. Пожалуйста, разблокируйте @ferganteusbot")
