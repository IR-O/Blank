import os
from pyrogram import filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from Chizuru import Chizuru, userbot, pytgcalls
from Chizuru.core.utils import search_song, get_audio_stream, get_video_stream, queue
from Chizuru.core.thumb_func import generate_cover
from Chizuru.core.strings import CLOSE_BUTTON
from config import Config

queues = {}

async def add_to_queue(chat_id, file, song_info):
    if chat_id not in queues:
        queues[chat_id] = []
    queues[chat_id].append({'file': file, 'info': song_info})
    return len(queues[chat_id])

async def get_from_queue(chat_id):
    if chat_id in queues and queues[chat_id]:
        return queues[chat_id].pop(0)
    return None

@Chizuru.on_message(filters.command(["play", "vplay"]))
async def play_command(client, message: Message):
    is_video = message.command[0].startswith("v")
    
    if len(message.command) < 2:
        await message.reply_text("❌ **Usage:** `/play <song name>`")
        return
    
    query = " ".join(message.command[1:])
    chat_id = message.chat.id
    user_name = message.from_user.mention
    
    msg = await message.reply_text("🔍 **Searching...**")
    
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
        
        song_info = await search_song(query)
        if not song_info:
            await msg.edit_text("❌ **Song not found!**")
            return
        
        if song_info['duration_sec'] > Config.DURATION_LIMIT * 60:
            await msg.edit_text(f"❌ **Song too long! Max {Config.DURATION_LIMIT} minutes.**")
            return
        
        if is_video:
            stream_url = await get_video_stream(song_info['link'])
        else:
            stream_url = await get_audio_stream(song_info['link'])
        
        if not stream_url:
            await msg.edit_text("❌ **Failed to get stream!**")
            return
        
        await generate_cover(
            user_name,
            song_info['title'],
            song_info['views'],
            song_info['duration'],
            song_info['thumbnail']
        )
        
        active_calls = [int(call.chat_id) for call in pytgcalls.active_calls]
        
        if chat_id in active_calls:
            position = await add_to_queue(chat_id, stream_url, song_info)
            await message.reply_photo(
                photo="final.png",
                caption=f"**➻ Added to Queue » {position}**\n\n"
                        f"🏷️ **Name:** [{song_info['title']}]({song_info['link']})\n"
                        f"⏰ **Duration:** `{song_info['duration']}`\n"
                        f"👤 **Requested by:** {user_name}",
                reply_markup=CLOSE_BUTTON
            )
        else:
            if is_video:
                from pytgcalls.types import VideoPiped
                await pytgcalls.join_group_call(chat_id, VideoPiped(stream_url))
            else:
                from pytgcalls.types import AudioPiped
                await pytgcalls.join_group_call(chat_id, AudioPiped(stream_url))
            
            await message.reply_photo(
                photo="final.png",
                caption=f"**➻ Started Streaming**\n\n"
                        f"🏷️ **Name:** [{song_info['title']}]({song_info['link']})\n"
                        f"⏰ **Duration:** `{song_info['duration']}`\n"
                        f"👀 **Views:** {song_info['views']}\n"
                        f"👤 **Requested by:** {user_name}",
                reply_markup=InlineKeyboardMarkup([
                    [InlineKeyboardButton("⏸ Pause", callback_data="pause"),
                     InlineKeyboardButton("⏹ Stop", callback_data="stop")],
                    [InlineKeyboardButton("❌ Close", callback_data="close_data")]
                ])
            )
        
        os.remove("final.png")
        await msg.delete()
        
    except Exception as e:
        await msg.edit_text(f"❌ **Error:** {str(e)[:200]}")

@Chizuru.on_message(filters.command("skip"))
async def skip_command(client, message: Message):
    chat_id = message.chat.id
    
    next_song = await get_from_queue(chat_id)
    if next_song:
        from pytgcalls.types import AudioPiped
        await pytgcalls.change_stream(
            chat_id,
            AudioPiped(next_song['file'])
        )
        await message.reply_text(f"⏭️ **Skipped to:** {next_song['info']['title']}")
    else:
        await pytgcalls.leave_group_call(chat_id)
        await message.reply_text("⏹️ **Queue empty! Stopped.**")

@Chizuru.on_message(filters.command("pause"))
async def pause_command(client, message: Message):
    chat_id = message.chat.id
    try:
        await pytgcalls.pause_stream(chat_id)
        await message.reply_text(f"⏸️ **Paused by** {message.from_user.mention}")
    except:
        await message.reply_text("❌ **Nothing to pause!**")

@Chizuru.on_message(filters.command("resume"))
async def resume_command(client, message: Message):
    chat_id = message.chat.id
    try:
        await pytgcalls.resume_stream(chat_id)
        await message.reply_text(f"▶️ **Resumed by** {message.from_user.mention}")
    except:
        await message.reply_text("❌ **Nothing to resume!**")

@Chizuru.on_message(filters.command("stop"))
async def stop_command(client, message: Message):
    chat_id = message.chat.id
    try:
        await pytgcalls.leave_group_call(chat_id)
        if chat_id in queues:
            queues[chat_id] = []
        await message.reply_text(f"⏹️ **Stopped by** {message.from_user.mention}")
    except:
        await message.reply_text("❌ **Nothing to stop!**")

@Chizuru.on_message(filters.command("queue"))
async def queue_command(client, message: Message):
    chat_id = message.chat.id
    if chat_id in queues and queues[chat_id]:
        queue_text = f"📋 **Queue ({len(queues[chat_id])}):**\n\n"
        for i, song in enumerate(queues[chat_id][:10], 1):
            queue_text += f"{i}. 🎵 {song['info']['title'][:30]}\n"
        await message.reply_text(queue_text)
    else:
        await message.reply_text("📋 **Queue is empty!**")

@Chizuru.on_message(filters.command("volume"))
async def volume_command(client, message: Message):
    if len(message.command) < 2:
        await message.reply_text("❌ **Usage:** `/volume 50`")
        return
    
    try:
        volume = int(message.command[1])
        if 0 <= volume <= 200:
            chat_id = message.chat.id
            await pytgcalls.change_volume_call(chat_id, volume)
            await message.reply_text(f"🔊 **Volume set to {volume}%**")
        else:
            await message.reply_text("❌ **Volume must be between 0 and 200!**")
    except:
        await message.reply_text("❌ **Invalid volume!**")

@Chizuru.on_message(filters.command("current"))
async def current_command(client, message: Message):
    await message.reply_text("🎵 **Current song information is not available right now.**")

from pytgcalls.types import Update

@pytgcalls.on_stream_end()
async def on_stream_end(_, update: Update):
    chat_id = update.chat_id
    next_song = await get_from_queue(chat_id)
    if next_song:
        from pytgcalls.types import AudioPiped
        await pytgcalls.change_stream(
            chat_id,
            AudioPiped(next_song['file'])
        )
    else:
        await pytgcalls.leave_group_call(chat_id)
