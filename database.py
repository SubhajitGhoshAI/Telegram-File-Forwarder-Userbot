import motor.motor_asyncio
from config import MONGO_URL

class Database:
    def __init__(self, uri, database_name):
        self._client = motor.motor_asyncio.AsyncIOMotorClient(uri)
        self.db = self._client[database_name]
        self.col = self.db.queue

    # নতুন ফাইল কিউতে যোগ করা
    async def add_to_queue(self, chat_id, message_id):
        await self.col.insert_one({
            "chat_id": chat_id,
            "message_id": message_id,
            "status": "pending"
        })

    # নির্দিষ্ট চ্যানেলের পেন্ডিং ফাইল খোঁজা (সবচেয়ে পুরনোটি আগে)
    async def get_next_from_channel(self, chat_id):
        return await self.col.find_one(
            {"chat_id": chat_id, "status": "pending"},
            sort=[("_id", 1)] # FIFO (First In First Out)
        )

    # কাজ শেষ হলে কিউ থেকে ডিলিট করা
    async def remove_from_queue(self, task_id):
        await self.col.delete_one({"_id": task_id})

db = Database(MONGO_URL, "UserBotQueue")
