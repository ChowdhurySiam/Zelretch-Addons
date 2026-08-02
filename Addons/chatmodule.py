"""Zelretch Addon: Chat Administration

Provides chat IDs, permissions, moderation, roles, links, and group-management tools.

Category: Administration
Maintainer: Siam Chowdhury
GitHub: https://github.com/ChowdhurySiam
Telegram: @Ch0wdhury_Siam
"""
ZELRETCH_MODULE_INFO = {'title': 'Chat Administration', 'icon': '🛡️', 'category': 'Administration', 'description': 'Provides chat IDs, permissions, moderation, roles, links, and group-management tools.', 'developer': 'Siam Chowdhury', 'github': 'https://github.com/ChowdhurySiam', 'telegram': 'https://t.me/Ch0wdhury_Siam', 'undo': '.unpin / .unban / .unmute / .delrole'}
import asyncio
import os
import json
import logging
from datetime import datetime, timedelta
from pyrogram import Client, filters
from pyrogram.types import Chat, User, Message, ChatPermissions
from pyrogram.enums import ChatType, ChatMemberStatus, ChatMembersFilter
from command import zel_command, zel_sudo, who_message, my_prefix
logger = logging.getLogger(__name__)

def load_config():
    try:
        with open('userdata/chatmodule_roles', 'r', encoding='utf-8') as f:
            return json.loads(f.read().strip())
    except FileNotFoundError:
        return {}

def save_config(roles):
    with open('userdata/chatmodule_roles', 'w', encoding='utf-8') as f:
        json.dump(roles, f, ensure_ascii=False, indent=2)

@Client.on_message(zel_command('id', 'ChatModule', os.path.basename(__file__), '[reply]') & zel_sudo())
async def id_handler(client, message):
    message = await who_message(client, message)
    ids = []
    me = await client.get_me()
    ids.append(f'<b>Your ID:</b> <code>{me.id}</code>')
    if message.chat.type == ChatType.PRIVATE:
        ids.append(f'<b>Chat ID:</b> <code>{message.chat.id}</code>')
        return await message.edit('\n'.join(ids))
    ids.append(f'<b>Chat ID:</b> <code>{message.chat.id}</code>')
    if message.reply_to_message and message.reply_to_message.from_user.id != me.id:
        user_id = message.reply_to_message.from_user.id
        ids.append(f'<b>User ID:</b> <code>{user_id}</code>')
    await message.edit('\n'.join(ids))

@Client.on_message(zel_command('rights', 'ChatModule', os.path.basename(__file__), '[-u username/id]') & zel_sudo())
async def rights_handler(client, message):
    message = await who_message(client, message)
    if message.chat.type == ChatType.PRIVATE:
        return await message.edit('<b>❌ This command works only in groups and channels.</b>')
    args = message.text.split()[1:] if len(message.command) > 1 else []
    user = None
    for arg in args:
        if arg.startswith('-u') or arg.startswith('username'):
            user = arg.split(' ', 1)[1] if ' ' in arg else None
            break
    if not user and message.reply_to_message:
        user = message.reply_to_message.from_user.id
    if not user:
        return await message.edit('<b>❌ Specify a user.</b>')
    try:
        user_obj = await client.get_users(user)
        chat_member = await client.get_chat_member(message.chat.id, user_obj.id)
        if chat_member.status not in [ChatMemberStatus.ADMINISTRATOR, ChatMemberStatus.OWNER]:
            return await message.edit(f'<b>❌ {user_obj.first_name} is not an administrator.</b>')
        rights = []
        if hasattr(chat_member, 'privileges'):
            privileges = chat_member.privileges
            if privileges.can_manage_chat:
                rights.append('Manage chat')
            if privileges.can_delete_messages:
                rights.append('Delete messages')
            if privileges.can_manage_video_chats:
                rights.append('Manage video chats')
            if privileges.can_restrict_members:
                rights.append('Restrict members')
            if privileges.can_promote_members:
                rights.append('Promote administrators')
            if privileges.can_change_info:
                rights.append('Change chat information')
            if privileges.can_invite_users:
                rights.append('Invite users')
            if privileges.can_post_messages:
                rights.append('Post messages')
            if privileges.can_edit_messages:
                rights.append('Edit messages')
            if privileges.can_pin_messages:
                rights.append('Pin messages')
        if not rights:
            rights_text = 'No special permissions'
        else:
            rights_text = '\n'.join([f'✅ {right}' for right in rights])
        rank = chat_member.title if hasattr(chat_member, 'title') and chat_member.title else 'Administrator'
        await message.edit(f'<b>Administrator permissions for {user_obj.first_name}:</b>\n\n{rights_text}\n\n<b>Title:</b> {rank}')
    except Exception as e:
        logger.error(f'Permission lookup error: {e}')
        await message.edit('<b>❌ Could not retrieve user information.</b>')

