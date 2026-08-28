# lesson1.py
# ملف الدرس الأول: التعريف بالنفس (A1_L1)

from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import ContextTypes

# محتوى الدرس الأول كاملاً ومنظمًا
LESSON_DATA = {
    "lesson_id": "A1_L1",
    "title": "التعريف بالنفس",
    "unit": "الوحدة الأولى: التعارف والتقديم",
    "level": "A1",
    "skills": {
        "introduction": {
            "text": "مرحباً بك في أول درس لك في اللغة العربية! 🌟\n\nاليوم سنتعلم كيف نعرّف عن أنفسنا بالعربية. هذه المهارة مهمة جداً لأنها تساعدك في التعرف على الآخرين وبناء علاقات جديدة.\n\nفي هذا الدرس ستتعلم:\n• كيف تقول اسمك\n• كيف تسأل عن اسم الآخرين\n• من أين أنت\n• كيف تصف عمرك ومهنتك",
            "image": "https://drive.google.com/uc?export=download&id=1fDorqrKC-QvoElNesKW6T_Eb6ezHc10R",
            "question": "كيف تقدم نفسك بالعربية لشخص تقابله لأول مرة؟ فكر في الجمل التي ستقولها."
        },
        "vocabulary": {
            "table": [
                {"arabic": "أنا", "english": "I", "transliteration": "Ana"},
                {"arabic": "اسمي", "english": "My name is", "transliteration": "Ismi"},
                {"arabic": "ماذا", "english": "What", "transliteration": "Mādha"},
                {"arabic": "اسمك", "english": "Your name (m)", "transliteration": "Ismuka"},
                {"arabic": "اسمكِ", "english": "Your name (f)", "transliteration": "Ismuki"},
                {"arabic": "من", "english": "From", "transliteration": "Min"},
                {"arabic": "أين", "english": "Where", "transliteration": "Ayna"},
                {"arabic": "عمري", "english": "My age", "transliteration": "'Umri"},
                {"arabic": "سنة", "english": "Year(s) old", "transliteration": "Sanah"},
                {"arabic": "أنا من", "english": "I am from", "transliteration": "Ana min"}
            ],
            "image": "https://drive.google.com/uc?export=download&id=16ilPf6aByU4RsuVGYHwoSc-fGrt-KNep"
        },
        "grammar": {
            "explanation": "🔤 **ضمائر المتكلم في اللغة العربية**\n\nفي اللغة العربية، هناك ضمائر تستخدم للحديث عن النفس:\n• **أنا** = I (للمذكر والمؤنث)\n• **نحن** = We\n\n📌 **جملة الاسم في العربية:**\nتتكون من مبتدأ + خبر\nمثال: أنا (مبتدأ) طالب (خبر)\n\n⚠️ **ملاحظة مهمة:**\nالضمائر في العربية لا تحتاج إلى فعل 'يكون' كما في الإنجليزية.\n• أنا طالب = I am a student (وليس 'أنا يكون طالب')",
            "examples": [
                "أنا أحمد. = I am Ahmed.",
                "أنا طالبة. = I am a student (f).",
                "أنا من مصر. = I am from Egypt.",
                "عمري عشرون سنة. = I am twenty years old.",
                "اسمي نور. = My name is Noor."
            ]
        },
        "reading": {
            "text": "📖 **نص قراءة: التعارف**\n\nمرحباً! اسمي أحمد. أنا من السعودية. عمري 25 سنة. أنا مهندس. أعمل في شركة كبيرة. أدرس اللغة العربية الآن لأنني أحب الثقافة العربية.\n\nأحب السفر والقراءة. في وقت الفراغ، أقرأ الكتب أو أمارس الرياضة.\n\nأنا سعيد بتعلم اللغة العربية، وأتمنى أن أتحدث بها بطلاقة يوماً ما.",
            "image": "https://drive.google.com/uc?export=download&id=1B_dVPhx23mVpU9rX0v1op-aSdjxREevF",
            "audio": "https://drive.google.com/uc?export=download&id=1iKsBknxnPN23W6YQn8k7n7B7DeiWKrZM"
        },
        "listening": {
            "audio": "https://drive.google.com/uc?export=download&id=1xdl-V241ySJetMjdCmYY7qwuPLwot8Xs",
            "image": "https://drive.google.com/uc?export=download&id=1lZ22At0hJHFUdG6frxZh54TpiEyeOWb7",
            "transcript": "مرحباً! اسمي ليلى. أنا من لبنان. عمري 22 سنة. أنا طالبة في الجامعة. أدرس الطب."
        },
        "conversation": {
            "questions": [
                "ما هو اسمك؟",
                "من أين أنت؟",
                "كم عمرك؟",
                "ماذا تعمل؟ (أو ماذا تدرس؟)",
                "ماذا تحب أن تفعل في وقت الفراغ؟"
            ],
            "example_conversation": "أحمد: مرحباً! ما اسمك؟\nسارة: اسمي سارة. وأنت؟\nأحمد: أنا أحمد. من أين أنت؟\nسارة: أنا من الأردن. وأنت؟\nأحمد: أنا من السعودية. كم عمرك؟\nسارة: عمري 20 سنة. وأنت؟\nأحمد: عمري 25 سنة. تشرفت بمعرفتك!"
        }
    }
}

