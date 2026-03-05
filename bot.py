import asyncio
import requests
from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters
from telegram.request import HTTPXRequest

BOT_TOKEN = "8337501018:AAEhBZm-2Y0hY68FPpsit-xgvwJBWkNpoAM"
API = "https://anishexploits.site/anish-exploits/api.php?key=demo-testing&num="

keyboard = ReplyKeyboardMarkup(
    [["📱 Phone Lookup"]],
    resize_keyboard=True
)

def fetch_api(num):
    try:
        r = requests.get(API + num, timeout=60)
        return r.json()
    except:
        return None

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Welcome to Number Info Bot 👋",
        reply_markup=keyboard
    )

async def handle(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text.strip()

    if text == "📱 Phone Lookup":
        await update.message.reply_text("📞 Send 10 digit mobile number:")
        return

    if text.isdigit() and len(text) == 10:
        await update.message.reply_text(f"🔍 Fetching info for {text} ...")

        await asyncio.sleep(1)

        data = await asyncio.to_thread(fetch_api, text)

        if not data or data.get("success") is not True:
            await update.message.reply_text("❌ No information found")
            return

        if "result" not in data or not data["result"]:
            await update.message.reply_text("❌ No records available")
            return

        d = data["result"][0]

        msg = f"""✅ Information Found
━━━━━━━━━━━━━━━━━━━━━━
🔢 Number: {text}
━━━━━━━━━━━━━━━━━━━━━━

👤 Name: {d.get("name","NA")}
👨‍🦳 Father: {d.get("father_name","NA")}
📱 Mobile: {d.get("mobile","NA")}
🆔 ID Number: {d.get("id_number","NA")}
🏠 Address: {d.get("address","NA")}
📍 Circle: {d.get("circle","NA")}

━━━━━━━━━━━━━━━━━━━━━━
👑 Developer: Anish Exploits
"""

        await update.message.reply_text(msg)
        return

    await update.message.reply_text(
        "⚠️ Invalid input\nUse button below ⬇️",
        reply_markup=keyboard
    )

def main():
    print("Anish Exploits Bot Started Successfully")

    request = HTTPXRequest(
        connect_timeout=120,
        read_timeout=120,
        write_timeout=120,
        pool_timeout=120
    )

    app = (
        ApplicationBuilder()
        .token(BOT_TOKEN)
        .request(request)
        .build()
    )

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle))

    app.run_polling(drop_pending_updates=True)

if __name__ == "__main__":
    main()
