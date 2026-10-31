import os
import logging
from telegram import Update, ReplyKeyboardMarkup, ReplyKeyboardRemove
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler, MessageHandler, filters

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

TOKEN = os.getenv("TELEGRAM_BOT_TOKEN", "YOUR_BOT_TOKEN_HERE")

# State dictionary to track user progress in the prank flow
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
    app = ApplicationBuilder().token(TOKEN).build()
    
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), handle_message))
    
    print("Bot is running...")
    app.run_polling()

if __name__ == "__main__":
    main()
