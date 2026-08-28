import asyncio
from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    ContextTypes,
    filters,
    MessageHandler,
)

TOKEN = "8629063079:AAHvPGBfbTdCJyHXz2EpHWzPiG8KfgroMMo"

# النصوص والترجمات الخاصة بالدرس الأول فقط
TRANSLATIONS = {
    "ar": {
        "lesson_title": "التعريف بالنفس",
        "unit": "الوحدة الأولى: التعارف والتقديم",
        "section_intro": "📌 **القسم الأول: التمهيد والتهيئة**",
        "section_vocab": "📚 **القسم الثاني: المفردات الجديدة**",
        "section_grammar": "⚖️ **القسم الثالث: القواعد النحوية**",
        "section_reading": "📖 **القسم الرابع: نص القراءة**",
        "section_listening": "🎧 **القسم الخامس: تدريب الاستماع**",
        "next_wait": "⏳ استراحة قصيرة لمدة 30 ثانية قبل الانتقال للقسم التالي...",
        "congrats": "🎉 مبروك! أكملت درس '{title}' بنجاح.",
        "intro_text": (
            "مرحباً بك في أول درس لك في اللغة العربية! 🌟\n\nاليوم سنتعلم كيف"
            " نعرّف عن أنفسنا بالعربية. هذه المهارة مهمة جداً."
        ),
        "grammar_text": (
            "🔤 **ضمائر المتكلم في اللغة العربية**\n• **أنا** = I\n• **نحن** = We"
        ),
        "reading_text": (
            "📖 **نص قراءة: التعارف**\nمرحباً! اسمي أحمد. أنا من السعودية. عمري"
            " 25 سنة."
        ),
        "listening_transcript": (
            "مرحباً! اسمي ليلى. أنا من لبنان. عمري 22 سنة."
        ),
    },
    "en": {
        "lesson_title": "Self Introduction",
        "unit": "Unit 1",
        "section_intro": "📌 **Section 1: Introduction**",
        "section_vocab": "📚 **Section 2: Vocabulary**",
        "section_grammar": "⚖️ **Section 3: Grammar**",
        "section_reading": "📖 **Section 4: Reading**",
        "section_listening": "🎧 **Section 5: Listening**",
        "next_wait": "⏳ Waiting 30 seconds before the next section...",
        "congrats": "🎉 Congratulations! You completed '{title}'.",
        "intro_text": "Welcome to your first Arabic lesson! 🌟",
        "grammar_text": "Pronouns...",
        "reading_text": "Reading text...",
        "listening_transcript": "Listening transcript...",
    },
}

# روابط الدرس الأول المباشرة
LESSON_LINKS = {
    "intro_image": (
        "https://drive.google.com/uc?export=download&id=1fDorqrKC-QvoElNesKW6T_Eb6ezHc10R"
    ),
    "vocab_image": (
        "https://drive.google.com/uc?export=download&id=16ilPf6aByU4RsuVGYHwoSc-fGrt-KNep"
    ),
    "reading_image": (
        "https://drive.google.com/uc?export=download&id=1B_dVPhx23mVpU9rX0v1op-aSdjxREevF"
    ),
    "reading_audio": (
        "https://drive.google.com/uc?export=download&id=1iKsBknxnPN23W6YQn8k7n7B7DeiWKrZM"
    ),
    "listening_image": (
        "https://drive.google.com/uc?export=download&id=1lZ22At0hJHFUdG6frxZh54TpiEyeOWb7"
    ),
    "listening_audio": (
        "https://drive.google.com/uc?export=download&id=1xdl-V241ySJetMjdCmYY7qwuPLwot8Xs"
    ),
}

VOCAB_LIST = [
    ("أنا", "I", "Ana"),
    ("اسمي", "My name is", "Ismi"),
    ("ماذا", "What", "Mādha"),
    ("اسمك", "Your name (m)", "Ismuka"),
    ("اسمكِ", "Your name (f)", "Ismuki"),
    ("من", "From", "Min"),
    ("أين", "Where", "Ayna"),
    ("عمري", "My age", "'Umri"),
    ("سنة", "Year(s) old", "Sanah"),
    ("أنا من", "I am from", "Ana min"),
]


# أمر تشغيل الدرس الأول مباشرة
async def start_lesson(update: Update, context: ContextTypes.DEFAULT_TYPE):
  chat_id = update.effective_chat.id
  bot = context.bot
  lang = "ar"  # اللغة الافتراضية للدرس
  t = TRANSLATIONS[lang]

  # القسم الأول: التمهيد
  await bot.send_message(
      chat_id=chat_id,
      text=(
          f"🚀 بدء الدرس: {t['lesson_title']}\n{t['unit']}\n\n"
          + t["section_intro"]
      ),
  )
  await bot.send_photo(chat_id=chat_id, photo=LESSON_LINKS["intro_image"])
  await bot.send_message(chat_id=chat_id, text=t["intro_text"])
  await asyncio.sleep(30)

  # القسم الثاني: المفردات
  await bot.send_message(chat_id=chat_id, text=t["section_vocab"])
  await bot.send_photo(chat_id=chat_id, photo=LESSON_LINKS["vocab_image"])
  vocab_text = "\n".join(
      [f"• {item[0]} - {item[1]} ({item[2]})" for item in VOCAB_LIST]
  )
  await bot.send_message(chat_id=chat_id, text=vocab_text)
  await asyncio.sleep(30)

  # القسم الثالث: القواعد
  await bot.send_message(chat_id=chat_id, text=t["section_grammar"])
  await bot.send_message(
      chat_id=chat_id, text=t["grammar_text"], parse_mode="Markdown"
  )
  await asyncio.sleep(30)

  # القسم الرابع: القراءة
  await bot.send_message(chat_id=chat_id, text=t["section_reading"])
  await bot.send_photo(chat_id=chat_id, photo=LESSON_LINKS["reading_image"])
  await bot.send_message(
      chat_id=chat_id, text=t["reading_text"], parse_mode="Markdown"
  )
  await bot.send_audio(chat_id=chat_id, audio=LESSON_LINKS["reading_audio"])
  await asyncio.sleep(30)

  # القسم الخامس: الاستماع
  await bot.send_message(chat_id=chat_id, text=t["section_listening"])
  await bot.send_photo(chat_id=chat_id, photo=LESSON_LINKS["listening_image"])
  await bot.send_audio(chat_id=chat_id, audio=LESSON_LINKS["listening_audio"])
  await bot.send_message(
      chat_id=chat_id, text=f"📄 Transcript:\n{t['listening_transcript']}"
  )

  # نهاية الدرس
  await bot.send_message(
      chat_id=chat_id, text=t["congrats"].format(title=t["lesson_title"])
  )


def main():
  app = ApplicationBuilder().token(TOKEN).build()
  app.add_handler(CommandHandler("start", start_lesson))
  print("بوت الدرس الأول يعمل بنجاح...")
  app.run_polling()


if __name__ == "__main__":
  main()
