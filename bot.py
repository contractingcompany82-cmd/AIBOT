import logging
import requests
import os
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
from dotenv import load_dotenv

load_dotenv()

TELEGRAM_BOT_TOKEN = os.getenv('8792076630:AAGKboaI54WThB5WtQchT1joQf3ylRveUEU')
OPENROUTER_API_KEY = os.getenv('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')

# Check karein keys load hui ya nahi
print("=" * 50)
print(f"🔑 Token loaded: {'YES ✅' if TELEGRAM_BOT_TOKEN else 'NO ❌'}")
print(f"🔑 Key loaded: {'YES ✅' if OPENROUTER_API_KEY else 'NO ❌'}")
if TELEGRAM_BOT_TOKEN:
    print(f"📝 Token: {TELEGRAM_BOT_TOKEN[:20]}...")
if OPENROUTER_API_KEY:
    print(f"📝 Key: {OPENROUTER_API_KEY[:20]}...")
print("=" * 50)

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print(f"✅ /start received from {update.effective_user.first_name}")
    await update.message.reply_text("👋 Bot working! Send me any message.")

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    user_message = update.message.text
    
    print(f"\n📩 {'='*40}")
    print(f"👤 User: {user.first_name}")
    print(f"💬 Message: {user_message}")
    print(f"⏳ Sending typing action...")
    
    try:
        await context.bot.send_chat_action(chat_id=update.effective_chat.id, action='typing')
        print("✅ Typing action sent")
        
        print("🌐 Calling OpenRouter API...")
        print(f"🔗 URL: https://openrouter.ai/api/v1/chat/completions")
        print(f"🔐 Auth Header: Bearer {OPENROUTER_API_KEY[:15]}...")
        
        response = requests.post(
            url="https://openrouter.ai/api/v1/chat/completions",
            headers={
                "Authorization": f"Bearer {OPENROUTER_API_KEY}",
                "Content-Type": "application/json",
                "HTTP-Referer": "https://t.me/",
                "X-Title": "TelegramBot"
            },
            json={
                "model": "gryphe/mythomist-7b:free",
                "messages": [{"role": "user", "content": user_message}],
                "max_tokens": 500
            },
            timeout=30
        )
        
        print(f"📡 Response received!")
        print(f"📡 Status Code: {response.status_code}")
        print(f"📡 Headers: {dict(response.headers)}")
        
        if response.status_code == 200:
            try:
                data = response.json()
                print(f"📦 JSON parsed successfully")
                print(f"📦 Keys in response: {list(data.keys())}")
                
                if 'choices' in data and len(data['choices']) > 0:
                    ai_response = data['choices'][0]['message']['content']
                    print(f"🤖 AI Response: {ai_response[:100]}...")
                    
                    print("📤 Sending reply to Telegram...")
                    await update.message.reply_text(ai_response)
                    print("✅ Reply sent successfully!")
                else:
                    print(f"❌ No choices in response: {data}")
                    await update.message.reply_text("⚠️ AI ne kuch nahi kaha!")
                    
            except Exception as e:
                print(f"❌ JSON parse error: {e}")
                print(f"❌ Raw response: {response.text[:500]}")
                await update.message.reply_text(f"⚠️ Data parse error: {e}")
        else:
            print(f"❌ API Error: {response.status_code}")
            print(f"❌ Response: {response.text[:500]}")
            await update.message.reply_text(f"⚠️ API Error: {response.status_code}")
            
    except requests.exceptions.Timeout:
        print("❌ Request timeout!")
        await update.message.reply_text("⏰ Timeout! Internet slow hai?")
        
    except requests.exceptions.ConnectionError:
        print("❌ Connection error!")
        await update.message.reply_text("🔌 Internet connection check karein!")
        
    except Exception as e:
        print(f"❌ Unexpected error: {type(e).__name__}: {e}")
        await update.message.reply_text(f"❌ Error: {str(e)}")

def main():
    print("\n🚀 Starting bot...")
    print("🤖 Bot is running! Send message in Telegram.\n")
    
    application = Application.builder().token(TELEGRAM_BOT_TOKEN).build()
    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    
    application.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == "__main__":
    main()
