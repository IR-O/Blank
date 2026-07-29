from pyrogram import filters
from pyrogram.types import Message
from Chizuru import Chizuru

@Chizuru.on_message(filters.command("ai") & filters.user(Config.OWNER_ID))
async def ai_command(client, message: Message):
    await message.reply_text("🤖 **AI Module:** Coming Soon!")
