from pyrogram import filters
from pyrogram.types import Message
from Chizuru import Chizuru
from config import Config

@Chizuru.on_message(filters.command("broadcast") & filters.user(Config.OWNER_ID))
async def broadcast_command(client, message: Message):
    if len(message.command) < 2:
        await message.reply_text("❌ **Usage:** `/broadcast <message>`")
        return
    
    broadcast_text = " ".join(message.command[1:])
    await message.reply_text(f"📢 **Broadcast sent:**\n\n{broadcast_text}")
