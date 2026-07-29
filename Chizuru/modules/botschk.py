from pyrogram import filters
from pyrogram.types import Message
from Chizuru import Chizuru

@Chizuru.on_message(filters.command("botschk") & filters.user(Config.OWNER_ID))
async def botschk_command(client, message: Message):
    await message.reply_text("✅ **Bot is running smoothly!**")
