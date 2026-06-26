import requests
import time

TOKEN = "BOT_TOKEN"

BASE_URL = f"https://tapi.bale.ai/bot{TOKEN}"


# ---------------- SEND MESSAGE ----------------

def send_message(chat_id, text):
    url = BASE_URL + "/sendMessage"
    data = {
        "chat_id": chat_id,
        "text": text
    }
    requests.post(url, json=data)


# ---------------- GET UPDATES ----------------

last_update_id = 0


def get_updates():
    global last_update_id

    url = BASE_URL + "/getUpdates"
    params = {"offset": last_update_id + 1}

    res = requests.get(url, params=params)
    data = res.json()

    if "result" in data:
        return data["result"]
    return []


# ---------------- BOT LOOP ----------------

print("Bot is running...")

while True:

    updates = get_updates()

    for update in updates:

        last_update_id = update["update_id"]

        if "message" not in update:
            continue

        message = update["message"]
        chat_id = message["chat"]["id"]
        text = message.get("text", "")

        # /start
        if text == "/start":
            send_message(
                chat_id,
                "👋 سلام!\nبه ربات ابزار بله خوش آمدی."
            )

        # menu
        elif text == "📥 فایل‌ها":
            send_message(chat_id, "🚧 بخش فایل‌ها به زودی...")

        elif text == "🖼 تصویر":
            send_message(chat_id, "🚧 بخش تصویر به زودی...")

        elif text == "📝 متن":
            send_message(chat_id, "🚧 بخش متن به زودی...")

        elif text == "🔐 امنیت":
            send_message(chat_id, "🚧 بخش امنیت به زودی...")

        elif text == "👤 پروفایل":
            send_message(chat_id, "👤 پروفایل شما در نسخه بعد اضافه می‌شود")

        else:
            send_message(chat_id, "از دستورات ربات استفاده کن 👇")

    time.sleep(1)
