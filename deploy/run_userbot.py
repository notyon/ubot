import asyncio
import os
from telethon import TelegramClient
from telethon.sessions import StringSession
from importlib import import_module
from pathlib import Path
import sys

# Tambahkan path plugin
sys.path.append(os.path.abspath("../userbot_template"))

# === Konfigurasi ===
API_ID = 123456  # Ganti dengan API ID default jika mau testing lokal
API_HASH = "abcdef1234567890abcdef1234567890"  # Ganti API HASH default

# === Folder session string tersimpan ===
SESSION_DIR = "../sessions"

# Auto import plugin dari folder plugins
def load_plugins(client):
    plugin_dir = Path("../userbot_template/plugins")
    for file in plugin_dir.glob("*.py"):
        if file.name.startswith("_"):
            continue
        name = file.stem
        try:
            module = import_module(f"userbot_template.plugins.{name}")
            if hasattr(module, "register"):
                module.register(client)
        except Exception as e:
            print(f"❌ Gagal load plugin {name}: {e}")

# Load semua .session string dan jalankan client
async def run_all_userbots():
    if not os.path.exists(SESSION_DIR):
        os.makedirs(SESSION_DIR)

    session_files = [f for f in os.listdir(SESSION_DIR) if f.endswith(".session") or f.endswith(".txt")]
    
    if not session_files:
        print("⚠️ Tidak ada session ditemukan di folder 'sessions/'.")
        return

    for filename in session_files:
        session_path = os.path.join(SESSION_DIR, filename)
        with open(session_path, "r") as f:
            session_str = f.read().strip()

        print(f"🚀 Menjalankan userbot dari session: {filename}")
        try:
            client = TelegramClient(StringSession(session_str), API_ID, API_HASH)
            load_plugins(client)

            await client.start()
            me = await client.get_me()
            print(f"✅ Userbot aktif sebagai: {me.first_name} (@{me.username or 'no username'})")

        except Exception as e:
            print(f"❌ Gagal menjalankan session {filename}: {e}")

    print("🔥 Semua userbot aktif.")

# Run
if __name__ == "__main__":
    asyncio.run(run_all_userbots())
