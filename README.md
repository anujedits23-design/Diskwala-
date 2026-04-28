🚀 DiskWala Ultra - Multi Platform Downloader Bot

A powerful Telegram Bot + Web API that extracts and delivers downloadable media from multiple platforms including:

- 🎬 YouTube, Instagram, Facebook (via yt-dlp)
- 📦 TeraBox (API-based extraction)
- 🔗 DiskWala links (bypass + fallback support)

---

✨ Features

- ⚡ Fast Extraction Engine
- 🎬 Multi-quality selection (144p – 4K)
- 📥 Direct Download Link (No Ads)
- 📤 Telegram Upload (Auto for small files)
- 🔐 Secure Expiring Links (48h)
- 🌐 Web-based Download Page
- 🧠 Smart Fallback System
- 🔄 DiskWala Link Bypass (Best Effort)

---

🏗️ Architecture

User → Telegram Bot → Extractor Engine → Token Generator → Web Server → Download

---

📁 Project Structure

diskwala-ultra/
│
├── bot.py              # Telegram bot logic
├── web.py              # Flask API server
├── extractor.py        # Multi-platform extractor
├── utils.py            # Token & security utils
├── config.py           # Config variables
├── requirements.txt    # Dependencies
├── Procfile            # Render deployment
├── runtime.txt         # Python version
└── templates/
    └── download.html   # Web UI

---

⚙️ Installation

1. Clone Repository

git clone https://github.com/yourusername/diskwala-ultra.git
cd diskwala-ultra

2. Install Dependencies

pip install -r requirements.txt

---

🔐 Configuration

Edit "config.py":

API_ID = 123456
API_HASH = "your_api_hash"
BOT_TOKEN = "your_bot_token"

BASE_URL = "https://your-domain.com"

LINK_EXPIRY = 172800  # 48 hours
MAX_UPLOAD_SIZE = 100 * 1024 * 1024

---

▶️ Running the Project

Start Web Server

python web.py

Start Telegram Bot

python bot.py

---

🚀 Deployment (Render)

Step 1: Push to GitHub

Step 2: Create Web Service on Render

- Build Command

pip install -r requirements.txt

- Start Command

gunicorn web:app

---

🤖 Bot Deployment

Run bot separately (Render background worker / VPS):

python bot.py

---

📦 Supported Platforms

Platform| Status
YouTube| ✅ Full
Instagram| ✅ Full
Facebook| ✅ Full
Twitter/X| ✅ Full
TeraBox| ✅ Partial (API-based)
DiskWala Links| ⚠️ Best-effort

---

⚠️ Limitations

- ❌ Private / login-required content
- ❌ DRM-protected platforms (Netflix, Prime, etc.)
- ⚠️ TeraBox reliability depends on external API
- ⚠️ DiskWala links may not always be fully extractable

---

🧠 Smart Logic

- 📦 Small files → Auto upload to Telegram
- 📥 Large files → Download link provided
- 🔄 Extraction fallback system implemented

---

🔒 Security

- Token-based download system
- Expiring links (48 hours)
- No third-party redirect or ads

---

💡 Future Improvements

- 🔐 Login session support (Instagram private)
- 🌍 Proxy rotation system
- 📦 Folder download (TeraBox)
- ⚡ CDN-based fast delivery
- 🧠 AI-based smart extractor

---

📜 License

This project is for educational purposes only.
Use responsibly and respect platform terms of service.

---

👨‍💻 Author

Developed by Anuj Kumar 

---

⭐ Support

If you like this project:

- ⭐ Star the repo
- 🍴 Fork it
- 🧠 Contribute improvements

---

🔥 Build your own DiskWala-level downloader today!
