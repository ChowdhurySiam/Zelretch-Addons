"""Zelretch Addon: Fictional Profile Generator

Creates a fictional profile card for entertainment and testing.

Category: Fun
Maintainer: Siam Chowdhury
GitHub: https://github.com/ChowdhurySiam
Telegram: @Ch0wdhury_Siam
"""

ZELRETCH_MODULE_INFO = {'title': 'Fictional Profile Generator', 'icon': '🧾', 'category': 'Fun', 'description': 'Creates a fictional profile card for entertainment and testing.', 'developer': 'Siam Chowdhury', 'github': 'https://github.com/ChowdhurySiam', 'telegram': 'https://t.me/Ch0wdhury_Siam', 'undo': '.undo (reply to the Addon output)'}
from random import randint
from time import sleep
from pyrogram import Client, filters
from command import zel_command, zel_sudo, who_message
from requirements_installer import install_library
import os

install_library('faker')
from faker import Faker

@Client.on_message(zel_command("doxx", "Doxx", os.path.basename(__file__)) & zel_sudo())
async def hack(client, message):
    message = await who_message(client, message)
    fake = Faker('en_US')
    await message.edit('Generating a fictional profile...')
    if randint(0, 1) == 0:
        name = 'Alex Morgan'
    else:
        name = fake.name()
    pasta = f'''
Fictional profile:
- - - - - -
Full name: {name}
Email address: {fake.email()}
Phone: {fake.phone_number()}
Registered address: {fake.street_address()}
Generated password: {fake.password()}
Payment card: {fake.credit_card_full()}
Passport number: {fake.passport_number()}
- - - - - -
Generated for entertainment and testing only.
'''
    sleep(2)
    await message.edit(pasta)
