from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
import psutil
import time
import asyncio

from config import *
from extractor import extract_video

app = Client("diskwala-bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

START_IMG = "https://d.uguu.se/zarjAhvx.jpg"
START_TIME = time.time()


# 🚀 START
@app.on_message(filters.command("start"))
async def start(client, message):
    text = """
<b>🚀 DiskWala Ultra Bot</b>

⚡ Fast • Secure • Multi Downloader

🎬 Supported:
• YouTube • Instagram • Facebook  
• TeraBox • DiskWala  

📌 Send link to start
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


# 📘 HELP
@app.on_callback_query(filters.regex("^help$"))
async def help_callback(client, query):
    await query.answer()

    text = "📘 Send link → Choose quality → Download"

    await query.message.edit_text(
        text,
        reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton("🔙 Back", callback_data="back")]
        ])
    )


# 🔙 BACK
@app.on_callback_query(filters.regex("^back$"))
async def back(client, query):
    await query.answer()
    await query.message.delete()
    await start(client, query.message)


# 📊 STATS
@app.on_callback_query(filters.regex("^stats$"))
async def stats(client, query):
    await query.answer()

    uptime = int(time.time() - START_TIME)
    ram = psutil.virtual_memory().percent
    cpu = psutil.cpu_percent()

    text = f"""
📊 Bot Stats

⏱ Uptime: {uptime}s  
🧠 CPU: {cpu}%  
💾 RAM: {ram}%
"""

    await query.message.edit_text(
        text,
        reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton("🔙 Back", callback_data="back")]
        ])
    )


# 🔗 LINK HANDLER
@app.on_message(filters.text & ~filters.command)
async def handler(client, message):
    url = message.text.strip()

    msg = await message.reply("⏳ Processing...")

    try:
        loop = asyncio.get_event_loop()
        data = await loop.run_in_executor(None, extract_video, url)
    except Exception as e:
        await msg.edit(f"❌ Error:\n{str(e)}")
        return

    if not data.get("formats"):
        await msg.edit("❌ No formats found")
        return

    buttons = []

    for i, f in enumerate(data["formats"][:5]):
        buttons.append([
            InlineKeyboardButton(
                f"📥 {f.get('quality','File')}",
                callback_data=f"dl|{i}"
            )
        ])

    # store formats temporarily
    app.temp_data = getattr(app, "temp_data", {})
    app.temp_data[message.chat.id] = data["formats"]

    buttons.append([
        InlineKeyboardButton("🌐 Web Download", url=f"{BASE_URL}/generate?url={url}")
    ])

    await msg.edit(
        "🎬 Select Quality:",
        reply_markup=InlineKeyboardMarkup(buttons)
    )


# 📥 DOWNLOAD
@app.on_callback_query(filters.regex("^dl"))
async def dl(client, query):
    await query.answer()

    try:
        _, index = query.data.split("|")
        index = int(index)

        formats = app.temp_data.get(query.message.chat.id)
        file = formats[index]

        url = file["url"]
        size = file.get("size", 0)

    except Exception as e:
        await query.message.reply("❌ Invalid request")
        return

    await query.message.edit("⏳ Processing file...")

    if size and size < MAX_UPLOAD_SIZE:
        try:
            await client.send_video(
                chat_id=query.message.chat.id,
                video=url,
                caption="✅ Uploaded"
            )
        except:
            await query.message.reply(
                "❌ Upload failed",
                reply_markup=InlineKeyboardMarkup([
                    [InlineKeyboardButton("📥 Download", url=url)]
                ])
            )
    else:
        await query.message.reply(
            "📥 File too large",
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("Download", url=url)]
            ])
        )

    await query.message.delete()


print("🚀 Bot running...")
app.run()
