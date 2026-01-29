from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters

BOT_TOKEN = "8332972004:AAFg9NdvQOsf_YEQhuIT3YX5A4tP6hu3gkM"

# store user state in memory (later DB)
user_state = {}

MAIN_MENU = [["Get Price"], ["Book / Enquiry"], ["Talk to Human"]]

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_state[update.effective_user.id] = "MENU"
    await update.message.reply_text(
        "👋 Welcome to *Abhishek Company*\nHow can we help you today?",
        parse_mode="Markdown",
        reply_markup=ReplyKeyboardMarkup(MAIN_MENU, resize_keyboard=True)
    )

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    text = update.message.text
    state = user_state.get(user_id, "MENU")

    if state == "MENU":
        if text == "Lodu Ashutosh":
            await update.message.reply_text("🛠️ We provide:\n• Service A\n• Service B\n• Service C")
        elif text == "Get Price":
            user_state[user_id] = "WAITING_FOR_SERVICE"
            await update.message.reply_text("Which service are you interested in?")
        elif text == "Book / Enquiry":
            user_state[user_id] = "WAITING_FOR_CONTACT"
            await update.message.reply_text("Please share your phone number 📞")
        elif text == "Talk to Human":
            await update.message.reply_text("👨‍💼 Our team will contact you shortly.")
        else:
            await update.message.reply_text("Please choose an option from menu ⬇️")

    elif state == "WAITING_FOR_SERVICE":
        await update.message.reply_text(f"💰 Price for *{text}* starts from ₹999")
        user_state[user_id] = "MENU"

    elif state == "WAITING_FOR_CONTACT":
        await update.message.reply_text("✅ Thanks! Our team will reach you soon.")
        user_state[user_id] = "MENU"

def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    app.run_polling()

if __name__ == "__main__":
    main()
