import sqlite3
from datetime import datetime
from balethon import Client, filters, ReplyKeyboardMarkup

TOKEN = "BOT_TOKEN"

# ---------------- DATABASE ----------------

db = sqlite3.connect("users.db", check_same_thread=False)
cursor = db.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS users(
    id INTEGER PRIMARY KEY,
    first_name TEXT,
    username TEXT,
    join_date TEXT,
    requests INTEGER DEFAULT 0
)
""")
db.commit()


def add_user(user):
    cursor.execute(
        "INSERT OR IGNORE INTO users(id,first_name,username,join_date,requests) VALUES(?,?,?,?,0)",
        (
            user.id,
            user.first_name,
            user.username,
            datetime.now().strftime("%Y-%m-%d %H:%M")
        )
    )
    db.commit()


def add_request(user_id):
    cursor.execute(
        "UPDATE users SET requests=requests+1 WHERE id=?",
        (user_id,)
    )
    db.commit()


def get_user(user_id):
    cursor.execute(
        "SELECT * FROM users WHERE id=?",
        (user_id,)
    )
    return cursor.fetchone()


# ---------------- KEYBOARD ----------------

menu = ReplyKeyboardMarkup(
    keyboard=[
        ["📥 فایل‌ها", "🖼 ابزار تصویر"],
        ["📝 ابزار متن", "🔐 امنیت"],
        ["👤 پروفایل", "ℹ️ راهنما"]
    ],
    resize_keyboard=True
)

# ---------------- BOT ----------------

app = Client(
    "SimpleBot",
    bot_token=TOKEN
)


@app.on_message(filters.command("start"))
async def start(client, message):

    add_user(message.from_user)

    await message.reply(
        f"""سلام {message.from_user.first_name} 👋

به ربات ابزار خوش آمدی.

یکی از گزینه‌های زیر را انتخاب کن.""",
        reply_markup=menu
    )


@app.on_message(filters.text("👤 پروفایل"))
async def profile(client, message):

    add_request(message.from_user.id)

    user = get_user(message.from_user.id)

    await message.reply(
f"""
👤 پروفایل

🆔 {user[0]}

👤 نام:
{user[1]}

📛 یوزرنیم:
{user[2]}

📅 تاریخ عضویت:
{user[3]}

📊 تعداد درخواست‌ها:
{user[4]}
"""
)


@app.on_message(filters.text)
async def menu_handler(client, message):

    add_request(message.from_user.id)

    text = message.text

    if text == "📥 فایل‌ها":
        await message.reply(
            "📄 ابزارهای فایل\n\n"
            "🚧 به‌زودی:\n"
            "• عکس به PDF\n"
            "• PDF به عکس\n"
            "• ادغام PDF"
        )

    elif text == "🖼 ابزار تصویر":
        await message.reply(
            "🖼 ابزارهای تصویر\n\n"
            "🚧 به‌زودی:\n"
            "• QR Code\n"
            "• OCR\n"
            "• واترمارک"
        )

    elif text == "📝 ابزار متن":
        await message.reply(
            "📝 ابزار متن\n\n"
            "🚧 به‌زودی:\n"
            "• شمارش کلمات\n"
            "• قالب‌بندی JSON\n"
            "• Markdown"
        )

    elif text == "🔐 امنیت":
        await message.reply(
            "🔐 ابزار امنیت\n\n"
            "🚧 به‌زودی:\n"
            "• تولید رمز عبور\n"
            "• UUID\n"
            "• Hash"
        )

    elif text == "ℹ️ راهنما":
        await message.reply(
            "این نسخه اولیه ربات است.\n"
            "در نسخه‌های بعدی امکانات بیشتری اضافه خواهد شد."
        )


app.run()
