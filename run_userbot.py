import asyncio
from telethon import TelegramClient
from telethon.sessions import StringSession
from bot_builder.database import get_all_sessions
import os
import glob
import importlib.util

PLUGINS_DIR = "userbot_plugins"
clients = []

def load_plugins(client):
    plugin_files = glob.glob(f"{PLUGINS_DIR}/*.py")
    for plugin_path in plugin_files:
        name = os.path.basename(plugin_path)[:-3]
        spec = importlib.util.spec_from_file_location(name, plugin_path)
        mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mod)
        if hasattr(mod, "register"):
            mod.register(client)

async def start_userbot(session_string):
    try:
        from config import API_ID, API_HASH
        client = TelegramClient(StringSession(session_string), API_ID, API_HASH)
        await client.start()
        load_plugins(client)
        print(f"[+] Userbot aktif: {client.session.save()[:20]}...")
        clients.append(client)
    except Exception as e:
        print(f"[!] Gagal jalankan userbot: {e}")

async def main():
    sessions = get_all_sessions()
    if not sessions:
        print("⚠️ Tidak ada session ditemukan.")
        return

    tasks = [start_userbot(s) for s in sessions]
    await asyncio.gather(*tasks)
    print("✅ Semua userbot aktif.")
    await asyncio.Event().wait()

if __name__ == "__main__":
    asyncio.run(main())
