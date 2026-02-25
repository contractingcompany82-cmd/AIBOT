import logging
import requests
import os
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
from dotenv import load_dotenv

load_dotenv()

TELEGRAM_BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
OPENROUTER_API_KEY = os.getenv('OPENROUTER_API_KEY')

print(f"🔑 Token loaded: {'Yes' if TELEGRAM_BOT_TOKEN else 'No'}")
print(f"🔑 Key loaded: {'Yes' if OPENROUTER_API_KEY else 'No'}")

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("👋 Hello! Test kar rahe hain...")

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_message = update.message.text
    print(f"📩 User: {user_message}")
    
    await context.bot.send_chat_action(chat_id=update.effective_chat.id, action='typing')
    
    try:
        print("🌐 Calling OpenRouter...")
        
        response = requests.post(
            url="https://openrouter.ai/api/v1/chat/completions",
            headers={
                "Authorization": f"Bearer {OPENROUTER_API_KEY}",
                "Content-Type": "application/json",
                "HTTP-Referer": "https://t.me/",
                "X-Title": "TelegramBot"
            },
            json={
                "model": "gryphe/mythomist-7b:free",  # Changed model
                "messages": [{"role": "user", "content": user_message}],
                "max_tokens": 500
            },
            timeout=30
        )
        
        print(f"📡 Status Code: {response.status_code}")
        print(f"📡 Response: {response.text[:200]}")
        
        if response.status_code == 200:
            data = response.json()
            ai_response = data['choices'][0]['message']['content']
            await update.message.reply_text(ai_response)
        else:
            await update.message.reply_text(f"⚠️ API Error: {response.status_code}\nCheck terminal for details")
            
    except Exception as e:
        print(f"❌ Exception: {str(e)}")
        await update.message.reply_text(f"❌ Error: {str(e)}")

def main():
    application = Application.builder().token(TELEGRAM_BOT_TOKEN).build()
    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    print("🤖 Bot running...")
    application.run_polling()

if __name__ == "__main__":
    main()
