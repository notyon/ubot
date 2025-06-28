from telethon import events
import asyncio
from config import GCAST_BLACKLIST

def register(client):
    @client.on(events.NewMessage(pattern=r"^.gspam (\d+) (\d+(?:\.\d+)?) (.+)", outgoing=True))
    async def gspam_handler(event):
        count = int(event.pattern_match.group(1))
        delay = float(event.pattern_match.group(2))
        text = event.pattern_match.group(3)

        if count > 30:
            return await event.edit("🚫 Jumlah spam terlalu besar! Max 30.")

        sent, failed = 0, 0
        await event.edit("📡 Mengirim spam global...")

        async for dialog in client.iter_dialogs():
            if dialog.is_group or dialog.is_channel:
                chat_id = str(dialog.id)
                if chat_id in GCAST_BLACKLIST:
                    continue
                try:
                    for _ in range(count):
                        await client.send_message(dialog.id, text)
                        await asyncio.sleep(delay)
                    sent += 1
                except Exception:
                    failed += 1
                    continue

        await event.edit(f"✅ GSpam selesai!\n🟢 Grup sukses: {sent}\n🔴 Gagal: {failed}")# Global SPAM with delay
