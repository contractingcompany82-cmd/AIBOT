import asyncio
import logging
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
import google.generativeai as genai
from PIL import Image
import io
import os

# Setup
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

TELEGRAM_BOT_TOKEN = "8792076630:AAGKboaI54WThB5WtQchT1joQf3ylRveUEU"
GEMINI_API_KEY = "AIzaSyBTBeL_QX2fbZS2VUs_tvmbELvZ9VSy2m0"

genai.configure(api_key=GEMINI_API_KEY)
text_model = genai.GenerativeModel('gemini-pro')
vision_model = genai.GenerativeModel('gemini-pro-vision')

# User session storage
user_sessions = {}

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    user_sessions[user_id] = {"history": []}
    
    await update.message.reply_text(
        f"👋 Namaste {update.effective_user.first_name}!\n\n"
        f"🤖 Main aapka AI assistant hoon.\n\n"
        f"✨ *Features:*\n"
        f"• 💬 Text questions\n"
        f"• 🖼️ Image analysis\n"
        f"• 📚 General Knowledge\n"
        f"• 💻 Coding help\n"
        f"• 🧮 Math solving\n\n"
        f"Bas bhejiye! 🚀",
        parse_mode='Markdown'
    )

async def handle_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    user_message = update.message.text
    
    if user_id not in user_sessions:
        user_sessions[user_id] = {"history": []}
    
    # Typing action
    await context.bot.send_chat_action(
        chat_id=update.effective_chat.id, 
        action='typing'
    )
    
    try:
        # Context add karein agar "yaad hai" jaise sawal ho
        prompt = user_message
        
        response = text_model.generate_content(prompt)
        reply = response.text
        
        # History save karein
        user_sessions[user_id]["history"].append({
            "user": user_message,
            "bot": reply
        })
        
        # Split long messages
        if len(reply) > 4000:
            chunks = [reply[i:i+4000] for i in range(0, len(reply), 4000)]
            for chunk in chunks:
                await update.message.reply_text(chunk)
        else:
            await update.message.reply_text(reply)
            
    except Exception as e:
        await update.message.reply_text(
            "❌ *Error!*\n"
            "Dobara try karein ya baad mein koshish karein.",
            parse_mode='Markdown'
        )

async def handle_image(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    
    await context.bot.send_chat_action(
        chat_id=update.effective_chat.id, 
        action='typing'
    )
    
    try:
        # Photo download karein
        photo_file = await update.message.photo[-1].get_file()
        photo_bytes = await photo_file.download_as_bytearray()
        
        # PIL Image mein convert karein
        image = Image.open(io.BytesIO(photo_bytes))
        
        # Caption check karein
        caption = update.message.caption or "Is image mein kya hai? Details mein bataiye."
        
        # Vision model se response
        response = vision_model.generate_content([caption, image])
        
        await update.message.reply_text(response.text)
        
    except Exception as e:
        await update.message.reply_text(
            "❌ Image process nahi ho payi.\n"
            f"Error: {str(e)}"
        )

async def clear_history(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    user_sessions[user_id] = {"history": []}
    await update.message.reply_text("🧹 History clear ho gayi!")

def main():
    application = Application.builder().token(TELEGRAM_BOT_TOKEN).build()
    
    # Commands
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("clear", clear_history))
    
    # Text messages
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_text))
    
    # Photos
    application.add_handler(MessageHandler(filters.PHOTO, handle_image))
    
    print("🤖 Bot with Vision is running...")
    application.run_polling()

if __name__ == "__main__":
    main()