@Client.on_message(zel_command('leave', 'ChatModule', os.path.basename(__file__)) & zel_sudo())
async def leave_handler(client, message):
    message = await who_message(client, message)
    if message.chat.type == ChatType.PRIVATE:
        return await message.edit('<b>❌ This command works only in groups and channels.</b>')
    await message.delete()
    await client.leave_chat(message.chat.id)

@Client.on_message(zel_command('pin', 'ChatModule', os.path.basename(__file__), '[reply]') & zel_sudo())
async def pin_handler(client, message):
    message = await who_message(client, message)
    if not message.reply_to_message:
        return await message.edit('<b>❌ Reply to a message to pin it.</b>')
    try:
        await client.pin_chat_message(message.chat.id, message.reply_to_message.id, disable_notification=False)
        await message.edit('<b>✅ Message pinned.</b>')
    except Exception as e:
        logger.error(f'Pin error: {e}')
        await message.edit('<b>❌ Could not pin the message.</b>')

@Client.on_message(zel_command('unpin', 'ChatModule', os.path.basename(__file__), '[reply]') & zel_sudo())
async def unpin_handler(client, message):
    message = await who_message(client, message)
    if not message.reply_to_message:
        return await message.edit('<b>❌ Reply to a message to unpin it.</b>')
    try:
        await client.unpin_chat_message(message.chat.id, message.reply_to_message.id)
        await message.edit('<b>✅ Message unpinned.</b>')
    except Exception as e:
        logger.error(f'Unpin error: {e}')
        await message.edit('<b>❌ Could not unpin the message.</b>')

@Client.on_message(zel_command('unpinall', 'ChatModule', os.path.basename(__file__)) & zel_sudo())
async def unpinall_handler(client, message):
    message = await who_message(client, message)
    if message.chat.type == ChatType.PRIVATE:
        return await message.edit('<b>❌ This command works only in groups and channels.</b>')
    try:
        await client.unpin_all_chat_messages(message.chat.id)
        await message.edit('<b>✅ All messages were unpinned.</b>')
    except Exception as e:
        logger.error(f'Unpin-all error: {e}')
        await message.edit('<b>❌ Could not unpin the messages.</b>')

@Client.on_message(zel_command('admins', 'ChatModule', os.path.basename(__file__)) & zel_sudo())
async def admins_handler(client, message):
    message = await who_message(client, message)
    if message.chat.type == ChatType.PRIVATE:
        return await message.edit('<b>❌ This command works only in groups and channels.</b>')
    try:
        admins = []
        async for member in client.get_chat_members(message.chat.id, filter=ChatMembersFilter.ADMINISTRATORS):
            if member.status == ChatMemberStatus.OWNER:
                admins.insert(0, f"👑 <a href='tg://user?id={member.user.id}'>{member.user.first_name}</a> | <code>{member.user.id}</code> - Owner")
            elif member.status == ChatMemberStatus.ADMINISTRATOR:
                rank = member.custom_title if member.custom_title else 'Administrator'
                admins.append(f"✅ <a href='tg://user?id={member.user.id}'>{member.user.first_name}</a> | <code>{member.user.id}</code> - {rank}")
        if not admins:
            await message.edit('<b>❌ No administrators were found.</b>')
        else:
            await message.edit(f'<b>Administrators:</b>\n\n' + '\n'.join(admins))
    except Exception as e:
        logger.error(f'Administrator-list error: {e}')
        await message.edit('<b>❌ Could not retrieve the administrator list.</b>')

