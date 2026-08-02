"""Zelretch Addon: Fictional Profile Generator

Creates a fictional profile card for entertainment and testing.

Category: Fun
Maintainer: Siam Chowdhury
GitHub: https://github.com/ChowdhurySiam
Telegram: @Ch0wdhury_Siam
"""

ZELRETCH_MODULE_INFO = {'title': 'Fictional Profile Generator', 'icon': '🧾', 'category': 'Fun', 'description': 'Creates a fictional profile card for entertainment and testing.', 'developer': 'Siam Chowdhury', 'github': 'https://github.com/ChowdhurySiam', 'telegram': 'https://t.me/Ch0wdhury_Siam'}

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
    fake = Faker('ru_RU')
    await message.edit('Доксим тя пидор')
    if randint(0, 1) == 0:
        name = 'Артур Ламаев'
    else:
        name = fake.name()
    pasta = f'''
Докс на тя:
- - - - - - 
ФИО : {name}
Адрес электронной почты : {fake.email()}
Телефон : {fake.phone_number()}
Адрес регистрации : {fake.street_address()}
Пароль к почте : {fake.password()}
Карта : {fake.credit_card_full()}
Паспорт: {fake.passport_number()}
- - - - - -
Жди докс бошеее
'''
    sleep(2)
    await message.edit(pasta)
