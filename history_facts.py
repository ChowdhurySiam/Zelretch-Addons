"""Zelretch Addon: History Facts

Returns concise English-language facts from built-in, offline-safe collections.

Category: Information
Maintainer: Siam Chowdhury
GitHub: https://github.com/ChowdhurySiam
Telegram: @Ch0wdhury_Siam
"""

import html
import os
import random

from pyrogram import Client

from command import zel_command, zel_sudo, who_message

ZELRETCH_MODULE_INFO = {
    "title": "History Facts",
    "icon": "📚",
    "category": "Information",
    "description": "Returns concise English-language facts from built-in history collections.",
    "developer": "Siam Chowdhury",
    "github": "https://github.com/ChowdhurySiam",
    "telegram": "https://t.me/Ch0wdhury_Siam",
}

MODULE_NAME = "HistoryFacts"
FILENAME = os.path.basename(__file__)

GENERAL_HISTORY_FACTS = [
    "The earliest known writing systems developed in Mesopotamia more than five thousand years ago.",
    "The Library of Alexandria was part of a larger research institution called the Mouseion.",
    "The printing press greatly accelerated the spread of books and ideas across Europe in the fifteenth century.",
    "The first modern Olympic Games were held in Athens in 1896.",
    "The Magna Carta was sealed in 1215 and became an important symbol of limits on political power.",
    "The ancient city of Petra was carved into sandstone cliffs in present-day Jordan.",
    "The Silk Road was a network of trade routes rather than a single road.",
    "The Rosetta Stone helped scholars decipher ancient Egyptian hieroglyphs.",
]

HITLER_FACTS = [
    "Adolf Hitler became chancellor of Germany in January 1933.",
    "Nazi Germany invaded Poland on 1 September 1939, beginning the Second World War in Europe.",
    "Hitler's regime established a totalitarian dictatorship and carried out the Holocaust.",
    "Hitler died in Berlin in April 1945 as Nazi Germany was collapsing.",
]

MUSSOLINI_FACTS = [
    "Benito Mussolini became prime minister of Italy in 1922.",
    "Mussolini's Fascist government dismantled democratic institutions and created a dictatorship.",
    "Fascist Italy invaded Ethiopia in 1935.",
    "Mussolini was removed from power in 1943 after Allied forces landed in Italy.",
]

STALIN_FACTS = [
    "Joseph Stalin became the dominant leader of the Soviet Union after Vladimir Lenin's death.",
    "Stalin's industrialization and collectivization campaigns caused severe disruption and widespread suffering.",
    "The Great Purge of the 1930s involved mass arrests, executions, and forced-labor sentences.",
    "The Soviet Union played a decisive role in defeating Nazi Germany during the Second World War.",
]


async def _send_fact(client, message, heading, facts):
    message = await who_message(client, message)
    fact = html.escape(random.choice(facts))
    await message.edit(f"<b>📚 {html.escape(heading)}</b>\n\n{fact}")


@Client.on_message(zel_command("rfact", MODULE_NAME, FILENAME) & zel_sudo())
async def random_history_fact(client, message):
    await _send_fact(client, message, "Random history fact", GENERAL_HISTORY_FACTS)


@Client.on_message(zel_command("hfact", MODULE_NAME, FILENAME) & zel_sudo())
async def hitler_fact(client, message):
    await _send_fact(client, message, "Historical fact about Adolf Hitler", HITLER_FACTS)


@Client.on_message(zel_command("mfact", MODULE_NAME, FILENAME) & zel_sudo())
async def mussolini_fact(client, message):
    await _send_fact(client, message, "Historical fact about Benito Mussolini", MUSSOLINI_FACTS)


@Client.on_message(zel_command("sfact", MODULE_NAME, FILENAME) & zel_sudo())
async def stalin_fact(client, message):
    await _send_fact(client, message, "Historical fact about Joseph Stalin", STALIN_FACTS)
