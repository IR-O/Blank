from pyrogram import filters
from pyrogram.types import Message
from Chizuru import Chizuru
import time

@Chizuru.on_message(filters.command("ping"))
async def ping_command(client, message: Message):
    start = time.time()
    msg = await message.reply_text("🏓 **Pinging...**")
    end = time.time()
    await msg.edit_text(f"🏓 **Pong!**\n\n📊 **Latency:** `{round((end - start) * 1000)}ms`")
