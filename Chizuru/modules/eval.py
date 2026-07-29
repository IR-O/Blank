from pyrogram import filters
from pyrogram.types import Message
from Chizuru import Chizuru
from config import Config
import sys

@Chizuru.on_message(filters.command("eval") & filters.user(Config.OWNER_ID))
async def eval_command(client, message: Message):
    if len(message.command) < 2:
        await message.reply_text("❌ **Usage:** `/eval <code>`")
        return
    
    code = " ".join(message.command[1:])
    try:
        result = eval(code)
        await message.reply_text(f"📊 **Result:**\n`{result}`")
    except Exception as e:
        await message.reply_text(f"❌ **Error:** `{str(e)}`")
