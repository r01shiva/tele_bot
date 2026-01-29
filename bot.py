import json
from telegram import Update, ReplyKeyboardMarkup
from telegram import ReplyKeyboardRemove
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    ContextTypes,
    filters
)

BOT_TOKEN = "8332972004:AAFg9NdvQOsf_YEQhuIT3YX5A4tP6hu3gkM"

# user state store (replace with DB later)
user_state = {}
user_data = {}

def load_menu():
    with open("menu.json", "r", encoding="utf-8") as f:
        return json.load(f)["main_menu"]

# ---------- START ----------
async def start(update, context):
    user_id = update.effective_user.id
    user_state[user_id] = "MENU"
    user_data[user_id] = {}

    # 1️⃣ REMOVE old keyboard
    await update.message.reply_text(
        "🔄 Updating menu...",
        reply_markup=ReplyKeyboardRemove()
    )

    # 2️⃣ SEND new keyboard
    await update.message.reply_text(
        "🚚 *Welcome to ABC Logistics*\nHow can we help you?",
        parse_mode="Markdown",
        reply_markup=ReplyKeyboardMarkup(load_menu(), resize_keyboard=True)
    )

# ---------- MESSAGE HANDLER ----------
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    text = update.message.text.strip()
    state = user_state.get(user_id, "MENU")

    # -------- MENU --------
    if state == "MENU":
        if text == "📦 Track Shipment":
            user_state[user_id] = "TRACK"
            await update.message.reply_text("📦 Please enter your *Tracking ID*:", parse_mode="Markdown")

        elif text == "💰 Get Rate":
            user_state[user_id] = "RATE_FROM"
            await update.message.reply_text("📍 Enter pickup city:")

        elif text == "🚚 Book Pickup":
            user_state[user_id] = "PICKUP_NAME"
            await update.message.reply_text("👤 Enter your full name:")

        elif text == "👨‍💼 Talk to Human":
            await update.message.reply_text(
                "📞 Our support team will contact you shortly.\nOr call: +91-XXXXXXXXXX"
            )

        else:
            await update.message.reply_text("Please select an option from menu ⬇️")

    # -------- TRACK SHIPMENT --------
    elif state == "TRACK":
        tracking_id = text
        # Dummy status (replace with real API)
        await update.message.reply_text(
            f"✅ *Shipment Status*\n\n"
            f"Tracking ID: `{tracking_id}`\n"
            f"Status: In Transit 🚛\n"
            f"Expected Delivery: 2 days",
            parse_mode="Markdown",
            reply_markup=ReplyKeyboardMarkup(load_menu(), resize_keyboard=True)
        )
        user_state[user_id] = "MENU"

    # -------- RATE CALCULATION --------
    elif state == "RATE_FROM":
        user_data[user_id]["from"] = text
        user_state[user_id] = "RATE_TO"
        await update.message.reply_text("📍 Enter destination city:")

    elif state == "RATE_TO":
        user_data[user_id]["to"] = text
        user_state[user_id] = "RATE_WEIGHT"
        await update.message.reply_text("⚖️ Enter weight (in kg):")

    elif state == "RATE_WEIGHT":
        weight = text
        from_city = user_data[user_id]["from"]
        to_city = user_data[user_id]["to"]

        await update.message.reply_text(
            f"💰 *Estimated Shipping Cost*\n\n"
            f"From: {from_city}\n"
            f"To: {to_city}\n"
            f"Weight: {weight} kg\n\n"
            f"Price: ₹{int(float(weight) * 50)} approx",
            parse_mode="Markdown",
            reply_markup=ReplyKeyboardMarkup(load_menu(), resize_keyboard=True)
        )
        user_state[user_id] = "MENU"

    # -------- PICKUP BOOKING --------
    elif state == "PICKUP_NAME":
        user_data[user_id]["name"] = text
        user_state[user_id] = "PICKUP_PHONE"
        await update.message.reply_text("📞 Enter your phone number:")

    elif state == "PICKUP_PHONE":
        user_data[user_id]["phone"] = text
        user_state[user_id] = "PICKUP_ADDRESS"
        await update.message.reply_text("🏠 Enter pickup address:")

    elif state == "PICKUP_ADDRESS":
        user_data[user_id]["address"] = text

        await update.message.reply_text(
            "✅ *Pickup Request Received*\n\n"
            "Our team will contact you shortly to confirm.\nThank you for choosing ABC Logistics 🚚",
            parse_mode="Markdown",
            reply_markup=ReplyKeyboardMarkup(load_menu(), resize_keyboard=True)
        )

        # Here you can notify admin / save to DB
        user_state[user_id] = "MENU"

# ---------- MAIN ----------
def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    app.run_polling()

if __name__ == "__main__":
    main()