@Client.on_message(zel_command('ban', 'ChatModule', os.path.basename(__file__), '[reply] [duration]') & zel_sudo())
async def ban_handler(client, message):
    message = await who_message(client, message)
    if message.chat.type == ChatType.PRIVATE:
        return await message.edit('<b>❌ This command works only in groups and channels.</b>')
    if not message.reply_to_message:
        return await message.edit('<b>❌ Reply to a user message to ban that user.</b>')
    user_id = message.reply_to_message.from_user.id
    args = message.text.split()[1:] if len(message.command) > 1 else []
    ban_time = None
    time_text = ''
    for arg in args:
        if arg.isdigit():
            ban_time = int(arg)
            if ban_time < 60:
                time_text = f'{ban_time} seconds'
            elif ban_time < 3600:
                time_text = f'{ban_time // 60} minutes'
            elif ban_time < 86400:
                time_text = f'{ban_time // 3600} hours'
            else:
                time_text = f'{ban_time // 86400} days'
            break
    try:
        user = await client.get_users(user_id)
        if ban_time:
            until_date = datetime.now() + timedelta(seconds=ban_time)
            await client.ban_chat_member(message.chat.id, user_id, until_date=until_date)
        else:
            await client.ban_chat_member(message.chat.id, user_id)
        time_info = f' for {time_text}' if time_text else ' permanently'
        await message.edit(f'<b>✅ User {user.first_name} banned{time_info}!</b>')
    except Exception as e:
        logger.error(f'Ban error: {e}')
        await message.edit('<b>❌ Could not ban the user.</b>')

@Client.on_message(zel_command('unban', 'ChatModule', os.path.basename(__file__), '[reply]') & zel_sudo())
async def unban_handler(client, message):
    message = await who_message(client, message)
    if message.chat.type == ChatType.PRIVATE:
        return await message.edit('<b>❌ This command works only in groups and channels.</b>')
    if not message.reply_to_message:
        return await message.edit('<b>❌ Reply to a user message to unban that user.</b>')
    try:
        user = await client.get_users(message.reply_to_message.from_user.id)
        await client.unban_chat_member(message.chat.id, user.id)
        await message.edit(f'<b>✅ User {user.first_name} unbanned.</b>')
    except Exception as e:
        logger.error(f'Unban error: {e}')
        await message.edit('<b>❌ Could not unban the user.</b>')

@Client.on_message(zel_command('kick', 'ChatModule', os.path.basename(__file__), '[reply]') & zel_sudo())
async def kick_handler(client, message):
    message = await who_message(client, message)
    if message.chat.type == ChatType.PRIVATE:
        return await message.edit('<b>❌ This command works only in groups and channels.</b>')
    if not message.reply_to_message:
        return await message.edit('<b>❌ Reply to a user message to remove that user.</b>')
    try:
        user = await client.get_users(message.reply_to_message.from_user.id)
        await client.ban_chat_member(message.chat.id, user.id)
        await asyncio.sleep(1)
        await client.unban_chat_member(message.chat.id, user.id)
        await message.edit(f'<b>✅ User {user.first_name} removed.</b>')
    except Exception as e:
        logger.error(f'Remove-user error: {e}')
        await message.edit('<b>❌ Could not remove the user.</b>')

@Client.on_message(zel_command('mute', 'ChatModule', os.path.basename(__file__), '[reply] [duration]') & zel_sudo())
async def mute_handler(client, message):
    message = await who_message(client, message)
    if message.chat.type == ChatType.PRIVATE:
        return await message.edit('<b>❌ This command works only in groups and channels.</b>')
    if not message.reply_to_message:
        return await message.edit('<b>❌ Reply to a user message to mute that user.</b>')
    user_id = message.reply_to_message.from_user.id
    args = message.text.split()[1:] if len(message.command) > 1 else []
    mute_time = None
    time_text = ''
    for arg in args:
        if arg.isdigit():
            mute_time = int(arg)
            if mute_time < 60:
                time_text = f'{mute_time} seconds'
            elif mute_time < 3600:
                time_text = f'{mute_time // 60} minutes'
            elif mute_time < 86400:
                time_text = f'{mute_time // 3600} hours'
            else:
                time_text = f'{mute_time // 86400} days'
            break
    try:
        user = await client.get_users(user_id)
        permissions = ChatPermissions()
        if mute_time:
            until_date = datetime.now() + timedelta(seconds=mute_time)
            await client.restrict_chat_member(message.chat.id, user_id, permissions=permissions, until_date=until_date)
        else:
            await client.restrict_chat_member(message.chat.id, user_id, permissions=permissions)
        time_info = f' for {time_text}' if time_text else ' permanently'
        await message.edit(f'<b>✅ User {user.first_name} muted{time_info}!</b>')
    except Exception as e:
        logger.error(f'Mute error: {e}')
        await message.edit('<b>❌ Could not mute the user.</b>')

