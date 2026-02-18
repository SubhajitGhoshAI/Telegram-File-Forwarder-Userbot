import os

# Environment Variables থেকে ডাটা নেওয়া হচ্ছে
API_ID = int(os.environ.get("API_ID", "0"))
API_HASH = os.environ.get("API_HASH", "")
SESSION_STRING = os.environ.get("SESSION_STRING", "") # তোমার Pyrogram সেশন স্ট্রিং

# সোর্স চ্যানেলগুলো এখানে লিস্ট আকারে থাকবে (ID সহ)
# উদাহরণ: [-1001234567890, -1009876543210]
# Environment Variable এ কমা দিয়ে লিখবে: -100123,-100456
SOURCE_CHANNELS = [int(x) for x in os.environ.get("SOURCE_CHANNELS", "").split(",") if x]

# যেখানে ফাইল পাঠানো হবে
DESTINATION_CHANNEL = int(os.environ.get("DESTINATION_CHANNEL", "0"))

# MongoDB URL
MONGO_URL = os.environ.get("MONGO_URL", "")

# পোর্ট (Web server এর জন্য)
PORT = int(os.environ.get("PORT", "8080"))
