import os
from dotenv import load_dotenv

load_dotenv()  # Ambil dari file .env jika tersedia

BOT_TOKEN = os.getenv("BOT_TOKEN")
ADMIN_ID = int(os.getenv("ADMIN_ID", 0))
MONGO_URI = os.getenv("MONGO_URI", "")
FORCE_JOIN_CHANNEL = os.getenv("FORCE_JOIN_CHANNEL", "")
FORCE_JOIN_NAME = os.getenv("FORCE_JOIN_NAME", "")  # Misalnya: 'leobaseid'
GCAST_BLACKLIST = os.getenv("GCAST_BLACKLIST", "").split("|")  # pisahkan pakai '|'# Configuration for bot_builder
