import requests
from telegram import Update
from telegram.ext import (
    Application,
    CommandHandler,
    ContextTypes
)

API_KEY = "HDuHz2uHhO9CoQbpVtt858zZeSCoGHzMtJX0tDnB6Tc"
BASE_URL = "https://keyauth-enterprise.onrender.com/"


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


BOT_TOKEN = "8705317928:AAGtzb8Rm6HrbPQC3OC_K0qUAolm6KYkmw8"

app = Application.builder().token(BOT_TOKEN).build()

app.add_handler(CommandHandler("start", start_command))
app.add_handler(CommandHandler("reset", reset_command))

print("Bot running...")
app.run_polling()
