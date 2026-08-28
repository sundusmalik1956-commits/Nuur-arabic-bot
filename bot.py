from datetime import datetime
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import (
    ApplicationBuilder,
    CallbackQueryHandler,
    CommandHandler,
    ContextTypes,
    MessageHandler,
    filters,
)
from google import genai

# استيراد ملف الدرس الأول
from lesson1 import start_lesson

# التوكن الخاص ببوت تيليجرام
TOKEN = "8629063079:AAHvPGBfbTdCJyHXz2EpHWzPiG8KfgroMMo"

# ضعي مفتاح جيميني الحقيقي هنا مباشرة بين علامتي التنصيص
GEMINI_API_KEY = "iXp2hUjxXlJmdVc_xwTT7DEpVb1b1MqUJOSi-lQ"

# إعداد عميل الذكاء الاصطناعي
client = genai.Client(api_key=GEMINI_API_KEY)

# اللغات والأوقات
TRANSLATIONS = {
    "ar": {
        "welcome": "مرحباً بك في المنصة العربية! 🌟\nالرجاء اختيار لغتك:",
        "time_prompt_1": "⏰ ممتاز! الآن أرسل **وقت درسك اليومي الأول** (مثلاً: 09:00):",
        "time_prompt_2": "⏰ رائع! الآن أرسل **وقت درسك اليومي الثاني** (مثلاً: 17:00):",
        "times_saved": "✅ تم حفظ الأوقات بنجاح:\n- الوقت الأول: {t1}\n- الوقت الثاني: {t2}\n\nتم إتمام إعداد جدولك اليومي بنجاح! 🚀",
        "error_time": "⚠️ الرجاء إدخال الوقت بصيغة HH:MM الصحيحة.",
        "lang_name": "العربية (Arabic)"
    },
    "tr": {
        "welcome": "Arapça Platformuna Hoş Geldiniz! 🌟\nLütfen dilinizi seçin:",
        "time_prompt_1": "⏰ Harika! Şimdi **ilk günlük ders saatinizi** gönderin (örn: 09:00):",
        "time_prompt_2": "⏰ Harika! Şimdi **ikinci günlük ders saatinizi** gönderin (örn: 17:00):",
        "times_saved": "✅ Zamanlar başarıyla kaydedildi:\n- 1. Zaman: {t1}\n- 2. Zaman: {t2}\n\nGünlük programınız başarıyla tamamlandı! 🚀",
        "error_time": "⚠️ Lütfen zamanı HH:MM formatında girin.",
        "lang_name": "Türkçe (Turkish)"
    },
    "en": {
        "welcome": "Welcome to the Arabic Platform! 🌟\nPlease select your language:",
        "time_prompt_1": "⏰ Great! Now send your **first daily lesson time** (e.g., 09:00):",
        "time_prompt_2": "⏰ Awesome! Now send your **second daily lesson time** (e.g., 17:00):",
        "times_saved": "✅ Times saved successfully:\n- Time 1: {t1}\n- Time 2: {t2}\n\nYour daily schedule has been successfully set up! 🚀",
        "error_time": "⚠️ Please enter time format HH:MM.",
        "lang_name": "الإنجليزية (English)"
    }
}

# أمر البداية
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat = update.effective_chat
    keyboard = [
        [
            InlineKeyboardButton("🇸🇦 العربية", callback_data="lang_ar"),
            InlineKeyboardButton("🇹🇷 Türkçe", callback_data="tr"),
            InlineKeyboardButton("🇬🇧 English", callback_data="en")
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await context.bot.send_message(
        chat_id=chat.id,
        text="مرحباً بك في المنصة العربية التعليمية! 🌟\nPlease select your language / Lütfen dilinizi seçin:",
        reply_markup=reply_markup
    )

# معالجة الأزرار واختيار اللغة
async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    
    if query.data.startswith("lang_") or query.data in ["tr", "en"]:
        lang = query.data.replace("lang_", "")
        context.user_data["lang"] = lang
        
        await query.message.reply_text("تم اختيار اللغة بنجاح! دعنا نبدأ الدرس الأول 📚")
        await start_lesson(update, context)

def main():
    application = ApplicationBuilder().token(TOKEN).build()
    
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CallbackQueryHandler(button_handler))
    
    print("البوت يعمل الآن بنجاح...")
    application.run_polling()

if __name__ == "__main__":
    main()