# دالة بدء الدرس الأول وإرسال محتواه للطالب عبر البوت
async def start_lesson(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat = update.effective_chat
    
    # 1. إرسال المقدمة مع الصورة
    intro = LESSON_DATA["skills"]["introduction"]
    await context.bot.send_photo(
        chat_id=chat.id,
        photo=intro["image"],
        caption=f"📚 **{LESSON_DATA['title']}** ({LESSON_DATA['level']})\n{LESSON_DATA['unit']}\n\n{intro['text']}\n\n💬 **سؤال التفكير:**\n{intro['question']}"
    )

    # 2. إرسال المفردات
    vocab = LESSON_DATA["skills"]["vocabulary"]
    vocab_text = "📖 **الكلمات الجديدة (Vocabulary):**\n\n"
    for item in vocab["table"]:
        vocab_text += f"• {item['arabic']} - {item['english']} ({item['transliteration']})\n"
    
    await context.bot.send_photo(
        chat_id=chat.id,
        photo=vocab["image"],
        caption=vocab_text
    )

    # 3. إرسال القاعدة النحوية
    grammar = LESSON_DATA["skills"]["grammar"]
    grammar_text = f"{grammar['explanation']}\n\n📌 **أمثلة:**\n" + "\n".join([f"• {ex}" for ex in grammar["examples"]])
    await context.bot.send_message(chat_id=chat.id, text=grammar_text)

    # 4. إرسال نص القراءة والصوت
    reading = LESSON_DATA["skills"]["reading"]
    await context.bot.send_photo(
        chat_id=chat.id,
        photo=reading["image"],
        caption=reading["text"]
    )
    await context.bot.send_audio(chat_id=chat.id, audio=reading["audio"], caption="🎧 تسجيل القراءة")

    # 5. إرسال الاستماع
    listening = LESSON_DATA["skills"]["listening"]
    await context.bot.send_audio(chat_id=chat.id, audio=listening["audio"], caption="🎧 تسجيل الاستماع (استمع جيداً)")

    # 6. فتح باب المحادثة والتمرين العملي
    conv = LESSON_DATA["skills"]["conversation"]
    conv_text = "🗣️ **تدريب المحادثة:**\nأجب الآن عن هذه الأسئلة بنفسك (كتابةً أو تسجيلاً صوتياً):\n\n"
    for q in conv["questions"]:
        conv_text += f"❓ {q}\n"
    
    await context.bot.send_message(chat_id=chat.id, text=conv_text)
