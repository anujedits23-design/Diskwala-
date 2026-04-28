from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
import psutil, time
import asyncio

from config import *
from extractor import extract_video

app = Client("bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

@app.on_message(filters.command("start"))
async def start(client, message):
    text = f"""
<b>🚀 DiskWala Ultra Bot</b>

<blockquote>
⚡ Fast • Secure • Multi-Platform Downloader
</blockquote>

🎬 <b>Supported:</b>
• YouTube • Instagram • Facebook  
• TeraBox • DiskWala Links  

✨ <b>Features:</b>
• 🎬 Quality Selection  
• 📤 Telegram Upload  
• 📥 Direct Download  
• 🔐 Secure Links  

📌 Send any link to start
"""

    buttons = InlineKeyboardMarkup([
        [
            InlineKeyboardButton("📘 Help", callback_data="help"),
            InlineKeyboardButton("📊 Stats", callback_data="stats")
        ],
        [
            InlineKeyboardButton("🌐 Web", url=BASE_URL)
        ]
    ])

    await message.reply_photo(
        photo=START_IMG,
        caption=text,
        reply_markup=buttons,
        parse_mode="html"
    )

@app.on_callback_query(filters.regex("help"))
async def help_callback(client, query):
    text = """
<b>📘 Help & Usage</b>

Send a link → Choose quality → Download

━━━━━━━━━━━━━━━

⚠️ Limitations:
• Private links ❌  
• DRM content ❌  

━━━━━━━━━━━━━━━

Supported:
• YouTube / Insta / FB  
• TeraBox  
• DiskWala  
"""

    buttons = InlineKeyboardMarkup([
        [InlineKeyboardButton("🔙 Back", callback_data="back")]
    ])

    await query.message.edit_caption(text, reply_markup=buttons, parse_mode="html")

@app.on_callback_query(filters.regex("back"))
async def back(client, query):
    await start(client, query.message)

@app.on_callback_query(filters.regex("stats"))
async def stats(client, query):
    uptime = int(time.time() - START_TIME)
    ram = psutil.virtual_memory().percent
    cpu = psutil.cpu_percent()

    text = f"""
<b>📊 Bot Stats</b>

⏱ Uptime: {uptime}s  
🧠 CPU: {cpu}%  
💾 RAM: {ram}%  

✅ Running Smooth
"""

    buttons = InlineKeyboardMarkup([
        [InlineKeyboardButton("🔙 Back", callback_data="back")]
    ])

    await query.message.edit_caption(text, reply_markup=buttons, parse_mode="html")

@app.on_message(filters.text & ~filters.command)
async def handler(client, message):
    url = message.text.strip()

    msg = await message.reply("⏳ Processing...")

    await asyncio.sleep(2)

    data = extract_video(url)

    buttons = []

    for f in data["formats"]:
        buttons.append([
            InlineKeyboardButton(
                f"📥 {f['quality']}",
                callback_data=f"dl|{f['url']}|{f['size']}"
            )
        ])

    buttons.append([
        InlineKeyboardButton("🌐 Web Download", url=f"{BASE_URL}/generate?url={url}")
    ])

    await msg.edit("🎬 Select Quality:", reply_markup=InlineKeyboardMarkup(buttons))


@app.on_callback_query(filters.regex("^dl"))
async def dl(client, query):
    _, url, size = query.data.split("|")
    size = int(size)

    if size and size < MAX_UPLOAD_SIZE:
        try:
            await client.send_video(query.message.chat.id, url)
        except:
            await query.message.reply("Use web download")
    else:
        await query.message.reply(
            "📥 Large file",
            reply_markup=InlineKeyboardMarkup(
                [[InlineKeyboardButton("Download", url=url)]]
            )
        )

    await query.message.delete()


app.run()
