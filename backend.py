import asyncio, datetime, config
from telegram import Bot, Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
from get_time import parse_data

user_state = {}  

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_state[update.effective_user.id] = "awaiting_city"
    await update.message.reply_text("Send me your city name (e.g., Toronto):")

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    text = update.message.text

    if user_id not in user_state:
        await update.message.reply_text("Please type /start to begin setup.")
        return

    state = user_state[user_id]

    if state == "awaiting_city":
        config.city = text
        user_state[user_id] = "awaiting_channel"
        await update.message.reply_text(f"City set to {config.city}. Now send me your channel ID (e.g., @my_channel):")
    elif state == "awaiting_channel":
        if not text.startswith("@"):
            await update.message.reply_text("Channel ID must start with '@'. Try again:")
            return
        config.channel_id = text
        user_state[user_id] = "done"
        await update.message.reply_text(
            "Done! ✅\n"
            "The bot will post daily Adhan times at 12:00 AM.\n\n"
            "**Important:** Make sure the bot is an *admin* in the channel or it won't be able to send messages."
        )
        message = parse_data()
        await context.bot.send_message(chat_id=config.channel_id, text=message)
        asyncio.create_task(send_daily_adhan(context.bot))
    else:
        await update.message.reply_text("You're already set up.")

async def send_daily_adhan(bot: Bot):
    while True:
        now = datetime.datetime.now()
        if now.hour == 0 and now.minute == 0:
            message = parse_data()
            await bot.send_message(chat_id=config.channel_id, text=message)
            await asyncio.sleep(60)
        await asyncio.sleep(30)

def main():
    app = Application.builder().token("YOUR_TOKEN_HERE").build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    app.run_polling()

if __name__ == "__main__":
    main()

