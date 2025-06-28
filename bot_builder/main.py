from pyrogram import Client, filters
from pyrogram.types import Message
from telethon.sync import TelegramClient
from telethon.sessions import StringSession
from telethon.errors import SessionPasswordNeededError

from config import BOT_TOKEN, ADMIN_ID, API_ID, API_HASH
from database import *
from conversation import ConversationManager

import asyncio

conv = ConversationManager()
bot = Client("bot_session", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)


# === /start ===
@bot.on_message(filters.command("start") & filters.private)
async def start(client, message: Message):
    await message.reply(
        "👋 Halo! Kirim `/makebot` untuk membuat userbot.\n\n📌 Hanya user yang diizinkan dapat menggunakan fitur ini."
    )


# === /allowuser (admin only) ===
@bot.on_message(filters.command("allowuser") & filters.user(ADMIN_ID))
async def allow_user_cmd(_, message: Message):
    if len(message.command) < 2:
        return await message.reply("Usage: /allowuser <user_id>")
    try:
        user_id = int(message.command[1])
        add_user(user_id)
        await message.reply(f"✅ User `{user_id}` diizinkan membuat userbot.")
    except:
        await message.reply("❌ Gagal menambahkan user.")


# === /makebot ===
@bot.on_message(filters.command("makebot") & filters.private)
async def makebot(client, message: Message):
    user_id = message.from_user.id

    if not is_user_allowed(user_id):
        return await message.reply("🚫 Kamu tidak diizinkan membuat userbot.")

    conv.start(user_id, "awaiting_api_id")
    await message.reply("Masukkan API ID kamu:")


# === Global handler untuk percakapan ===
@bot.on_message(filters.private & filters.text)
async def handle_inputs(client, message: Message):
    user_id = message.from_user.id
    state = conv.get_state(user_id)

    if not state:
        return

    if state == "awaiting_api_id":
        try:
            conv.set_data(user_id, "api_id", int(message.text))
            conv.set_state(user_id, "awaiting_api_hash")
            await message.reply("Masukkan API HASH kamu:")
        except:
            await message.reply("❌ API ID tidak valid. Masukkan angka.")

    elif state == "awaiting_api_hash":
        conv.set_data(user_id, "api_hash", message.text.strip())
        conv.set_state(user_id, "awaiting_phone")
        await message.reply("Masukkan nomor HP kamu (contoh: +62xxxxxxxxxx):")

    elif state == "awaiting_phone":
        phone = message.text.strip()
        conv.set_data(user_id, "phone", phone)
        await message.reply("📲 Mengirim kode OTP ke akun kamu...")

        try:
            data = conv.get_data(user_id)
            client_telethon = TelegramClient(StringSession(), data["api_id"], data["api_hash"])
            await client_telethon.connect()
            await client_telethon.send_code_request(phone)

            conv.set_data(user_id, "client", client_telethon)
            conv.set_state(user_id, "awaiting_otp")
            await message.reply("Masukkan kode OTP yang kamu terima:")
        except Exception as e:
            await message.reply(f"❌ Gagal kirim kode: {e}")
            conv.end(user_id)

    elif state == "awaiting_otp":
        otp = message.text.strip()
        data = conv.get_data(user_id)
        client_telethon = data.get("client")
        phone = data.get("phone")

        try:
            await client_telethon.sign_in(phone, otp)
        except SessionPasswordNeededError:
            await message.reply("🔐 Akun ini menggunakan verifikasi dua langkah (password).\nMasukkan password kamu:")

            password_msg = await bot.listen(user_id)
            password = password_msg.text.strip()

            try:
                await client_telethon.sign_in(password=password)
            except Exception as e:
                await message.reply(f"❌ Gagal login dengan password: {e}")
                await client_telethon.disconnect()
                conv.end(user_id)
                return
        except Exception as e:
            await message.reply(f"❌ Gagal login: {e}")
            await client_telethon.disconnect()
            conv.end(user_id)
            return

        # Jika berhasil login
        session_str = client_telethon.session.save()
        save_session(user_id, session_str)
        await client_telethon.disconnect()
        await message.reply("✅ Userbot berhasil dibuat dan disimpan!\nSilakan jalankan userbot kamu.")
        conv.end(user_id)


# === /status ===
@bot.on_message(filters.command("status") & filters.private)
async def status(_, message: Message):
    user_id = message.from_user.id
    if get_session(user_id):
        await message.reply("✅ Session userbot kamu tersimpan.")
    else:
        await message.reply("🚫 Kamu belum membuat userbot.")


# === /stopbot ===
@bot.on_message(filters.command("stopbot") & filters.private)
async def stopbot(_, message: Message):
    user_id = message.from_user.id
    if get_session(user_id):
        delete_session(user_id)
        await message.reply("🛑 Session kamu sudah dihapus.")
    else:
        await message.reply("⚠️ Tidak ada session ditemukan.")


# === /sudolist ===
@bot.on_message(filters.command("sudolist") & filters.user(ADMIN_ID))
async def sudolist(_, message: Message):
    sudo_users = get_sudo_list()
    text = "👑 Daftar SUDO:\n"
    text += "\n".join([f"- `{uid}`" for uid in sudo_users]) or "Tidak ada."
    await message.reply(text)


# === RUN BOT ===
print("🤖 Bot pusat aktif.")
bot.run()
