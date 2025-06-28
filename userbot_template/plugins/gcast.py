from telethon import events
from config import GCAST_BLACKLIST
from time import sleep

def register(client):
    @client.on(events.NewMessage(pattern=r"^.gcast(?: |$)(.*)", outgoing=True))
    async def gcast(event):
        msg = event.pattern_match.group(1)
        if not msg:
            return await event.reply("🚫 Masukkan teks untuk di-GCAST.\nContoh: `.gcast Halo semua!`")

        sent, failed = 0, 0
        await event.edit("🚀 Memulai GCAST...")

        async for dialog in client.iter_dialogs():
            if dialog.is_group or dialog.is_channel:
                chat_id = str(dialog.id)
                if chat_id in GCAST_BLACKLIST:
                    continue
                try:
                    await client.send_message(dialog.id, msg)
                    sent += 1
                except Exception:
                    failed += 1
                    continue
                sleep(0.5)  # Hindari spam flood

        await event.edit(f"✅ GCAST selesai!\n📨 Berhasil: {sent}\n❌ Gagal: {failed}")# GCAST feature
