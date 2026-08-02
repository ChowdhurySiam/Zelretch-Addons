"""Zelretch Addon: Bull Text

Generates randomized dramatic text for entertainment.

Category: Fun
Maintainer: Siam Chowdhury
GitHub: https://github.com/ChowdhurySiam
Telegram: @Ch0wdhury_Siam
"""

ZELRETCH_MODULE_INFO = {'title': 'Bull Text', 'icon': '💬', 'category': 'Fun', 'description': 'Generates randomized dramatic text for entertainment.', 'developer': 'Siam Chowdhury', 'github': 'https://github.com/ChowdhurySiam', 'telegram': 'https://t.me/Ch0wdhury_Siam', 'undo': '.undo (reply to the Addon output)'}
import asyncio
import glob
import os
import random
from pyrogram import Client, filters
from command import zel_command, zel_sudo, who_message

bullr = (
    'YOUR CONFIDENCE IS LOUDER THAN YOUR ARGUMENT.',
    'THAT PLAN HAS MORE HOLES THAN A BROKEN UMBRELLA.',
    'YOU BROUGHT MAXIMUM ENERGY AND MINIMUM ACCURACY.',
    'EVEN AUTOCORRECT COULD NOT SAVE THAT SENTENCE.',
    'YOUR COMEBACK IS STILL BUFFERING.',
    'THE LOGIC LEFT THE CHAT BEFORE YOU ARRIVED.',
    'YOU ARE SPEEDRUNNING THE WRONG ANSWER.',
    'THAT EXPLANATION NEEDS A RESTART AND A PATCH.',
    'YOU HAVE UNLOCKED A NEW LEVEL OF CONFUSION.',
    'THE DRAMA IS IMPRESSIVE; THE EVIDENCE IS MISSING.',
    'YOUR ARGUMENT HAS EXPIRED. PLEASE GENERATE A NEW ONE.',
    'THAT WAS A BOLD MOVE WITH NO SUPPORTING DATA.',
    'YOU ARE USING PREMIUM CONFIDENCE ON A FREE TRIAL OF LOGIC.',
    'THE PLOT TWIST IS THAT NOTHING YOU SAID CONNECTS.',
    'YOUR MESSAGE ARRIVED, BUT THE POINT DID NOT.',
    'THAT TAKE NEEDS DEBUGGING.',
    'YOU HAVE GREAT TIMING FOR THE WRONG MOMENT.',
    'THE FACTS REQUESTED A SAFE DISTANCE FROM THAT CLAIM.',
    'YOUR STRATEGY IS MOSTLY DECORATIVE.',
    'THE ANSWER WAS NEARBY, YET YOU CHOSE ADVENTURE.',
)

def bullme():
    return random.choice(bullr)

@Client.on_message(zel_command("bull", "BullMod", os.path.basename(__file__)) & zel_sudo())
async def bull_handler(client, message):
    message = await who_message(client, message)
    try:
        aoa = bullme()
        await message.edit(aoa)
    except Exception as e:
        await message.edit("Error :(")

@Client.on_message(zel_command("bulli", "BullMod", os.path.basename(__file__)) & zel_sudo())
async def bulli_handler(client, message):
    message = await who_message(client, message)
    aoa = bullme()
    await message.edit(f"<i>{aoa}</i>")
