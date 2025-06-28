import os
from dotenv import load_dotenv

load_dotenv()

API_ID = int(os.getenv("API_ID", 123456))
API_HASH = os.getenv("API_HASH", "your_api_hash_here")
SESSION = os.getenv("SESSION", "")
FORCE_JOIN_CHANNEL = os.getenv("FORCE_JOIN_CHANNEL", "")
GCAST_BLACKLIST = os.getenv("GCAST_BLACKLIST", "").split("|")
SUDO_USERS = os.getenv("SUDO_USERS", "").split("|")  # user_id list# Config file for userbot
