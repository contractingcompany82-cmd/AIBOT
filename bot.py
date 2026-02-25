import logging
import requests
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

# ========== APNE DETAILS YAHAN DALEIN ==========
TELEGRAM_BOT_TOKEN = "8792076630:AAGKboaI54WThB5WtQchT1joQf3ylRveUEU"
OPENROUTER_API_KEY = "import logging
import requests
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

# ========== APNE DETAILS YAHAN DALEIN ==========
TELEGRAM_BOT_TOKEN = "8792076630:AAGKboaI54WThB5WtQchT1joQf3ylRveUEU"
OPENROUTER_API_KEY = "import logging
import requests
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

# ========== APNE DETAILS YAHAN DALEIN ==========
TELEGRAM_BOT_TOKEN = "8792076630:AAGKboaI54WThB5WtQchT1joQf3ylRveUEU"
OPENROUTER_API_KEY = "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"  # Ismein 'sk-or-v1-' se start hoga
# ===============================================

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("👋 Hello! Main OpenRouter AI hoon. Poochiye kuch bhi!")

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_message = update.message.text
    
    await context.bot.send_chat_action(chat_id=update.effective_chat.id, action='typing')
    
    try:
        # OpenRouter API call
        response = requests.post(
            url="https://openrouter.ai/api/v1/chat/completions",
            headers={
                "Authorization": f"Bearer {OPENROUTER_API_KEY}",
                "Content-Type": "application/json"
            },
            json={
                "model": "mistralai/mistral-7b-instruct:free",  # FREE model
                "messages": [{"role": "user", "content": user_message}]
            }
        )
        
        data = response.json()
        ai_response = data['choices'][0]['message']['content']
        
        await update.message.reply_text(ai_response)
        
    except Exception as e:
        await update.message.reply_text(f"❌ Error: {str(e)}")

def main():
    application = Application.builder().token(TELEGRAM_BOT_TOKEN).build()
    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    print("🤖 Bot chal raha hai...")
    application.run_polling()

if __name__ == "__main__":
    main()"  # Ismein 'sk-or-v1-' se start hoga
# ===============================================

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("👋 Hello! Main OpenRouter AI hoon. Poochiye kuch bhi!")

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_message = update.message.text
    
    await context.bot.send_chat_action(chat_id=update.effective_chat.id, action='typing')
    
    try:
        # OpenRouter API call
        response = requests.post(
            url="https://openrouter.ai/api/v1/chat/completions",
            headers={
                "Authorization": f"Bearer {OPENROUTER_API_KEY}",
                "Content-Type": "application/json"
            },
            json={
                "model": "mistralai/mistral-7b-instruct:free",  # FREE model
                "messages": [{"role": "user", "content": user_message}]
            }
        )
        
        data = response.json()
        ai_response = data['choices'][0]['message']['content']
        
        await update.message.reply_text(ai_response)
        
    except Exception as e:
        await update.message.reply_text(f"❌ Error: {str(e)}")

def main():
    application = Application.builder().token(TELEGRAM_BOT_TOKEN).build()
    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    print("🤖 Bot chal raha hai...")
    application.run_polling()

if __name__ == "__main__":
    main()"  # Ismein 'sk-or-v1-' se start hoga
# ===============================================

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("👋 Hello! Main OpenRouter AI hoon. Poochiye kuch bhi!")

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_message = update.message.text
    
    await context.bot.send_chat_action(chat_id=update.effective_chat.id, action='typing')
    
    try:
        # OpenRouter API call
        response = requests.post(
            url="https://openrouter.ai/api/v1/chat/completions",
            headers={
                "Authorization": f"Bearer {OPENROUTER_API_KEY}",
                "Content-Type": "application/json"
            },
            json={
                "model": "mistralai/mistral-7b-instruct:free",  # FREE model
                "messages": [{"role": "user", "content": user_message}]
            }
        )
        
        data = response.json()
        ai_response = data['choices'][0]['message']['content']
        
        await update.message.reply_text(ai_response)
        
    except Exception as e:
        await update.message.reply_text(f"❌ Error: {str(e)}")

def main():
    application = Application.builder().token(TELEGRAM_BOT_TOKEN).build()
    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    print("🤖 Bot chal raha hai...")
    application.run_polling()

if __name__ == "__main__":
    main()
