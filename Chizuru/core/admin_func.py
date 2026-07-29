from functools import wraps
from pyrogram.types import Message
from config import Config

AUTHORIZED_USERS = [Config.OWNER_ID]

def authorized_users(func):
    @wraps(func)
    async def wrapper(client, message: Message):
        if message.from_user.id in AUTHORIZED_USERS:
            return await func(client, message)
        else:
            await message.reply_text("❌ You are not authorized!")
    return wrapper

admins = {}

async def set_admins(chat_id, admin_list):
    admins[chat_id] = admin_list

async def get_admins(chat_id):
    return admins.get(chat_id, [])
