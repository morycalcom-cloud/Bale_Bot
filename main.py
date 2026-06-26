from balethon import (
Client,
filters,
InlineKeyboardMarkup,
InlineKeyboardButton
)

menu = InlineKeyboardMarkup([
[
InlineKeyboardButton("📥 فایل‌ها", callback_data="files"),
InlineKeyboardButton("🖼 تصویر", callback_data="image")
],
[
InlineKeyboardButton("📝 متن", callback_data="text"),
InlineKeyboardButton("🔐 امنیت", callback_data="security")
],
[
InlineKeyboardButton("👤 پروفایل", callback_data="profile"),
InlineKeyboardButton("ℹ️ راهنما", callback_data="help")
]
])

@app.on_message(filters.command("start"))
async def start(client, message):
await message.reply(
"👋 به ربات خوش آمدید",
reply_markup=menu
)

@app.on_callback_query()
async def callbacks(client, callback):

```
if callback.data == "files":
    await callback.message.edit(
        "📥 ابزارهای فایل\n\n🚧 به زودی..."
    )

elif callback.data == "image":
    await callback.message.edit(
        "🖼 ابزارهای تصویر\n\n🚧 به زودی..."
    )

elif callback.data == "text":
    await callback.message.edit(
        "📝 ابزارهای متن\n\n🚧 به زودی..."
    )

elif callback.data == "security":
    await callback.message.edit(
        "🔐 ابزارهای امنیتی\n\n🚧 به زودی..."
    )

elif callback.data == "help":
    await callback.message.edit(
        "ℹ️ راهنمای ربات"
    )
```
