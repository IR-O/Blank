from pyrogram import filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from Chizuru import Chizuru
from Chizuru.core.strings import START_TEXT, HELP_TEXT

@Chizuru.on_message(filters.command("start"))
async def start_command(client, message: Message):
    user = message.from_user
    await message.reply_text(
        START_TEXT.format(user.first_name),
        reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton("📚 Help", callback_data="help"),
             InlineKeyboardButton("📢 Updates", url="https://t.me/your_channel")],
            [InlineKeyboardButton("👨‍💻 Developer", url="https://t.me/narratorxcb")]
        ]),
        disable_web_page_preview=True
    )

@Chizuru.on_callback_query()
async def callback_handler(client, callback_query):
    data = callback_query.data
    
    if data == "help":
        await callback_query.message.edit_text(
            HELP_TEXT,
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("🔙 Back", callback_data="back")]
            ])
        )
    
    elif data == "back":
        user = callback_query.from_user
        await callback_query.message.edit_text(
            START_TEXT.format(user.first_name),
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("📚 Help", callback_data="help"),
                 InlineKeyboardButton("📢 Updates", url="https://t.me/your_channel")],
                [InlineKeyboardButton("👨‍💻 Developer", url="https://t.me/narratorxcb")]
            ])
        )
    
    elif data == "pause":
        await callback_query.answer("⏸️ Paused!")
    
    elif data == "resume":
        await callback_query.answer("▶️ Resumed!")
    
    elif data == "stop":
        await callback_query.answer("⏹️ Stopped!")
        await callback_query.message.delete()
    
    elif data == "close_data":
        await callback_query.message.delete()
        await callback_query.answer("Closed!")
