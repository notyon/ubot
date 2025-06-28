from telethon import events

def register(client):
    @client.on(events.NewMessage(pattern=r"^.menu$", outgoing=True))
    async def menu_handler(event):
        menu_text = """
📖 **Userbot Menu**:

🔹 `.gcast <teks>`  
Kirim pesan ke semua grup/channel

🔹 `.spam <jumlah> <delay> <teks>`  
Spam dengan delay (contoh: `.spam 5 1 halo`)

🔹 `.gspam <jumlah> <delay> <teks>`  
Spam global ke semua grup (dengan delay)

🔹 `.fakevc`  
Gabung fake voice chat di grup saat ini

🔹 `.gfakevc`  
Gabung fake voice chat di semua grup

🔹 `.leavemute`  
Keluar dari grup yang membisukan akun kamu

🔹 `.menu`  
Tampilkan menu ini

🛡️ Admin-only:
🔹 `.addsudo <user_id>`  
🔹 `.delsudo <user_id>`  
🔹 `.sudolist`
        """
        await event.reply(menu_text)# .menu command with feature descriptions
