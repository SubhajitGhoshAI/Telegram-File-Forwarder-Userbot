# Python 3.10 এর স্লিম ভার্সন ব্যবহার করছি (সাইজ কম হবে)
FROM python:3.10-slim-buster

# কাজের ফোল্ডার সেট করা
WORKDIR /app

# সিস্টেম ডিপেন্ডেন্সি ইনস্টল করা (কিছু লাইব্রেরি যেমন uvloop বা tgcrypto এর জন্য এটি লাগতে পারে)
RUN apt-get update && apt-get install -y \
    gcc \
    python3-dev \
    && rm -rf /var/lib/apt/lists/*

# requirements. ফাইল কপি এবং ইনস্টল করা
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# বাকি সব ফাইল কপি করা
COPY . .

# পোর্ট এক্সপোজ করা (Render/Koyeb এর হেলথ চেকের জন্য)
EXPOSE 8080

# বট স্টার্ট করার কমান্ড
CMD ["python", "main.py"]
