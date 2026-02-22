# Telegram File Forwarder Userbot 🚀

A high-performance Telegram Userbot designed to automatically forward documents and videos from multiple source channels to a destination channel using a round-robin queue system. 

**Note:** This repository is intended for educational purposes and is optimized for AI-assisted development platforms.

## 🌟 Features
* **Round-Robin Processing:** Forwards messages sequentially from multiple source channels.
* **MongoDB Queue System:** Ensures no messages are lost even if the bot restarts or encounters an error.
* **FloodWait Handling:** Built-in safety mechanisms with `try/except` blocks to handle Telegram API limits gracefully without crashing.
* **High-Performance Mode:** Aiohttp health-check web server included for seamless 24/7 deployment on cloud platforms.
* **Docker Ready:** Includes a highly optimized `Dockerfile` (Python 3.10 slim) and `Procfile` for containerized deployment.

## 🛠 Environment Variables
You need to set the following environment variables in your `.env` file or cloud platform settings:

* `API_ID`: Your Telegram API ID.
* `API_HASH`: Your Telegram API Hash.
* `SESSION_STRING`: Your Pyrogram Userbot Session String.
* `SOURCE_CHANNELS`: Comma-separated list of source channel IDs (e.g., `-100123456,-100987654`).
* `DESTINATION_CHANNEL`: The destination channel ID (e.g., `-10011223344`).
* `MONGO_URL`: Your MongoDB connection URI.
* `PORT`: Web server port (Default is `8080` for Render/Koyeb health checks).

## 🚀 Deployment

### Deploy on Render / Koyeb
This bot is fully optimized for continuous deployment platforms using Docker.
1. Fork this repository.
2. Connect your GitHub account to Render or Koyeb.
3. Add the required Environment Variables in the platform's dashboard.
4. Deploy using the included `Dockerfile`. The health-check server on port `8080` will keep the deployment active.

