import motor.motor_asyncio
from config import Config

class ChatsDB:
    def __init__(self):
        if Config.MONGO_URL:
            self.client = motor.motor_asyncio.AsyncIOMotorClient(Config.MONGO_URL)
            self.db = self.client['ChizuruMusic']
            self.collection = self.db['chats']
    
    async def add_chat(self, chat_id):
        if not Config.MONGO_URL:
            return
        if not await self.get_chat(chat_id):
            await self.collection.insert_one({'chat_id': chat_id})
    
    async def get_chat(self, chat_id):
        if not Config.MONGO_URL:
            return None
        return await self.collection.find_one({'chat_id': chat_id})
    
    async def remove_chat(self, chat_id):
        if not Config.MONGO_URL:
            return
        await self.collection.delete_one({'chat_id': chat_id})

chats_db = ChatsDB()
