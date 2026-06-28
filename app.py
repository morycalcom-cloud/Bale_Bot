import os
import requests
from flask import Flask, request
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv("BALE_TOKEN")

app = Flask(__name__)

API = f"https://tapi.bale.ai/bot{TOKEN}"


def send_message(chat_id, text):
    requests.post(
        API + "/sendMessage",
        json={
            "chat_id": chat_id,
            "text": text
        }
    )


@app.route("/")
def home():
    return "Bale AI Bot Online"


@app.route("/webhook", methods=["POST"])
def webhook():

    update = request.get_json()

    print(update)

    if "message" not in update:
        return "ok"

    message = update["message"]

    chat_id = message["chat"]["id"]

    text = message.get("text", "")

    if text == "/start":
        send_message(
            chat_id,
            """سلام 👋

به ربات هوش مصنوعی خوش آمدید.

دستورات:

/help
/image
"""
        )

    elif text == "/help":
        send_message(
            chat_id,
            "پیام خود را ارسال کنید تا پاسخ بدهم."
        )

    else:
        send_message(
            chat_id,
            f"شما نوشتید:\n{text}"
        )

    return "ok"


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
