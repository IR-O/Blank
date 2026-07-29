import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    # Bot Account
    API_ID: int = int(os.environ.get("API_ID", 0))
    API_HASH: str = os.environ.get("API_HASH", "")
    BOT_TOKEN: str = os.environ.get("BOT_TOKEN", "")
    
    # Assistant Account
    ASSISTANT_SESSION: str = os.environ.get("ASSISTANT_SESSION", "")
    ASSISTANT_API_ID: int = int(os.environ.get("ASSISTANT_API_ID", 0))
    ASSISTANT_API_HASH: str = os.environ.get("ASSISTANT_API_HASH", "")
    
    # Owner
    OWNER_ID: int = int(os.environ.get("OWNER_ID", 0))
    LOGGER_ID: int = int(os.environ.get("LOGGER_ID", -1001234567890))
    
    # MongoDB
    MONGO_URL: str = os.environ.get("MONGO_URL", "")
    
    # Settings
    DURATION_LIMIT: int = 300
    SESSION_NAME: str = "ChizuruMusic"
    START_IMG_URL: str = "https://graph.org/file/e3fa9ab16ebefbfdd29d9.jpg"
