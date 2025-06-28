from telethon import events
import asyncio
import re

def register(client):
    @client.on(events.NewMessage(pattern=r"^.spam (\d+) (\d+(?:\.\d+)?) (.+)", outgoing=True))
    async def spam_handler(event):
        count = int(event.pattern_match.group(1))
        delay = float(event.pattern_match.group(2))
        text = event.pattern_match.group(3)

        if count > 50:
            return await event.reply("🚫 Terlalu banyak spam! Max: 50")

        await event.delete()
        for i in range(count):
            try:
                await event.respond(text)
                await asyncio.sleep(delay)
            except Exception as e:
                await event.respond(f"❌ Gagal spam ke-{i+1}: {e}")
                break# SPAM with delay