@Client.on_message(zel_command('unmute', 'ChatModule', os.path.basename(__file__), '[reply]') & zel_sudo())
async def unmute_handler(client, message):
    message = await who_message(client, message)
    if message.chat.type == ChatType.PRIVATE:
        return await message.edit('<b>❌ This command works only in groups and channels.</b>')
    if not message.reply_to_message:
        return await message.edit('<b>❌ Reply to a user message to unmute that user.</b>')
    try:
        user = await client.get_users(message.reply_to_message.from_user.id)
        permissions = ChatPermissions(can_send_messages=True, can_send_media_messages=True, can_send_other_messages=True, can_add_web_page_previews=True)
        await client.restrict_chat_member(message.chat.id, user.id, permissions=permissions)
        await message.edit(f'<b>✅ User {user.first_name} unmuted.</b>')
    except Exception as e:
        logger.error(f'Unmute error: {e}')
        await message.edit('<b>❌ Could not unmute the user.</b>')

@Client.on_message(zel_command('rename', 'ChatModule', os.path.basename(__file__), '[name]') & zel_sudo())
async def rename_handler(client, message):
    message = await who_message(client, message)
    if message.chat.type == ChatType.PRIVATE:
        return await message.edit('<b>❌ This command works only in groups and channels.</b>')
    args = message.text.split()[1:] if len(message.command) > 1 else []
    if not args:
        return await message.edit('<b>❌ Specify a new title.</b>')
    new_title = ' '.join(args)
    try:
        await client.set_chat_title(message.chat.id, new_title)
        chat_type = 'group' if message.chat.type == ChatType.SUPERGROUP else 'channel'
        await message.edit(f'<b>✅ {chat_type} renamed to {new_title}!</b>')
    except Exception as e:
        logger.error(f'Rename error: {e}')
        await message.edit('<b>❌ Could not rename the chat.</b>')

@Client.on_message(zel_command('create', 'ChatModule', os.path.basename(__file__), '[-g|--group name] [-c|--channel name]') & zel_sudo())
async def create_handler(client, message):
    message = await who_message(client, message)
    args = message.text.split()[1:] if len(message.command) > 1 else []
    if not args:
        return await message.edit('<b>❌ Usage:</b> <code>create -g name</code> or <code>create -c name</code>')
    group_name = None
    channel_name = None
    i = 0
    while i < len(args):
        if args[i] in ['-g', '--group'] and i + 1 < len(args):
            group_name = args[i + 1]
            i += 2
        elif args[i] in ['-c', '--channel'] and i + 1 < len(args):
            channel_name = args[i + 1]
            i += 2
        else:
            i += 1
    try:
        if channel_name:
            chat = await client.create_channel(channel_name, '')
            await message.edit(f'<b>✅ Channel {channel_name} created.</b>\n<b>Link:</b> {chat.invite_link}')
        elif group_name:
            chat = await client.create_group(group_name, '')
            await message.edit(f'<b>✅ Group {group_name} created.</b>\n<b>Link:</b> {chat.invite_link}')
        else:
            await message.edit('<b>❌ Invalid arguments.</b>')
    except Exception as e:
        logger.error(f'Chat creation error: {e}')
        await message.edit('<b>❌ Could not create the chat.</b>')

@Client.on_message(zel_command('geturl', 'ChatModule', os.path.basename(__file__), '[reply]') & zel_sudo())
async def geturl_handler(client, message):
    message = await who_message(client, message)
    if not message.reply_to_message:
        return await message.edit('<b>❌ Reply to a message to obtain its link.</b>')
    try:
        reply = message.reply_to_message
        chat = message.chat
        if chat.type == ChatType.SUPERGROUP:
            link = f'https://t.me/c/{str(chat.id)[4:]}/{reply.id}'
        else:
            link = f'https://t.me/{chat.username}/{reply.id}' if chat.username else f'https://t.me/c/{chat.id}/{reply.id}'
        await message.edit(f'<b>🔗 Message link:</b> {link}')
    except Exception as e:
        logger.error(f'Message-link error: {e}')
        await message.edit('<b>❌ Could not retrieve the link.</b>')

