from telethon import TelegramClient
from telethon.sessions import StringSession


if STRING_SESSION:
    # pylint: disable=invalid-name
    bot = TelegramClient(StringSession(STRING_SESSION), API_KEY, API_HASH)
else:
    # pylint: disable=invalid-name
    bot = TelegramClient("userbot", API_KEY, API_HASH)

# --------------------------
george = bot

# --------------------------
global zeus
zeus = page_number
