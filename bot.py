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

# استيراد دوال الدروس من الملفات الأخرى
from lesson1 import start_lesson
from lesson2 import start_lesson_2

TOKEN = "ضع_التوكن_هنا"

# النصوص والترجمات لاختيار اللغات والأوقات
TRANSLATIONS = {
    "ar": {
        "welcome": "أهلاً بك في منصة تعليم اللغة العربية! 🌟\nاختر لغتك المفضلة:",
        "time_prompt_1": (
            "⏰ ممتاز! الآن أرسل **الوقت الأول** المناسب لك يومياً لتلقي الدرس"
            " (صيغة 24 ساعة، مثلاً: 09:00):"
        ),
        "time_prompt_2": (
            "⏰ رائع! الآن أرسل **الوقت الثاني** المناسب لك يومياً لتلقي الدرس"
            " (صيغة 24 ساعة، مثلاً: 17:00):"
        ),
        "times_saved": (
            "✅ تم حفظ الموعدين بنجاح:\n- الوقت الأول: {t1}\n- الوقت الثاني:"
            " {t2}\n\nتم إعداد جدولك اليومي بنجاح! 🚀\n\nيبدأ الآن الدرس الأول:"
        ),
        "error_time": (
            "الرجاء إدخال الوقت بالتنسيق الصحيح (مثال: 14:30) / Please enter time"
            " format HH:MM"
        ),
    },
    "tr": {
        "welcome": (
            "Arapça Öğrenme Platformuna Hoş Geldiniz! 🌟\nLütfen dilinizi"
            " seçin:"
        ),
        "time_prompt_1": (
            "⏰ Harika! Şimdi günlük **birinci ders saatinizi** gönderin (Örn:"
            " 09:00):"
        ),
        "time_prompt_2": (
            "⏰ Süper! Şimdi günlük **ikinci ders saatinizi** gönderin (Örn:"
            " 17:00):"
        ),
        "times_saved": (
            "✅ Saatler başarıyla kaydedildi:\n- 1. Saat: {t1}\n- 2. Saat:"
            " {t2}\n\nGünlük programınız başarıyla ayarlandı! 🚀\n\nBirinci ders başlıyor:"
        ),
        "error_time": "Lütfen saat formatını doğru girin (Örn: 14:30)",
    },
    "en": {
        "welcome": "Welcome to the Arabic Platform! 🌟\nPlease select your language:",
        "time_prompt_1": (
            "⏰ Great! Now send your **first daily lesson time** (e.g., 09:00):"
        ),
        "time_prompt_2": (
            "⏰ Awesome! Now send your **second daily lesson time** (e.g.,"
            " 17:00):"
        ),
        "times_saved": (
            "✅ Times saved successfully:\n- Time 1: {t1}\n- Time 2:"
            " {t2}\n\nYour daily schedule has been successfully set up! 🚀\n\nStarting first lesson:"
        ),
        "error_time": "Please enter time format HH:MM",
    },
}


# 1. أمر البداية (اختيار اللغة)
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
  keyboard = [
      [
          InlineKeyboardButton("🇸🇦 العربية", callback_data="lang_ar"),
          InlineKeyboardButton("🇹🇷 Türkçe", callback_data="lang_tr"),
          InlineKeyboardButton("🇬🇧 English", callback_data="lang_en"),
      ]
  ]
  await update.message.reply_text(
      "Welcome / Lütfen dilinizi seçin / اختر لغتك:",
      reply_markup=InlineKeyboardMarkup(keyboard),
  )


# 2. معالجة اختيار اللغة وطلب الوقت الأول
async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
  query = update.callback_query
  await query.answer()
  data = query.data

  if data.startswith("lang_"):
    lang = data.split("_")[1]
    context.user_data["lang"] = lang
    t = TRANSLATIONS[lang]

    # ضبط الحالة لانتظار الوقت الأول
    context.user_data["step"] = "wait_time_1"
    await query.message.edit_text(t["welcome"] + "\n\n" + t["time_prompt_1"])


# 3. استقبال الوقتين تباعاً وحفظهما ثم تشغيل الدرس تلقائياً
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
  text = update.message.text.strip()
  lang = context.user_data.get("lang", "en")
  t = TRANSLATIONS[lang]
  step = context.user_data.get("step")

  if step == "wait_time_1":
    try:
      time_1 = datetime.strptime(text, "%H:%M").time()
      context.user_data["time_1"] = time_1
      context.user_data["step"] = "wait_time_2"
      await update.message.reply_text(t["time_prompt_2"])
    except ValueError:
      await update.message.reply_text(t["error_time"])

  elif step == "wait_time_2":
    try:
      time_2 = datetime.strptime(text, "%H:%M").time()
      context.user_data["time_2"] = time_2
      context.user_data["step"] = "done"

      t1_str = context.user_data["time_1"].strftime("%H:%M")
      t2_str = time_2.strftime("%H:%M")

      # إرسال رسالة تأكيد الحفظ
      await update.message.reply_text(
          t["times_saved"].format(t1=t1_str, t2=t2_str)
      )

      # الانتقال لتشغيل الدرس الأول تلقائياً فور حفظ الأوقات
      await start_lesson(update, context)

    except ValueError:
      await update.message.reply_text(t["error_time"])
  else:
    await update.message.reply_text("الرجاء البدء بالضغط على /start")


def main():
  app = ApplicationBuilder().token(TOKEN).build()
  app.add_handler(CommandHandler("start", start))
  app.add_handler(CommandHandler("lesson2", start_lesson_2)) # أمر اختياري لتشغيل الدرس الثاني يدوياً
  app.add_handler(CallbackQueryHandler(button_handler))
  app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
  print("البوت يعمل بنجاح مع ربط جميع الملفات...")
  app.run_polling()


if __name__ == "__main__":
  main()
