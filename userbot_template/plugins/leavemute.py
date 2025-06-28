from telethon import events
from telethon.tl.functions.channels import LeaveChannelRequest
from telethon.tl.functions.channels import GetParticipantRequest
from telethon.tl.types import ChannelParticipantSelf

def register(client):
    @client.on(events.NewMessage(pattern=r"^.leavemute$", outgoing=True))
    async def leavemute_handler(event):
        left, skipped = 0, 0
        await event.edit("🔍 Mengecek grup untuk mute...")

        async for dialog in client.iter_dialogs():
            if not dialog.is_group:
                continue
            try:
                user_participant = await client(GetParticipantRequest(dialog.entity, 'me'))
                if isinstance(user_participant.participant, ChannelParticipantSelf):
                    if getattr(user_participant.participant, 'muted', False):
                        await client(LeaveChannelRequest(dialog.entity))
                        left += 1
                    else:
                        skipped += 1
            except Exception:
                skipped += 1
                continue

        await event.edit(f"✅ Selesai!\n🚪 Keluar dari: {left} grup\n✅ Aman di: {skipped} grup")# Leave groups that mute the user
