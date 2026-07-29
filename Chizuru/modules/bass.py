from pyrogram import filters
from pyrogram.types import Message
from Chizuru import Chizuru

@Chizuru.on_message(filters.command("bass") & filters.group)
async def bass_command(client, message: Message):
    await message.reply_text("🔊 **Bass Boost:** Coming Soon!")
