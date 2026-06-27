from flask import Flask, request

from handlers.start import start
from handlers.messages import echo
from handlers.admin import admin

app = Flask(__name__)


@app.route("/")
def home():
    return "ONLINE"


@app.route("/webhook", methods=["POST"])
def webhook():

    update = request.json

    if not update:
        return "OK"

    if "message" not in update:
        return "OK"

    message = update["message"]

    text = message.get("text", "")

    if text == "/start":
        start(message)

    elif text == "/admin":
        admin(message)

    else:
        echo(message)

    return "OK"


if __name__ == "__main__":

    import os

    app.run(
        host="0.0.0.0",
        port=int(os.getenv("PORT", 8080))
    )
