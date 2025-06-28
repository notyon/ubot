
import os
from dotenv import load_dotenv

# Load variabel dari .env file
load_dotenv()

# Telegram Bot Token dari @BotFather
BOT_TOKEN = os.getenv("8068737897:AAEC4EfVnn-GeN7Yo0oMRpxcY0_eYCjHVLo")

# ID Admin bot pusat (int)
ADMIN_ID = int(os.getenv("1684865940"))

# MongoDB URI
MONGO_URI = os.getenv("mongodb+srv://ucik:ucik@cluster0.0l3r8.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0")

# API_ID & API_HASH wajib untuk autentikasi Pyrogram
API_ID = int(os.getenv("29486311"))
API_HASH = os.getenv("ffdc688dc4eee8d2585cb24155188432")
FORCE_JOIN_CHANNEL = os.getenv("FORCE_JOIN_CHANNEL", "1001991260453")
FORCE_JOIN_NAME = os.getenv("FORCE_JOIN_NAME", "leobaseid")  # Misalnya: 'leobaseid'
GCAST_BLACKLIST = os.getenv("GCAST_BLACKLIST", "").split("|")  # pisahkan pakai '|'# Configuration for bot_builder
