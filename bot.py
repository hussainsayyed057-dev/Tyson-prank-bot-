import os
import logging
import threading
from flask import Flask
from telegram import Update, ReplyKeyboardMarkup, ReplyKeyboardRemove
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler, MessageHandler, filters

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
PORT = int(os.getenv("PORT", 8080))

# Flask app for Render health check
app_flask = Flask(__name__)

@app_flask.route('/')
def index():
    return "Tyson Shadow Bot is active."

def run_flask():
    app_flask.run(host="0.0.0.0", port=PORT)

# Telegram bot states and handlers
user_states = {}

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    user_states[user_id] = "awaiting_gender"
    
    welcome_text = (
        "Welcome to Tyson Shadow Bot.\n\n"
        "Initializing secure node...\n"
        "Target connection established.\n\n"
        "Please select your gender to proceed with profile verification:"
    )
    
    reply_keyboard = [["Male", "Female"]]
    markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True, resize_keyboard=True)
    
    await update.message.reply_text(welcome_text, reply_markup=markup)

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    text = update.message.text
    
    state = user_states.get(user_id)
    
    if state == "awaiting_gender":
        if text.lower() in ["male", "female"]:
            user_states[user_id] = "completed"
            prank_response = (
                f"Nice ({text} profile recorded).\n\n"
                "Ab tumhara all data dark web per leak ho chuka h and many gangster funding you for working."
            )
            await update.message.reply_text(prank_response, reply_markup=ReplyKeyboardRemove())
        else:
            await update.message.reply_text("Please select either 'Male' or 'Female' using the keyboard.")
    else:
        await update.message.reply_text("Type /start to restart the session.")

def main():
    # Start Flask in a separate thread so Render health checks pass
    t = threading.Thread(target=run_flask)
    t.daemon = True
    t.start()

    # Build and run Telegram bot polling
    application = ApplicationBuilder().token(TOKEN).build()
    
    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), handle_message))
    
    print("Bot polling started...")
    application.run_polling()

if __name__ == "__main__":
    main()
