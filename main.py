from flask import Flask, request
import requests

TOKEN = "BOT_TOKEN"
BASE_URL = f"https://tapi.bale.ai/bot{TOKEN}"

app = Flask(__name__)


def send_message(chat_id, text):
    url = BASE_URL + "/sendMessage"
    requests.post(url, json={
        "chat_id": chat_id,
        "text": text
    })


@app.route("/", methods=["GET"])
def home():
    return "Bot is running"


@app.route("/webhook", methods=["POST"])
def webhook():

    data = request.json

    if "message" not in data:
        return "ok"

    message = data["message"]
    chat_id = message["chat"]["id"]
    text = message.get("text", "")

    if text == "/start":
        send_message(chat_id, "👋 سلام! ربات فعال شد")

    elif text == "📥 فایل‌ها":
        send_message(chat_id, "🚧 بخش فایل‌ها")

    elif text == "🖼 تصویر":
        send_message(chat_id, "🚧 بخش تصویر")

    else:
        send_message(chat_id, "از منو استفاده کن 👇")

    return "ok"


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
