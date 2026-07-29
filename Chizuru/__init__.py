from pyrogram import Client
from config import Config
from pytgcalls import PyTgCalls

# Bot Client
Chizuru = Client(
    name=Config.SESSION_NAME,
    api_id=Config.API_ID,
    api_hash=Config.API_HASH,
    bot_token=Config.BOT_TOKEN
)

# Assistant Client
userbot = Client(
    name="assistant",
    api_id=Config.ASSISTANT_API_ID,
    api_hash=Config.ASSISTANT_API_HASH,
    session_string=Config.ASSISTANT_SESSION
)

# PyTgCalls
pytgcalls = PyTgCalls(userbot)

# Import modules
from Chizuru import modules
