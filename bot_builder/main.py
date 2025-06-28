from database import *
from pyrogram import Client, filters
from pyrogram.types import Message
from telethon.sync import TelegramClient
from telethon.sessions import StringSession
import asyncio

# Tambahkan ini:
from config import BOT_TOKEN, ADMIN_ID, API_ID, API_HASH

# Ubah baris ini:
bot = Client("bot_session", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)


# ==== COMMANDS ====

@bot.on_message(filters.command("start") & filters.private)
async def start(client, message: Message):
    user_id = message.from_user.id
    await message.reply_text("👋 Halo! Kirim `/makebot` untuk membuat userbot.\n\n📌 Hanya user terverifikasi yang diizinkan.")

@bot.on_message(filters.command("allowuser") & filters.user(ADMIN_ID))
async def allow_user_cmd(_, message: Message):
    if len(message.command) < 2:
        return await message.reply("Usage: /allowuser <user_id>")
    try:
        user_id = int(message.command[1])
        add_user(user_id)
        await message.reply(f"✅ User `{user_id}` diizinkan membuat userbot.")
    except:
        await message.reply("❌ Gagal menambahkan.")

@bot.on_message(filters.command("makebot") & filters.private)
async def make_bot(client, message: Message):
    user_id = message.from_user.id
    if not is_user_allowed(user_id):
        return await message.reply("🚫 Kamu tidak diizinkan membuat userbot.")

    await message.reply("Masukkan API ID kamu:")
    api_id_msg = await bot.listen(user_id)
    API_ID_TEMP[user_id] = int(api_id_msg.text)

    await message.reply("Masukkan API HASH kamu:")
    api_hash_msg = await bot.listen(user_id)
    API_HASH_TEMP[user_id] = api_hash_msg.text

    await message.reply("Masukkan nomor telepon akun kamu (dalam format internasional, contoh: `+628xxxxxxxxx`):")
    phone_msg = await bot.listen(user_id)
    phone = phone_msg.text

    await message.reply("📲 Mengirim kode OTP ke akun kamu...")
    try:
        client_telethon = TelegramClient(StringSession(), API_ID_TEMP[user_id], API_HASH_TEMP[user_id])
        await client_telethon.connect()
        code_sent = await client_telethon.send_code_request(phone)

        await message.reply("Masukkan kode OTP (tanpa spasi):")
        otp_msg = await bot.listen(user_id)
        otp_code = otp_msg.text.strip()

        await client_telethon.sign_in(phone, otp_code)
        session_str = client_telethon.session.save()

        save_session(user_id, session_str)
        await message.reply("✅ Userbot berhasil dibuat!\n\nGunakan `.menu` di akun kamu.")
        await client_telethon.disconnect()

    except Exception as e:
        await message.reply(f"❌ Gagal login: {e}")


@bot.on_message(filters.command("status") & filters.private)
async def status(_, message: Message):
    user_id = message.from_user.id
    if get_session(user_id):
        await message.reply("✅ Session userbot kamu tersimpan.")
    else:
        await message.reply("🚫 Kamu belum membuat userbot.")

@bot.on_message(filters.command("stopbot") & filters.private)
async def stopbot(_, message: Message):
    user_id = message.from_user.id
    if get_session(user_id):
        delete_session(user_id)
        await message.reply("🛑 Session kamu sudah dihapus.")
    else:
        await message.reply("⚠️ Tidak ada session ditemukan.")

@bot.on_message(filters.command("sudolist") & filters.user(ADMIN_ID))
async def sudolist(_, message: Message):
    sudo_users = get_sudo_list()
    text = "👑 Daftar SUDO:\n"
    text += "\n".join([f"- `{uid}`" for uid in sudo_users]) or "Tidak ada."
    await message.reply(text)


# === Run Bot ===
print("🤖 Bot pusat aktif.")
bot.run()
