from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
import asyncio

from config import *
from extractor import extract_video

app = Client("bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)


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
