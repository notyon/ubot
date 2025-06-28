from telethon import events
from telethon.tl.functions.channels import GetFullChannelRequest
from telethon.tl.functions.phone import CreateGroupCallRequest, JoinGroupCallRequest
from telethon.tl.types import InputGroupCall, InputPeerChannel
from time import sleep

def register(client):
    @client.on(events.NewMessage(pattern=r"^.gfakevc$", outgoing=True))
    async def gfakevc_handler(event):
        await event.edit("🚀 Memulai fake voice chat di semua grup...")

        count = 0
        async for dialog in client.iter_dialogs():
            if not dialog.is_group:
                continue
            try:
                entity = await client.get_entity(dialog.id)
                full = await client(GetFullChannelRequest(entity))
                call = full.full_chat.call

                # Kalau belum ada voice chat, buat dulu
                if not call:
                    await client(CreateGroupCallRequest(
                        peer=entity,
                        random_id=client.rnd_id()
                    ))
                    full = await client(GetFullChannelRequest(entity))
                    call = full.full_chat.call

                # Gabung ke voice chat
                await client(JoinGroupCallRequest(
                    call=InputGroupCall(id=call.id, access_hash=call.access_hash),
                    peer=InputPeerChannel(entity.id, entity.access_hash),
                    join_as=await client.get_me(),
                    params={"mute": True}
                ))

                count += 1
                sleep(1)
            except Exception:
                continue

        await event.edit(f"✅ Fake VC aktif di {count} grup.")# Global Fake VC
