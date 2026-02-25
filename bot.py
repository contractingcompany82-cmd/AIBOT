import os
import requests
import asyncio
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Get tokens
TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
API_KEY = os.getenv('OPENROUTER_API_KEY')

print(f"🔑 Token: {'✅ Found' if TOKEN else '❌ Not Found'}")
print(f"🔑 API Key: {'✅ Found' if API_KEY else '❌ Not Found'}")

if not TOKEN or not API_KEY:
    print("❌ ERROR: Missing environment variables!")
    print("Make sure .env file exists with correct values")
    exit(1)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /start command"""
    await update.message.reply_text(
        "👋 *Hello!* Bot is working perfectly!\n\n"
        "Send me any message and I'll reply using AI.",
        parse_mode='Markdown'
    )

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle user messages"""
    user_text = update.message.text
    user_name = update.effective_user.first_name
    
    print(f"\n📩 {user_name}: {user_text}")
    
    # Show typing indicator
    await context.bot.send_chat_action(
        chat_id=update.effective_chat.id, 
        action='typing'
    )
    
    try:
        # Call OpenRouter API
        print("🤖 Calling OpenRouter...")
        
        response = requests.post(
            url="https://openrouter.ai/api/v1/chat/completions",
            headers={
                "Authorization": f"Bearer {API_KEY}",
                "Content-Type": "application/json",
                "HTTP-Referer": "https://t.me/",
                "X-Title": "Telegram AI Bot"
            },
            json={
                "model": "gryphe/mythomist-7b:free",
                "messages": [
                    {"role": "user", "content": user_text}
                ],
                "max_tokens": 1000
            },
            timeout=60
        )
        
        print(f"📡 Status: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            ai_reply = data['choices'][0]['message']['content']
            print(f"✅ Reply: {ai_reply[:50]}...")
            
            # Send reply (split if too long)
            if len(ai_reply) > 4096:
                for i in range(0, len(ai_reply), 4096):
                    await update.message.reply_text(ai_reply[i:i+4096])
            else:
                await update.message.reply_text(ai_reply)
        else:
            error_text = f"⚠️ API Error: {response.status_code}\n{response.text[:200]}"
            print(f"❌ {error_text}")
            await update.message.reply_text(error_text)
            
    except requests.exceptions.Timeout:
        print("❌ Timeout error")
        await update.message.reply_text("⏰ Request timeout! Please try again.")
        
    except Exception as e:
        print(f"❌ Error: {type(e).__name__}: {e}")
        await update.message.reply_text(f"❌ Error: {str(e)}")

def main():
    """Start the bot"""
    print("\n" + "="*50)
    print("🚀 Starting Telegram AI Bot...")
    print("="*50 + "\n")
    
    # Create application
    application = Application.builder().token(TOKEN).build()
    
    # Add handlers
    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    
    print("✅ Bot is running! Send /start in Telegram\n")
    
    # Run the bot
    application.run_polling(drop_pending_updates=True)

if __name__ == "__main__":
    main()
