import asyncio
from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    ContextTypes,
)

TOKEN = "8629063079:AAHvPGBfbTdCJyHXz2EpHWzPiG8KfgroMMo"

# النصوص الخاصة بالدرس الثاني فقط
TRANSLATIONS = {
    "ar": {
        "lesson_title": "التعريف بالعائلة",
        "unit": "الوحدة الثانية: العائلة",
        "section_intro": "📌 **القسم الأول: التمهيد والتهيئة**",
        "section_vocab": "📚 **القسم الثاني: المفردات الجديدة**",
        "section_grammar": "⚖️ **القسم الثالث: القواعد النحوية**",
        "section_reading": "📖 **القسم الرابع: نص القراءة**",
        "section_listening": "🎧 **القسم الخامس: تدريب الاستماع**",
        "next_wait": "⏳ استراحة قصيرة لمدة 30 ثانية قبل الانتقال للقسم التالي...",
        "congrats": "🎉 مبروك! أكملت درس '{title}' بنجاح.",
        "intro_text": "مرحباً بك في درسنا الثاني! 🌟\n\nفي هذا الدرس سنتعلم كيف نتحدث عن عائلتنا بالعربية.",
        "grammar_text": "🔤 **ضمائر الملكية في اللغة العربية**\nنضيف حرف الياء (ي) للدلالة على الملكية.\nمثال: أب + ي = أبي (my father)",
        "reading_text": "📖 **نص قراءة: عائلتي**\nمرحباً! اسمي أحمد. هذه عائلتي. أبي اسمه خالد. مهندس. أمي اسمها نورة. طبيبة.",
        "listening_transcript": "أهلاً! أنا سارة. هذه عائلتي. أبي اسمه أحمد. رجل طويل. أمي اسمها منى. قصيرة.",
    }
}

# روابط الدرس الثاني المباشرة
LESSON_LINKS = {
    "intro_image": "https://drive.google.com/uc?export=download&id=1KSsRwTkcOdZo8MUXbVmX2RDh19nKHaMh",
    "vocab_image": "https://drive.google.com/uc?export=download&id=14Es4I0uAmHF5FzNsevThxc1g9p7Rmh2Z",
    "reading_image": "https://drive.google.com/uc?export=download&id=1mnQYeljFU1YaoW3u1Jl7YV7-9WHivuTd",
    "listening_audio": "https://drive.google.com/uc?export=download&id=1WKXVJy1lWQwydtEHTAOP2fzGbO633MQL",
}

VOCAB_LIST_2 = [
    ("عائلة", "Family", "'A'ila"),
    ("أب", "Father", "Ab"),
    ("أم", "Mother", "Umm"),
    ("أخ", "Brother", "Akh"),
    ("أخت", "Sister", "Ukht"),
    ("جد", "Grandfather", "Jadd"),
    ("جدة", "Grandmother", "Jadda"),
]

# أمر تشغيل الدرس الثاني مباشرة
async def start_lesson_2(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    bot = context.bot
    t = TRANSLATIONS["ar"]

    # القسم الأول: التمهيد
    await bot.send_message(chat_id=chat_id, text=f"🚀 بدء الدرس الثاني: {t['lesson_title']}\n{t['unit']}\n\n{t['section_intro']}")
    await bot.send_photo(chat_id=chat_id, photo=LESSON_LINKS["intro_image"])
    await bot.send_message(chat_id=chat_id, text=t["intro_text"])
    await asyncio.sleep(30)

    # القسم الثاني: المفردات
    await bot.send_message(chat_id=chat_id, text=t["section_vocab"])
    await bot.send_photo(chat_id=chat_id, photo=LESSON_LINKS["vocab_image"])
    vocab_text = "\n".join([f"• {item[0]} - {item[1]} ({item[2]})" for item in VOCAB_LIST_2])
    await bot.send_message(chat_id=chat_id, text=vocab_text)
    await asyncio.sleep(30)

    # القسم الثالث: القواعد
    await bot.send_message(chat_id=chat_id, text=t["section_grammar"])
    await bot.send_message(chat_id=chat_id, text=t["grammar_text"], parse_mode="Markdown")
    await asyncio.sleep(30)

    # القسم الرابع: القراءة
    await bot.send_message(chat_id=chat_id, text=t["section_reading"])
    await bot.send_photo(chat_id=chat_id, photo=LESSON_LINKS["reading_image"])
    await bot.send_message(chat_id=chat_id, text=t["reading_text"], parse_mode="Markdown")
    await asyncio.sleep(30)

    # القسم الخامس: الاستماع
    await bot.send_message(chat_id=chat_id, text=t["section_listening"])
    await bot.send_audio(chat_id=chat_id, audio=LESSON_LINKS["listening_audio"])
    await bot.send_message(chat_id=chat_id, text=f"📄 Transcript:\n{t['listening_transcript']}")

    # نهاية الدرس
    await bot.send_message(chat_id=chat_id, text=t["congrats"].format(title=t["lesson_title"]))

def main():
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start_lesson_2))
    print("بوت الدرس الثاني يعمل بنجاح...")
    app.run_polling()

if __name__ == "__main__":
    main()
