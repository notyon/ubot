import os
from dotenv import load_dotenv

# Load .env file
load_dotenv()

# Helper untuk validasi
def ensure_env(var_name, cast=str):
    value = os.getenv(var_name)
    if value is None or value.strip() == "":
        raise ValueError(f"❌ ENV variable '{var_name}' is missing or empty.")
    try:
        return cast(value)
    except Exception:
        raise ValueError(f"❌ ENV variable '{var_name}' is not valid {cast.__name__}.")

# Ambil variabel dengan validasi
BOT_TOKEN = ensure_env("BOT_TOKEN")
ADMIN_ID = ensure_env("ADMIN_ID", int)
MONGO_URI = ensure_env("MONGO_URI")
API_ID = ensure_env("API_ID", int)
API_HASH = ensure_env("API_HASH")
