from telethon import TelegramClient
from telethon.sessions import StringSession
from config import API_ID, API_HASH, SESSION
from pathlib import Path
import asyncio
import os
import importlib

# Load plugin dari folder plugins
def load_plugins(client):
    plugins_path = Path(__file__).parent / "plugins"
    for plugin in plugins_path.glob("*.py"):
        if plugin.name.startswith("_"):
            continue
        name = plugin.stem
        try:
            mod = importlib.import_module(f"userbot_template.plugins.{name}")
            if hasattr(mod, "register"):
                mod.register(client)
        except Exception as e:
            print(f"❌ Gagal load plugin {name}: {e}")

async def main():
    print("🔁 Memulai userbot...")

    client = TelegramClient(StringSession(SESSION), API_ID, API_HASH)
    load_plugins(client)

    await client.start()
    me = await client.get_me()
    print(f"✅ Userbot aktif sebagai: {me.first_name} (@{me.username or 'no username'})")

    await client.run_until_disconnected()

if __name__ == "__main__":
    asyncio.run(main())# Main userbot runner (Telethon)
