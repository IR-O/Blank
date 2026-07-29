from pyrogram import filters
from pyrogram.types import Message
from Chizuru import Chizuru
from Chizuru.core.utils import yt

@Chizuru.on_message(filters.command("yt"))
async def youtube_command(client, message: Message):
    if len(message.command) < 2:
        await message.reply_text("❌ **Usage:** `/yt <song name>`")
        return
    
    query = " ".join(message.command[1:])
    msg = await message.reply_text("🔍 **Searching...**")
    
    try:
        result = await yt.search(query)
        if result:
            await msg.edit_text(
                f"🎵 **YouTube Search Result:**\n\n"
                f"🏷️ **Title:** {result['title']}\n"
                f"⏰ **Duration:** {result['duration']}\n"
                f"🔗 **URL:** {result['url']}"
            )
        else:
            await msg.edit_text("❌ **No results found!**")
    except Exception as e:
        await msg.edit_text(f"❌ **Error:** {str(e)}")
