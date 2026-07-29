import motor.motor_asyncio
from config import Config

class UsersDB:
    def __init__(self):
        self.client = motor.motor_asyncio.AsyncIOMotorClient(Config.MONGO_URL)
        self.db = self.client['ChizuruMusic']
        self.collection = self.db['users']
    
    async def add_user(self, user_id, username=""):
        if not await self.get_user(user_id):
            await self.collection.insert_one({
                'user_id': user_id,
                'username': username
            })
    
    async def get_user(self, user_id):
        return await self.collection.find_one({'user_id': user_id})
    
    async def get_all_users(self):
        return await self.collection.find().to_list(None)

users_db = UsersDB()
