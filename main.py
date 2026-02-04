import json
import os
import datetime
from telethon import TelegramClient, events
from telethon.sessions import StringSession
import config
from keep_alive import keep_alive

# Javoblar tarixini saqlash uchun fayl
HISTORY_FILE = 'reply_history.json'

def load_history():
    if os.path.exists(HISTORY_FILE):
        try:
            with open(HISTORY_FILE, 'r') as f:
                return json.load(f)
        except:
            return {}
    return {}

def save_history(history):
    with open(HISTORY_FILE, 'w') as f:
        json.dump(history, f)

# Clientni sozlash
api_id = int(os.environ.get('API_ID', config.API_ID))
api_hash = os.environ.get('API_HASH', config.API_HASH)

# Agar kompyuterda bo'lsa, fayldan o'qiydi.
# Agar Render (server) da bo'lsa, "Environment Variable" dan o'qiydi.
session_string = os.environ.get('SESSION_STRING')

if session_string:
    print("Session string topildi, tozalanmoqda...", flush=True)
    # Hamma probel va yangi qatorlarni olib tashlaymiz
    clean_session = "".join(session_string.split())
    client = TelegramClient(StringSession(clean_session), api_id, api_hash)
else:
    print("Session string topilmadi, local sessiondan foydalaniladi.", flush=True)
    client = TelegramClient('my_userbot_session', api_id, api_hash)

@client.on(events.NewMessage(incoming=True))
async def handle_incoming_message(event):
    # Debug xabari (faqat siz uchun)
    if event.is_private and event.raw_text.lower() == '.test':
        await event.reply("Bot ishlayapti! ✅")
        return

    if not event.is_private:
        return

    sender = await event.get_sender()
    if not sender:
        return
        
    sender_id = str(sender.id)
    print(f"Yangi xabar keldi: {sender_id} dan")
    
    me = await client.get_me()
    if sender_id == str(me.id):
        return

    history = load_history()
    today_str = datetime.date.today().isoformat()

    last_reply_date = history.get(sender_id)

    if last_reply_date != today_str:
        print(f"Javob qaytarilmoqda: {sender.first_name} (ID: {sender_id})")
        try:
            await event.reply(config.AUTO_REPLY_MESSAGE)
            history[sender_id] = today_str
            save_history(history)
        except Exception as e:
            print(f"Xatolik xabar yuborishda: {e}")
    else:
        print(f"Bugun allaqachon javob berilgan: {sender_id}")

print("Bot jarayoni boshlandi...")

if __name__ == '__main__':
    print("Dastur boshlanmoqda...", flush=True)
    keep_alive()
    try:
        print("Telegram client boshlanmoqda...", flush=True)
        client.start()
        print("Bot muvaffaqiyatli ulandi va ishlayapti! ✅", flush=True)
        client.run_until_disconnected()
    except Exception as e:
        print(f"KRITIK XATOLIK: {e}", flush=True)
