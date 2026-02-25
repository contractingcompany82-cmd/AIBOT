import logging
import requests
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

# ========== YAHAN APNI NAYI KEYS DALEIN ==========
TELEGRAM_BOT_TOKEN = "8792076630:AAGKboaI54WThB5WtQchT1joQf3ylRveUEU"  # Naya token yahan dalein
OPENROUTER_API_KEY = "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"  # Nayi key yahan dalein
# ================================================

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "👋 *Namaste!* \n\n"
        "🤖 Main aapka AI assistant hoon.\n"
        "💬 Mujhe kuch bhi poochiye!\n\n"
        "_Powered by OpenRouter AI_",
        parse_mode='Markdown'
    )

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    user_message = update.message.text
    
    print(f"📩 {user.first_name}: {user_message}")
    
    # Typing indicator
    await context.bot.send_chat_action(
        chat_id=update.effective_chat.id, 
        action='typing'
    )
    
    try:
        # OpenRouter API call
        response = requests.post(
            url="https://openrouter.ai/api/v1/chat/completions",
            headers={
                "Authorization": f"Bearer {OPENROUTER_API_KEY}",
                "Content-Type": "application/json",
                "HTTP-Referer": "https://t.me/YourBot",
                "X-Title": "Telegram AI Bot"
            },
            json={
                "model": "mistralai/mistral-7b-instruct:free",
                "messages": [
                    {"role": "system", "content": "You are a helpful assistant. Reply in Hindi or English as per user's language."},
                    {"role": "user", "content": user_message}
                ],
                "temperature": 0.7,
                "max_tokens": 1000
            },
            timeout=60
        )
        
        print(f"📡 Status: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            ai_response = data['choices'][0]['message']['content']
            print(f"✅ Reply sent: {ai_response[:50]}...")
            
            # Split long messages
            if len(ai_response) > 4096:
                for i in range(0, len(ai_response), 4096):
                    await update.message.reply_text(ai_response[i:i+4096])
            else:
                await update.message.reply_text(ai_response)
        else:
            error_msg = f"❌ API Error: {response.status_code}\n{response.text[:200]}"
            print(error_msg)
            await update.message.reply_text("⚠️ Kuch problem aa gayi. Dobara try karein!")
            
    except requests.exceptions.Timeout:
        print("❌ Timeout error")
        await update.message.reply_text("⏰ Time lag raha hai. Thodi der baad try karein!")
        
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        await update.message.reply_text(f"❌ Error: {str(e)}")

async def error_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    logger.error(f"Update {update} caused error {context.error}")

def main():
    print("🚀 Bot start ho raha hai...")
    print("✅ OpenRouter AI connected")
    
    application = Application.builder().token(TELEGRAM_BOT_TOKEN).build()
    
    # Handlers
    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    application.add_error_handler(error_handler)
    
    print("🤖 Bot ready! Telegram mein test karein...")
    application.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == "__main__":
    main()
