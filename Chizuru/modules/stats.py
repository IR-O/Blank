from pyrogram import filters
from pyrogram.types import Message
from Chizuru import Chizuru
from config import Config

@Chizuru.on_message(filters.command("stats") & filters.user(Config.OWNER_ID))
async def stats_command(client, message: Message):
    await message.reply_text(
        f"📊 **Bot Statistics**\n\n"
        f"⚡ **Status:** Online\n"
        f"💻 **Version:** 1.0.0\n"
        f"👨‍💻 **Developer:** @narratorxcb"
    )
