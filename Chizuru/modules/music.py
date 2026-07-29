import os
from pyrogram import filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from pytgcalls.types import AudioPiped, VideoPiped, AudioQuality
from Chizuru import Chizuru, userbot, pytgcalls
from Chizuru.core.utils import yt, queue
from Chizuru.core.thumb_func import generate_cover
from Chizuru.core.strings import HELP_TEXT
from config import Config

active_calls = []

@Chizuru.on_message(filters.command(["play", "vplay"]) & filters.group)
async def play_handler(client, message: Message):
    is_video = message.command[0].startswith("v")
    chat_id = message.chat.id
    
    if len(message.command) < 2:
        await message.reply_text("❌ **Usage:** `/play <song name>`")
        return
    
    sent = await message.reply_text("🔍 **Searching...**")
    query = " ".join(message.command[1:])
    user_mention = message.from_user.mention
    
    try:
        from pyrogram.raw.functions.phone import CreateGroupCall
        try:
            await userbot.invoke(
                CreateGroupCall(
                    peer=await userbot.resolve_peer(chat_id),
                    title="Chizuru Music 🎵"
                )
            )
        except:
            pass
        
        media = await yt.search(query, video=is_video)
        if not media:
            await sent.edit_text("❌ **Song not found!**")
            return
        
        if media['duration_sec'] > Config.DURATION_LIMIT * 60:
            await sent.edit_text(f"❌ **Song too long! Max {Config.DURATION_LIMIT} minutes.**")
            return
        
        if chat_id in active_calls:
            position = await queue.add(chat_id, media)
            await sent.edit_text(
                f"🎵 **Added to Queue » {position}**\n\n"
                f"🏷️ **Name:** [{media['title']}]({media['url']})\n"
                f"⏰ **Duration:** `{media['duration']}`\n"
                f"👤 **Requested by:** {user_mention}"
            )
        else:
            await generate_cover(
                user_mention,
                media['title'],
                "0",
                media['duration'],
                "https://graph.org/file/e3fa9ab16ebefbfdd29d9.jpg"
            )
            
            if is_video:
                await pytgcalls.join_group_call(chat_id, VideoPiped(media['file_path']))
            else:
                await pytgcalls.join_group_call(chat_id, AudioPiped(media['file_path'], AudioQuality.STUDIO))
            
            if chat_id not in active_calls:
                active_calls.append(chat_id)
            
            await sent.delete()
            await message.reply_photo(
                photo="final.png",
                caption=f"🎵 **Now Playing:**\n\n"
                        f"🏷️ **Name:** [{media['title']}]({media['url']})\n"
                        f"⏰ **Duration:** `{media['duration']}`\n"
                        f"👤 **Requested by:** {user_mention}",
                reply_markup=InlineKeyboardMarkup([
                    [InlineKeyboardButton("⏸ Pause", callback_data="pause"),
                     InlineKeyboardButton("⏹ Stop", callback_data="stop")],
                    [InlineKeyboardButton("❌ Close", callback_data="close_data")]
                ])
            )
            os.remove("final.png")
    except Exception as e:
        await sent.edit_text(f"❌ **Error:** {str(e)[:200]}")

@Chizuru.on_callback_query()
async def callback_handler(client, callback_query):
    data = callback_query.data
    chat_id = callback_query.message.chat.id
    
    if data == "pause":
        try:
            await pytgcalls.pause_stream(chat_id)
            await callback_query.answer("⏸️ Paused!")
        except:
            await callback_query.answer("❌ Failed!")
    elif data == "resume":
        try:
            await pytgcalls.resume_stream(chat_id)
            await callback_query.answer("▶️ Resumed!")
        except:
            await callback_query.answer("❌ Failed!")
    elif data == "stop":
        try:
            await pytgcalls.leave_group_call(chat_id)
            if chat_id in active_calls:
                active_calls.remove(chat_id)
            await queue.clear(chat_id)
            await callback_query.answer("⏹️ Stopped!")
            await callback_query.message.delete()
        except:
            await callback_query.answer("❌ Failed!")
    elif data == "close_data":
        await callback_query.message.delete()
        await callback_query.answer("Closed!")

@Chizuru.on_message(filters.command("skip") & filters.group)
async def skip_handler(client, message: Message):
    chat_id = message.chat.id
    next_song = await queue.get(chat_id)
    
    if next_song:
        try:
            await pytgcalls.change_stream(chat_id, AudioPiped(next_song['file_path']))
            await message.reply_text(f"⏭️ **Skipped to:** {next_song['title']}")
        except:
            await message.reply_text("❌ **Failed to skip!**")
    else:
        try:
            await pytgcalls.leave_group_call(chat_id)
            if chat_id in active_calls:
                active_calls.remove(chat_id)
            await message.reply_text("⏹️ **Queue empty! Stopped.**")
        except:
            await message.reply_text("❌ **Nothing to skip!**")

@Chizuru.on_message(filters.command("pause") & filters.group)
async def pause_handler(client, message: Message):
    try:
        await pytgcalls.pause_stream(message.chat.id)
        await message.reply_text("⏸️ **Paused!**")
    except:
        await message.reply_text("❌ **Nothing to pause!**")

@Chizuru.on_message(filters.command("resume") & filters.group)
async def resume_handler(client, message: Message):
    try:
        await pytgcalls.resume_stream(message.chat.id)
        await message.reply_text("▶️ **Resumed!**")
    except:
        await message.reply_text("❌ **Nothing to resume!**")

@Chizuru.on_message(filters.command("stop") & filters.group)
async def stop_handler(client, message: Message):
    chat_id = message.chat.id
    try:
        await pytgcalls.leave_group_call(chat_id)
        if chat_id in active_calls:
            active_calls.remove(chat_id)
        await queue.clear(chat_id)
        await message.reply_text("⏹️ **Stopped!**")
    except:
        await message.reply_text("❌ **Nothing to stop!**")

@Chizuru.on_message(filters.command("queue") & filters.group)
async def queue_handler(client, message: Message):
    chat_id = message.chat.id
    all_songs = await queue.get_all(chat_id)
    
    if all_songs:
        text = f"📋 **Queue ({len(all_songs)}):**\n\n"
        for i, song in enumerate(all_songs[:10], 1):
            text += f"{i}. 🎵 {song['title'][:30]}\n"
        await message.reply_text(text)
    else:
        await message.reply_text("📋 **Queue is empty!**")

@Chizuru.on_message(filters.command("volume") & filters.group)
async def volume_handler(client, message: Message):
    if len(message.command) < 2:
        await message.reply_text("❌ **Usage:** `/volume 50`")
        return
    
    try:
        volume = int(message.command[1])
        if 0 <= volume <= 200:
            await pytgcalls.change_volume_call(message.chat.id, volume)
            await message.reply_text(f"🔊 **Volume set to {volume}%**")
        else:
            await message.reply_text("❌ **Volume must be between 0 and 200!**")
    except:
        await message.reply_text("❌ **Invalid volume!**")

@Chizuru.on_message(filters.command("current") & filters.group)
async def current_handler(client, message: Message):
    chat_id = message.chat.id
    current = await queue.get_all(chat_id)
    
    if current:
        song = current[0]
        await message.reply_text(
            f"🎵 **Currently Playing:**\n"
            f"🏷️ **Name:** {song['title']}\n"
            f"⏰ **Duration:** {song['duration']}\n"
            f"📌 **Status:** {'▶️ Playing' if chat_id in active_calls else '⏸️ Paused'}"
        )
    else:
        await message.reply_text("❌ **No song is playing!**")
