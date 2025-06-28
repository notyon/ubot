from telethon import events
from config import SUDO_USERS

def register(client):
    @client.on(events.NewMessage(pattern=r"^.addsudo (\d+)", outgoing=True))
    async def addsudo(event):
        user_id = event.pattern_match.group(1)
        if str(event.sender_id) not in SUDO_USERS:
            return await event.reply("🚫 Kamu bukan SUDO.")
        if user_id not in SUDO_USERS:
            SUDO_USERS.append(user_id)
            await event.reply(f"✅ User {user_id} ditambahkan ke SUDO.")
        else:
            await event.reply("ℹ️ Sudah ada di daftar SUDO.")

    @client.on(events.NewMessage(pattern=r"^.delsudo (\d+)", outgoing=True))
    async def delsudo(event):
        user_id = event.pattern_match.group(1)
        if str(event.sender_id) not in SUDO_USERS:
            return await event.reply("🚫 Kamu bukan SUDO.")
        if user_id in SUDO_USERS:
            SUDO_USERS.remove(user_id)
            await event.reply(f"✅ User {user_id} dihapus dari SUDO.")
        else:
            await event.reply("⚠️ Tidak ada di daftar SUDO.")

    @client.on(events.NewMessage(pattern=r"^.sudolist$", outgoing=True))
    async def sudolist(event):
        text = "👑 Daftar SUDO:\n"
        text += "\n".join([f"- `{uid}`" for uid in SUDO_USERS]) or "Kosong."
        await event.reply(text)# SUDO control feature
