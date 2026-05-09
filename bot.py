import threading
import requests

from flask import Flask

from telegram import Update
from telegram.ext import (
    Application,
    CommandHandler,
    ContextTypes
)

API_KEY = "HDuHz2uHhO9CoQbpVtt858zZeSCoGHzMtJX0tDnB6Tc"
BASE_URL = "https://keyauth-enterprise.onrender.com/"
BOT_TOKEN = "8705317928:AAGtzb8Rm6HrbPQC3OC_K0qUAolm6KYkmw8"


# ---------------- FLASK WEB SERVER ---------------- #

web_app = Flask(__name__)


@web_app.route("/")
def home():
    return "Bot is running!"


def run_web():
    web_app.run(host="0.0.0.0", port=10000)


# ---------------- API FUNCTION ---------------- #

def reset_key(key):
    try:
        response = requests.post(
            BASE_URL + "api/reset",
            json={"key": key},
            headers={"X-API-Key": API_KEY},
            timeout=10
        )

        return response.json()

    except requests.RequestException as e:
        return {
            "success": False,
            "error": str(e)
        }


# ---------------- TELEGRAM COMMANDS ---------------- #

async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "✅ Bot Online\n\nUse:\n/reset KEY"
    )


async def reset_command(update: Update, context: ContextTypes.DEFAULT_TYPE):

    if not context.args:
        await update.message.reply_text(
            "Usage:\n/reset KEY"
        )
        return

    key = context.args[0]

    result = reset_key(key)

    if result.get("success"):
        await update.message.reply_text(
            f"✅ Key reset successfully:\n{key}"
        )
    else:
        await update.message.reply_text(
            f"❌ Error:\n{result.get('error')}"
        )


# ---------------- MAIN BOT ---------------- #

def run_bot():

    app = Application.builder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start_command))
    app.add_handler(CommandHandler("reset", reset_command))

    print("Bot running...")
    app.run_polling()


if __name__ == "__main__":

    threading.Thread(target=run_bot).start()

    run_web()
