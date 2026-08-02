"""Zelretch Addon: Media to GIF

Converts replied photos or videos into an optimized GIF.

Category: Files & Media
Maintainer: Siam Chowdhury
GitHub: https://github.com/ChowdhurySiam
Telegram: @Ch0wdhury_Siam
"""
ZELRETCH_MODULE_INFO = {'title': 'Media to GIF', 'icon': '🎞️', 'category': 'Files & Media', 'description': 'Converts replied photos or videos into an optimized GIF.', 'developer': 'Siam Chowdhury', 'github': 'https://github.com/ChowdhurySiam', 'telegram': 'https://t.me/Ch0wdhury_Siam', 'undo': '.undo (reply to the Addon output)'}
import os
import subprocess
import asyncio
from pyrogram import Client, filters
from pyrogram.types import ReplyParameters
from command import zel_command, zel_sudo, who_message
from requirements_installer import install_library
install_library('Pillow -U')
from PIL import Image

def cleanup_temp_files(*files):
    """Remove temporary files."""
    for f in files:
        if f and os.path.exists(f):
            try:
                os.remove(f)
            except Exception:
                pass

def convert_video_to_gif(video_path: str, gif_path: str) -> None:
    """Convert video to GIF with optimized settings."""
    command = ['ffmpeg', '-y', '-i', video_path, '-vf', 'fps=30,scale=640:-1:flags=lanczos', '-c:v', 'gif', gif_path]
    subprocess.run(command, check=True)

@Client.on_message(zel_command('media2gif', 'Media2Gif', os.path.basename(__file__), '[reply to photo or video]') & zel_sudo())
async def media2gif(client, message):
    message = await who_message(client, message)
    reply = message.reply_to_message
    if not reply or not (reply.photo or reply.video):
        return await message.edit('⚠️ Reply to a photo or video.')
    status_msg = await message.edit('⏳ Starting...')
    if reply.photo:
        try:
            await status_msg.edit('⏬ Downloading file...')
            photo_path = await reply.download(file_name='pic2gif_in.jpg')
            gif_path = 'pic2gif_out.gif'
            await status_msg.edit('🔄 Converting...')
            img = Image.open(photo_path).convert('RGB')
            img.save(gif_path, save_all=True, append_images=[], duration=100, loop=0, format='GIF')
            await status_msg.edit('📤 Uploading...')
            await client.send_animation(chat_id=message.chat.id, animation=gif_path, reply_parameters=ReplyParameters(message_id=reply.id), message_thread_id=message.message_thread_id)
        except Exception as e:
            await status_msg.edit('❌ GIF conversion failed.')
            print(f'Error during photo2gif: {e}')
        finally:
            await status_msg.edit('🧹 Cleaning up...')
            cleanup_temp_files('pic2gif_in.jpg', 'pic2gif_out.gif')
            await status_msg.delete()
            await message.delete()
        return
    if reply.video:
        try:
            await status_msg.edit('⏬ Downloading file...')
            video_path = await reply.download(file_name='pic2gif_in.mp4')
            gif_path = 'pic2gif_out.gif'
            await status_msg.edit('🔄 Converting...')
            convert_video_to_gif(video_path, gif_path)
            await status_msg.edit('📤 Uploading...')
            await client.send_animation(chat_id=message.chat.id, animation=gif_path, reply_parameters=ReplyParameters(message_id=reply.id), message_thread_id=message.message_thread_id)
        except Exception as e:
            await status_msg.edit('❌ GIF conversion failed.')
            print(f'Error during video2gif: {e}')
        finally:
            await status_msg.edit('🧹 Cleaning up...')
            cleanup_temp_files('pic2gif_in.mp4', 'pic2gif_out.gif')
            await status_msg.delete()
            await message.delete()
        return
