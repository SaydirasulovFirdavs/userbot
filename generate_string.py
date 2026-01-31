from telethon.sync import TelegramClient
from telethon.sessions import StringSession
import config

print("Kuting...")

with TelegramClient(StringSession(), config.API_ID, config.API_HASH) as client:
    print("\nPastdagi uzun kodni nusxalab oling va Render da 'SESSION_STRING' deb saqlang:\n")
    print(client.session.save())
    print("\n")
