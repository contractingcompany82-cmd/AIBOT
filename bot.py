import os
import requests
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
API_KEY = os.getenv('OPENROUTER_API_KEY')

print(f"Token: {'Found' if TOKEN else 'NOT FOUND'}")
print(f"API Key: {'Found' if API_KEY else 'NOT FOUND'}")

if not TOKEN or not API_KEY:
    print("ERROR: Check .env file!")
    exit(1)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("👋 Bot working! Send me any message.")

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    chat_id = update.effective_chat.id
    
    print(f"Received: {text}")
    
    await context.bot.send_chat_action(chat_id=chat_id, action='typing')
    
    try:
        response = requests.post(
            "https://openrouter.ai/api/v1/chat/completions",
            headers={
                "Authorization": f"Bearer {API_KEY}",
                "Content-Type": "application/json"
            },
            json={
                "model": "gryphe/mythomist-7b:free",
                "messages": [{"role": "user", "content": text}]
            },
            timeout=30
        )
        
        if response.status_code == 200:
            reply = response.json()['choices'][0]['message']['content']
            await update.message.reply_text(reply)
        else:
            await update.message.reply_text(f"Error: {response.status_code}")
            
    except Exception as e:
        print(f"Error: {e}")
        await update.message.reply_text("Error occurred!")

def main():
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.command, handle_message))
    
    print("Bot started!")
    app.run_polling()

if __name__ == "__main__":
    main()
