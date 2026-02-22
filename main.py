import asyncio
import logging
import time
from aiohttp import web
from pyrogram import Client, filters, idle
from pyrogram.errors import FloodWait
from config import API_ID, API_HASH, SESSION_STRING, SOURCE_CHANNELS, DESTINATION_CHANNEL, PORT
from database import db

# লগিং সেটআপ
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# ইউজারবট ক্লায়েন্ট
app = Client(
    "my_userbot",
    api_id=API_ID,
    api_hash=API_HASH,
    session_string=SESSION_STRING
)

# বট স্টার্ট হওয়ার সময়
START_TIME = time.time()

# --- Web Server for Health Check (Koyeb/Render) ---
async def web_server():
    async def handle(request):
        return web.Response(text="Bot is Running High Performance Mode!")

    webapp = web.Application()
    webapp.router.add_get("/", handle)
    runner = web.AppRunner(webapp)
    await runner.setup()
    site = web.TCPSite(runner, "0.0.0.0", PORT)
    await site.start()
    logger.info(f"Web server started on port {PORT}")

# --- Message Listener ---
# শুধুমাত্র ভিডিও এবং ফাইল (ডকুমেন্ট) ধরবে।
@app.on_message(filters.chat(SOURCE_CHANNELS) & (filters.document | filters.video))
async def incoming_handler(client, message):
    # বট স্টার্ট হওয়ার আগের মেসেজ ইগনোর করবে
    if message.date.timestamp() < START_TIME:
        return

    # ডাটাবেসে যোগ করা হচ্ছে
    await db.add_to_queue(message.chat.id, message.id)
    logger.info(f"Added to queue: Msg ID {message.id} from {message.chat.title}")

# --- Worker Loop (Round Robin Logic) ---
async def worker_loop():
    logger.info("Worker started processing...")
    while True:
        try:
            # আমরা সোর্স চ্যানেলগুলোর লিস্ট ধরে লুপ চালাবো
            for channel_id in SOURCE_CHANNELS:
                while True:
                    try:
                        # এই চ্যানেলের কোনো পেন্ডিং ফাইল আছে কিনা চেক করা (DB Error Handle করার জন্য try এর ভেতরে)
                        task = await db.get_next_from_channel(channel_id)
                        
                        if not task:
                            # যদি এই চ্যানেলে আর কোনো ফাইল না থাকে, লুপ ব্রেক করে পরের চ্যানেলে যাবে
                            break 
                        
                        # ফাইল পাঠানো শুরু
                        logger.info(f"Forwarding Msg {task['message_id']} from {channel_id}")
                        
                        await app.copy_message(
                            chat_id=DESTINATION_CHANNEL,
                            from_chat_id=task['chat_id'],
                            message_id=task['message_id']
                        )
                        
                        # সফল হলে ডাটাবেস থেকে মুছে ফেলা
                        await db.remove_from_queue(task['_id'])
                        
                        # ৩ সেকেন্ড ডিলে
                        await asyncio.sleep(3)
                        
                    except FloodWait as e:
                        logger.warning(f"FloodWait hit! Sleeping for {e.value} seconds.")
                        await asyncio.sleep(e.value)
                    except Exception as e:
                        logger.error(f"Worker Error: {e}")
                        # যদি সোর্স মেসেজ ডিলিট হয়ে যায় বা অন্য এরর হয়, তাহলে স্কিপ করে মুছে ফেলবে
                        if 'task' in locals() and task:
                            logger.info("Skipping broken message")
                            await db.remove_from_queue(task['_id'])
                        await asyncio.sleep(5)
            
            # সব চ্যানেলের কাজ শেষ হলে ৩ সেকেন্ড বিশ্রাম নিয়ে আবার চেক করবে
            await asyncio.sleep(3)
            
        except Exception as e:
            logger.error(f"Critical Worker Error: {e}")
            await asyncio.sleep(5)

# --- Main Entry Point ---
async def main():
    await app.start()
    logger.info("Userbot Started!")
    
    # ওয়েব সার্ভার এবং ওয়ার্কার একসাথে চালানো
    await asyncio.gather(
        web_server(),
        worker_loop(),
        idle()
    )

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
