import os
import requests
from flask import Flask, request, jsonify

app = Flask(__name__)

BOT_TOKEN = os.getenv("BOT_TOKEN")

if not BOT_TOKEN:
    raise Exception("BOT_TOKEN environment variable not found")

API = f"https://tapi.bale.ai/bot{BOT_TOKEN}"


def send_message(chat_id, text):
    requests.post(
        f"{API}/sendMessage",
        json={
            "chat_id": chat_id,
            "text": text
        },
        timeout=10
    )


@app.route("/")
def home():
    return "Bale Bot is Running!"


@app.route("/webhook", methods=["POST"])
def webhook():
    update = request.get_json()

    print(update)

    if not update:
        return jsonify({"ok": True})

    if "message" in update:

        message = update["message"]

        chat_id = message["chat"]["id"]

        text = message.get("text", "")

        if text == "/start":
            send_message(
                chat_id,
                "سلام 👋\nربات با موفقیت روی Railway اجرا شد."
            )

        elif text == "/ping":
            send_message(chat_id, "🏓 Pong!")

        else:
            send_message(
                chat_id,
                f"شما نوشتید:\n\n{text}"
            )

    return jsonify({"ok": True})


if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=int(os.environ.get("PORT", 8080))
    )