@Client.on_message(zel_command('addrole', 'ChatModule', os.path.basename(__file__), '-n role_name -p permission_number') & zel_sudo())
async def addrole_handler(client, message):
    message = await who_message(client, message)
    args = message.text.split()[1:] if len(message.command) > 1 else []
    if len(args) < 4:
        return await message.edit('<b>❌ Usage:</b> <code>addrole -n role_name -p permission_number</code>')
    name = None
    perms = None
    i = 0
    while i < len(args):
        if args[i] in ['-n', 'name'] and i + 1 < len(args):
            name = args[i + 1]
            i += 2
        elif args[i] in ['-p', 'perms'] and i + 1 < len(args):
            try:
                perms = int(args[i + 1])
                i += 2
            except ValueError:
                i += 1
        else:
            i += 1
    if not name or perms is None:
        return await message.edit('<b>❌ Invalid arguments.</b>')
    roles = load_config()
    roles[name] = perms
    save_config(roles)
    await message.edit(f'<b>✅ Role {name} created with permissions {perms}!</b>')

@Client.on_message(zel_command('delrole', 'ChatModule', os.path.basename(__file__), '-n role_name') & zel_sudo())
async def delrole_handler(client, message):
    message = await who_message(client, message)
    args = message.text.split()[1:] if len(message.command) > 1 else []
    if len(args) < 2:
        return await message.edit('<b>❌ Usage:</b> <code>delrole -n role_name</code>')
    name = None
    i = 0
    while i < len(args):
        if args[i] in ['-n', 'name'] and i + 1 < len(args):
            name = args[i + 1]
            i += 2
        else:
            i += 1
    if not name:
        return await message.edit('<b>❌ Specify a role name.</b>')
    roles = load_config()
    if name not in roles:
        return await message.edit(f'<b>❌ Role {name} was not found.</b>')
    del roles[name]
    save_config(roles)
    await message.edit(f'<b>✅ Role {name} deleted.</b>')

@Client.on_message(zel_command('roles', 'ChatModule', os.path.basename(__file__), '[-n role_name]') & zel_sudo())
async def roles_handler(client, message):
    message = await who_message(client, message)
    args = message.text.split()[1:] if len(message.command) > 1 else []
    roles = load_config()
    if not roles:
        return await message.edit('<b>❌ No roles were found.</b>')
    if not args:
        role_list = '\n'.join([f'➡️ <code>{role}</code>' for role in roles.keys()])
        await message.edit(f'<b>Available roles:</b>\n{role_list}')
    else:
        role_name = ' '.join(args)
        if role_name not in roles:
            return await message.edit(f'<b>❌ Role {role_name} was not found.</b>')
        await message.edit(f'<b>Role {role_name}:</b>\n<b>Permissions:</b> <code>{roles[role_name]}</code>')

@Client.on_message(zel_command('chatinfo', 'ChatModule', os.path.basename(__file__)) & zel_sudo())
async def chatinfo_handler(client, message):
    message = await who_message(client, message)
    if message.chat.type == ChatType.PRIVATE:
        return await message.edit('<b>❌ This command works only in groups and channels.</b>')
    try:
        chat = await client.get_chat(message.chat.id)
        members_count = 0
        online_count = 0
        async for _ in client.get_chat_members(chat.id):
            members_count += 1
        admins_count = 0
        async for _ in client.get_chat_members(chat.id, filter=ChatMembersFilter.ADMINISTRATORS):
            admins_count += 1
        info_text = f"""<b>📊 Chat information:</b>\n\n🆔 <b>ID:</b> <code>{chat.id}</code>\n📝 <b>Title:</b> {chat.title}\n👥 <b>Members:</b> {members_count}\n👤 <b>Administrators:</b> {admins_count}\n🌐 <b>Username:</b> @{chat.username} if chat.username else "None"\n🔗 <b>Link:</b> {(chat.invite_link if chat.invite_link else 'None')}\n        """
        await message.edit(info_text)
    except Exception as e:
        logger.error(f'Information lookup error: {e}')
        await message.edit('<b>❌ Could not retrieve chat information.</b>')
