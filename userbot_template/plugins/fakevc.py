from telethon import events
from telethon.tl.functions.phone import CreateGroupCallRequest
from telethon.tl.functions.channels import GetFullChannelRequest
from telethon.tl.functions.phone import JoinGroupCallRequest
from telethon.tl.types import InputGroupCall, InputPeerChannel

def register(client):
    @client.on(events.NewMessage(pattern=r"^.fakevc$"))
    async def fakevc(event):
        chat = await event.get_chat()
        if not getattr(chat, 'creator', False) and not getattr(chat, 'admin_rights', None):
            return await event.reply("🚫 Kamu harus admin untuk memulai fake voice chat.")

        try:
            full_chat = await client(GetFullChannelRequest(channel=chat))
            call = full_chat.full_chat.call

            if not call:
                await client(CreateGroupCallRequest(
                    peer=chat,
                    random_id=client.rnd_id(),
                ))
                full_chat = await client(GetFullChannelRequest(channel=chat))

            call = full_chat.full_chat.call
            await client(JoinGroupCallRequest(
                call=InputGroupCall(id=call.id, access_hash=call.access_hash),
                peer=InputPeerChannel(chat.id, chat.access_hash),
                join_as=await client.get_me(),
                params={"mute": True}
            ))

            await event.reply("✅ Fake voice chat dimulai.")

        except Exception as e:
            await event.reply(f"❌ Gagal join fake VC: {e}")# Fake VC join
