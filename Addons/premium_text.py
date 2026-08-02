"""Zelretch Addon: Premium Text

Transforms supported characters into premium-emoji styled text.

Category: Fun
Maintainer: Siam Chowdhury
GitHub: https://github.com/ChowdhurySiam
Telegram: @Ch0wdhury_Siam
"""

ZELRETCH_MODULE_INFO = {'title': 'Premium Text', 'icon': '💠', 'category': 'Fun', 'description': 'Transforms supported characters into premium-emoji styled text.', 'developer': 'Siam Chowdhury', 'github': 'https://github.com/ChowdhurySiam', 'telegram': 'https://t.me/Ch0wdhury_Siam'}

from pyrogram import Client, filters
from command import zel_command, zel_sudo, who_message
import os

emoji_list = {
    '1': '<emoji id=5235776368905562305>1️⃣</emoji>',
    '2': '<emoji id=5237704680372447424>2️⃣</emoji>',
    '3': '<emoji id=5238044171767393675>3️⃣</emoji>',
    '4': '<emoji id=5235533321001250232>4️⃣</emoji>',
    '5': '<emoji id=5238171599152097811>5️⃣</emoji>',
    '6': '<emoji id=5235500881113263583>6️⃣</emoji>',
    '7': '<emoji id=5237875542761417785>7️⃣</emoji>',
    '8': '<emoji id=5238067300166281132>8️⃣</emoji>',
    '9': '<emoji id=5237872922831367023>9️⃣</emoji>',
    '0': '<emoji id=5238055991517390123>0️⃣</emoji>',
    '!': '<emoji id=5211108619377977503>🔤</emoji>',
    '?': '<emoji id=5210880311801423356>🔤</emoji>',
    '(': '<emoji id=5256085766009793165>🔤</emoji>',
    ')': '<emoji id=5255844096789983205>🔤</emoji>',
    '.': '<emoji id=5255831662859660095>🔤</emoji>',
    ',': '<emoji id=5255809805771090545>🔤</emoji>',
    ' ': '<emoji id=4992465913241404107>🔤</emoji>',
    'a': '<emoji id=5226734466315067436>🔤</emoji>',
    'b': '<emoji id=5330453760395191684>🔤</emoji>', 
    'c': '<emoji id=5330523098347218561>🔤</emoji>', 
    'd': '<emoji id=5361630910816984823>🔤</emoji>', 
    'e': '<emoji id=5332587336939084375>🔤</emoji>', 
    'f': '<emoji id=5330369145244491360>🔤</emoji>', 
    'g': '<emoji id=5361861335812416268>🔤</emoji>',
    'h': '<emoji id=5330133162561380231>🔤</emoji>', 
    'i': '<emoji id=5381808177547321132>🔤</emoji>',
    'j': '<emoji id=5330383228442258084>🔤</emoji>',
    'k': '<emoji id=5330026574357996347>🔤</emoji>',
    'l': '<emoji id=5332396623211274002>🔤</emoji>',
    'm': '<emoji id=5332321341024508571>🔤</emoji>',
    'n': '<emoji id=5359736027080565026>🔤</emoji>',
    'o': '<emoji id=5361583176550457135>🔤</emoji>',
    'p': '<emoji id=5361909160273255840>🔤</emoji>',
    'q': '<emoji id=5361948540828393629>🔤</emoji>',
    'r': '<emoji id=5332514996804918116>🔤</emoji>',
    's': '<emoji id=5332807088940785741>🔤</emoji>',
    't': '<emoji id=5332558333024934589>🔤</emoji>',
    'u': '<emoji id=5330069773139059849>🔤</emoji>',
    'v': '<emoji id=5395613572531232916>🔤</emoji>',
    'w': '<emoji id=5332308237079288987>🔤</emoji>',
    'x': '<emoji id=5332575697577714724>🔤</emoji>',
    'y': '<emoji id=5332648110726323166>🔤</emoji>',
    'z': '<emoji id=5330309934825351007>🔤</emoji>'
}

@Client.on_message(zel_command("prem_text", "PremiumText", os.path.basename(__file__), "[text]") & zel_sudo())
async def prem_text(client, message):
    message = await who_message(client, message)
    full_text = ' '.join(message.text.lower().split()[1:])
    result = ''
    await client.edit_message_text(message.chat.id, message.id, "Generating text..")
    for i in full_text:
        try:
            result = result + emoji_list[i]
        except:
            result += i
    await client.edit_message_text(message.chat.id, message.id, result)
