import asyncio
import os
from telethon import TelegramClient
from telethon.sessions import StringSession
from telethon.tl.functions.channels import JoinChannelRequest

from config import API_ID, API_HASH, SESSION, FORCE_JOIN_CHANNEL
from plugins import load_plugins

async def main():
    if not SESSION:
        print("❌ SESSION string tidak ditemukan di config.")
        return

    print("🔁 Memulai userbot dari session string...")

    client = TelegramClient(StringSession(SESSION), API_ID, API_HASH)
    load_plugins(client)

    await client.start()
    me = await client.get_me()
    print(f"✅ Userbot aktif sebagai: {me.first_name} (@{me.username or 'no username'})")

    # Auto join ke channel
    if FORCE_JOIN_CHANNEL:
        try:
            await client(JoinChannelRequest(FORCE_JOIN_CHANNEL))
            print(f"📌 Auto join ke channel: {FORCE_JOIN_CHANNEL}")
        except Exception as e:
            print(f"⚠️ Gagal join channel: {e}")

    await client.run_until_disconnected()

if __name__ == "__main__":
    asyncio.run(main())# Loads session string and starts userbot
