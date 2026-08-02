"""Zelretch Addon: Promo Claimer

Monitors supported promo messages and attempts eligible token redemptions.

Category: Automation
Maintainer: Siam Chowdhury
GitHub: https://github.com/ChowdhurySiam
Telegram: @Ch0wdhury_Siam
"""

ZELRETCH_MODULE_INFO = {'title': 'Promo Claimer', 'icon': '🎟️', 'category': 'Automation', 'description': 'Monitors supported promo messages and attempts eligible token redemptions.', 'developer': 'Siam Chowdhury', 'github': 'https://github.com/ChowdhurySiam', 'telegram': 'https://t.me/Ch0wdhury_Siam'}

# Licensed under GNU AGPLv3.
# Integrates with the supported Telegram promo service.

import asyncio
import os
import logging
from pyrogram import Client, filters
from pyrogram.enums import ParseMode
import re
from command import zel_command, zel_sudo, who_message, get_text

logger = logging.getLogger(__name__)

filename = os.path.basename(__file__)
Module_Name = 'PromoClaimer'

LANGUAGES = {'en': {'module_name': 'PromoClaimer',
        'claimed_promo': '[PromoClaimer] 👌 I successfully claimed promo {promo} for {amount} '
                         'tokens!',
        'error_watcher': '[PromoClaimer] ⛔️ An error occurred while watching for messages:\n{e}',
        'invalid_promo': '[PromoClaimer] 😢 Promo code {promo} is invalid or has expired!',
        'already_claimed': '[PromoClaimer] 😢 Promo code {promo} has already been claimed!',
        'checking_tokens': '[PromoClaimer] Checking tokens balance...',
        'watcher_started': '[PromoClaimer] Watcher started for StableWaifuBot promos',
        'command_description': '| Check tokens balance'}}



@Client.on_message(zel_command("checktokens", Module_Name, filename) & zel_sudo())
async def checktokens(client, message):
    message = await who_message(client, message)
    await message.edit(
        get_text("PromoClaimer", "checking_tokens", LANGUAGES=LANGUAGES),
        parse_mode=ParseMode.MARKDOWN
    )
    
    try:
        bot_username = "StableWaifuBot"
        sent_message = await client.send_message(bot_username, "/tokens")
        response = None
        
        for _ in range(15):
            await asyncio.sleep(1)
            async for msg in client.get_chat_history(bot_username, limit=1):
                if msg.from_user and not msg.from_user.is_self and msg.id != sent_message.id:
                    response = msg
                    break
            if response:
                break
        
        if response and response.text:
            # Check whether the service returned a token balance
            if "not found" in response.text.lower():
                tokens = f"❌ {response.text}"
            else:
                # Show the complete service response
                tokens = response.text
        else:
            tokens = "❌ No response from bot"
        
        await message.edit(tokens, parse_mode=ParseMode.MARKDOWN)
        
    except Exception as e:
        await message.edit(f"❌ Error: {e}", parse_mode=ParseMode.MARKDOWN)

@Client.on_message(filters.text & ~filters.me)
async def watcher(client, message):
    try:
        print(message.text)
        if not message.text:
            return
            
        pattern = r'https://t\.me/StableWaifuBot\?start=promo_(\w+)'
        matches = re.findall(pattern, message.text)
        if not matches:
            return
            
        bot_username = "StableWaifuBot"
        
        for match in matches:
            promo = 'promo_' + match
            
            sent_message = await client.send_message(bot_username, f'/start {promo}')
            response = None
            
            for _ in range(15):
                await asyncio.sleep(1)
                async for msg in client.get_chat_history(bot_username, limit=1):
                    if msg.from_user and not msg.from_user.is_self and msg.id != sent_message.id:
                        response = msg
                        break
                if response:
                    break
            
            if not response:
                logger.error(f"No response for promo {promo}")
                continue
            
            response_text = response.text.casefold()
            if any(term in response_text for term in ('invalid', 'expired', 'not found')):
                logger.info(get_text("PromoClaimer", "invalid_promo", LANGUAGES=LANGUAGES, promo=promo))
            elif any(term in response_text for term in ('already claimed', 'already activated')):
                logger.info(get_text("PromoClaimer", "already_claimed", LANGUAGES=LANGUAGES, promo=promo))
            else:
                try:
                    amount = response.text.split('(+')[1]
                    logger.info(get_text("PromoClaimer", "claimed_promo", LANGUAGES=LANGUAGES, promo=promo, amount=amount))
                except (IndexError, ValueError):
                    logger.info(get_text("PromoClaimer", "claimed_promo", LANGUAGES=LANGUAGES, promo=promo, amount="?"))
                    
    except Exception as e:
        logger.error(get_text("PromoClaimer", "error_watcher", LANGUAGES=LANGUAGES, e=str(e)))
