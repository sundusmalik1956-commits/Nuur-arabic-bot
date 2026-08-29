# -*- coding: utf-8 -*-
"""
lesson1.py
الدرس الأول: التحيات والتعارف (مستوى A1)
يتوافق مع بنية lesson_engine و ai_service، ويشمل الصور، الصوتيات، التدريبات، والتصحيح الذكي.
رابط الوسائط: https://drive.google.com/drive/folders/1F0S-WwsGyfbHU0lmJsVTfQnJOHn_2dUR
"""

import logging
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import ContextTypes
import database as db
from services import ai_service

logger = logging.getLogger(__name__)

# مفتاح تتبع مهارة الذكاء الاصطناعي النشطة لهذا الدرس
ACTIVE_SKILL_KEY = "lesson_1_active_skill"


def get_active_skill(user_id: int) -> str | None:
    return db.get_temp_state(user_id, ACTIVE_SKILL_KEY)


def set_active_skill(user_id: int, skill: str | None):
    db.set_temp_state(user_id, ACTIVE_SKILL_KEY, skill)


async def send_lesson_1(bot, chat_id: int, lang: str):
    """إرسال محتوى الدرس الأول كاملاً باللغة المطلوبة مع الصور والصوتيات والتدريبات."""
    
    # 1. التمهيد ورابط الوسائط
    intro_text = (
        "الدرس 1: التحيات والتعارف\n"
        "Birim 1: Selamlaşma ve Tanışma\n\n"
        "1. التمهيد / Giriş\n"
        "أهلاً بك في عالم اللغة العربية. التواصل يبدأ بتحية طيبة والتعريف بالاسم.\n"
        "Arap dünyasına hoş geldiniz. İletişim, güzel bir selamlama ve isimle tanışma ile başlar.\n\n"
        "رابط ملفات الصور والصوت للدرس:\n"
        "https://drive.google.com/drive/folders/1F0S-WwsGyfbHU0lmJsVTfQnJOHn_2dUR\n\n"
        "سؤال تمهيدي بسيط / Basit Giriş Sorusu:\n"
        "كيف تحيي شخصاً في الصباح باللغة العربية؟\n"
        "Sabahleyin birini Arapça nasıl selamlarsınız?"
    )
    await bot.send_message(chat_id=chat_id, text=intro_text)

    # 2. المفردات
    vocab_text = (
        "2. المفردات (7 كلمات أساسية) / Kelimeler (7 Temel Kelime)\n\n"
        "1. مَرْحباً / Merhaba (Hello)\n"
        "2. صَبَاحُ الخَيْرِ / Günaydın (Good morning)\n"
        "3. اِسْمي / Benim adım (My name is)\n"
        "4. كَيْفَ حَالُكَ / Nasılsın? (How are you?)\n"
        "5. بِخَيْرٍ / İyiyim (Fine)\n"
        "6. شُكْراً / Teşekkür ederim (Thank you)\n"
        "7. مَعَ السَّلَامَةِ / Hoşçakal (Goodbye)\n\n"
        "تدريبات المفردات / Kelime Alıştırmaları:"
    )
    await bot.send_message(chat_id=chat_id, text=vocab_text)

    # تدريبات المفردات (خيارات متعددة)
    q1_keyboard = InlineKeyboardMarkup([
        [InlineKeyboardButton("أ) شكراً", callback_data="l1_v1|a"), InlineKeyboardButton("ب) أهلاً وسهلاً", callback_data="l1_v1|b")],
        [InlineKeyboardButton("ج) مع السلامة", callback_data="l1_v1|c")]
    ])
    await bot.send_message(chat_id=chat_id, text="1. ما معنى كلمة (مَرْحباً)؟ / (Marhaban) kelimesinin anlamı nedir?", reply_markup=q1_keyboard)

    q2_keyboard = InlineKeyboardMarkup([
        [InlineKeyboardButton("أ) Good morning", callback_data="l1_v2|a"), InlineKeyboardButton("ب) Good evening", callback_data="l1_v2|b")],
        [InlineKeyboardButton("ج) Good night", callback_data="l1_v2|c")]
    ])
    await bot.send_message(chat_id=chat_id, text="2. الترجمة الصحيحة لـ (صَبَاحُ الخَيْرِ) هي: / (Sabahü'l-hayr) ifadesinin doğru çevirisi:", reply_markup=q2_keyboard)

    q3_keyboard = InlineKeyboardMarkup([
        [InlineKeyboardButton("أ) كيف حالك", callback_data="l1_v3|a"), InlineKeyboardButton("ب) اسمي", callback_data="l1_v3|b")],
        [InlineKeyboardButton("ج) بخير", callback_data="l1_v3|c")]
    ])
    await bot.send_message(chat_id=chat_id, text="3. الكلمة المناسبة لتعني (My name is) باللغة العربية هي: / Arapçada (My name is) anlamına gelen kelime:", reply_markup=q3_keyboard)

    # 3. القاعدة النحوية
    grammar_text = (
        "3. القاعدة النحوية: الضمائر المنفصلة للمتكلم والمخاطب\n"
        "Dilbilgisi Kuralı: Mütekellim ve Muhatap Zamirleri\n\n"
        "الضمير | المعنى | مثال\n"
        "أَنَا | I / Ben | أنا أحدثك\n"
        "أَنْتَ | You / Sen (Müذكر/Erkek) | أنتَ طالب\n"
        "أَنْتِ | You / Sen (مؤنث/Kadın) | أنتِ طالبة\n\n"
        "شرح مبسط / Basit Açıklama:\n"
        "نستعمل (أنا) للتعبير عن النفس، و(أنتَ) لمخاطبة الذكر، و(أنتِ) لمخاطبة الأنثى.\n"
        "(Ana) kelimesini kendimizi ifade etmek için, (Ente) erkek muhatap için, (Enti) kadın muhatap için kullanırız.\n\n"
        "تدريبات القاعدة / Kural Alıştırmaları:"
    )
    await bot.send_message(chat_id=chat_id, text=grammar_text)

    g1_keyboard = InlineKeyboardMarkup([
        [InlineKeyboardButton("أ) أنا", callback_data="l1_g1|a"), InlineKeyboardButton("ب) أنتَ", callback_data="l1_g1|b")],
        [InlineKeyboardButton("ج) أنتِ", callback_data="l1_g1|c")]
    ])
    await bot.send_message(chat_id=chat_id, text="1. اختر الضمير المناسب: (...... طالب مجتهد) / Uygun zamiri seçin:", reply_markup=g1_keyboard)

    g2_keyboard = InlineKeyboardMarkup([
        [InlineKeyboardButton("أ) أنتِ", callback_data="l1_g2|a"), InlineKeyboardButton("ب) أنتَ", callback_data="l1_g2|b")],
        [InlineKeyboardButton("ج) أنا", callback_data="l1_g2|c")]
    ])
    await bot.send_message(chat_id=chat_id, text="2. اختر الضمير المناسب لمخاطبة المؤنث: (...... معلمة ذكية) / Müennes için uygun zamir:", reply_markup=g2_keyboard)

    g3_keyboard = InlineKeyboardMarkup([
        [InlineKeyboardButton("أ) أنتَ أدرس العربية", callback_data="l1_g3|a"), InlineKeyboardButton("ب) أنا أدرس العربية", callback_data="l1_g3|b")],
        [InlineKeyboardButton("ج) أنتِ أدرس العربية", callback_data="l1_g3|c")]
    ])
    await bot.send_message(chat_id=chat_id, text="3. الجملة الصحيحة للمتكلم هي: / Mütekellim (Konuşmacı) için doğru cümle:", reply_markup=g3_keyboard)

    # 4. نص القراءة
    reading_text = (
        "4. نص القراءة / Okuma Metni\n\n"
        "أنا أحمد. أنا من الأردن. أنا طالب في الجامعة. وأنتَ؟ ما اسمك ومن أين أنت؟\n"
        "Ben Ahmet. Ben Ürdünlüyüm. Üniversitede öğrenciyim. Ya sen? Adın ne ve nerelisin?\n\n"
        "تدريبات القراءة / Okuma Alıştırmaları:"
    )
    await bot.send_message(chat_id=chat_id, text=reading_text)

    r1_keyboard = InlineKeyboardMarkup([
        [InlineKeyboardButton("أ) محمد", callback_data="l1_r1|a"), InlineKeyboardButton("ب) أحمد", callback_data="l1_r1|b")],
        [InlineKeyboardButton("ج) علي", callback_data="l1_r1|c")]
    ])
    await bot.send_message(chat_id=chat_id, text="1. ما اسم الشخصية في النص؟ / Metindeki kişinin adı nedir?", reply_markup=r1_keyboard)

    r2_keyboard = InlineKeyboardMarkup([
        [InlineKeyboardButton("أ) من مصر", callback_data="l1_r2|a"), InlineKeyboardButton("ب) من سوريا", callback_data="l1_r2|b")],
        [InlineKeyboardButton("ج) من الأردن", callback_data="l1_r2|c")]
    ])
    await bot.send_message(chat_id=chat_id, text="2. من أين أحمد؟ / Ahmet nerelidir?", reply_markup=r2_keyboard)

    r3_keyboard = InlineKeyboardMarkup([
        [InlineKeyboardButton("أ) طالب", callback_data="l1_r3|a"), InlineKeyboardButton("ب) معلم", callback_data="l1_r3|b")],
        [InlineKeyboardButton("ج) طبيب", callback_data="l1_r3|c")]
    ])
    await bot.send_message(chat_id=chat_id, text="3. ما هي مهنة أحمد؟ / Ahmet'in mesleği nedir?", reply_markup=r3_keyboard)

    # 5. نص الاستماع
    listening_text = (
        "5. نص الاستماع / Dinleme Metni\n\n"
        "صباح الخير! أنا سارة من ألمانيا، عمري عشرون سنة، وأتمنى أن أتحدث العربية بطلاقة.\n"
        "Günaydın! Ben Almanya'dan Sara, yirmi yaşındayım ve akıcı bir şekilde Arapça konuşmayı umuyorum.\n\n"
        "تدريبات الاستماع / Dinleme Alıştırmaları:"
    )
    await bot.send_message(chat_id=chat_id, text=listening_text)

    l1_keyboard = InlineKeyboardMarkup([
        [InlineKeyboardButton("أ) من ألمانيا", callback_data="l1_l1|a"), InlineKeyboardButton("ب) من تركيا", callback_data="l1_l1|b")],
        [InlineKeyboardButton("ج) من الإمارات", callback_data="l1_l1|c")]
    ])
    await bot.send_message(chat_id=chat_id, text="1. من أين سارة؟ / Sara nerelidir?", reply_markup=l1_keyboard)

    l2_keyboard = InlineKeyboardMarkup([
        [InlineKeyboardButton("أ) 18 سنة", callback_data="l1_l2|a"), InlineKeyboardButton("ب) 20 سنة", callback_data="l1_l2|b")],
        [InlineKeyboardButton("ج) 25 سنة", callback_data="l1_l2|c")]
    ])
    await bot.send_message(chat_id=chat_id, text="2. كم عمر سارة؟ / Sara kaç yaşındadır?", reply_markup=l2_keyboard)

    l3_keyboard = InlineKeyboardMarkup([
        [InlineKeyboardButton("أ) أن تسافر", callback_data="l1_l3|a"), InlineKeyboardButton("ب) أن تتحدث العربية بطلاقة", callback_data="l1_l3|b")],
        [InlineKeyboardButton("ج) أن تتعلم الإنجليزية", callback_data="l1_l3|c")]
    ])
    await bot.send_message(chat_id=chat_id, text="3. ماذا تتمنى سارة؟ / Sara neyi umut ediyor / arzuluyor?", reply_markup=l3_keyboard)

    # 6. تدريب المحادثة
    set_active_skill(chat_id, "speaking")
    conv_text = (
        "6. تدريب المحادثة (تفاعل ذكي مع الذكاء الاصطناعي)\n"
        "Konuşma Alıştırması (Yapay Zeka ile Etkileşim)\n\n"
        "أجب عن الأسئلة التالية باللغة العربية (نصياً أو بصوتك)، وسيقوم البوت بتصحيحها ومساعدتك:\n"
        "Aşağıdaki soruları Arapça olarak cevaplayın (yazılı veya sesli olarak), bot düzeltecektir:\n\n"
        "1. ما اسمك؟ (Adın ne?)\n"
        "2. من أين أنت؟ (Nerelisin?)\n"
        "3. كم عمرك؟ (Kaç yaşındasın?)"
    )
    await bot.send_message(chat_id=chat_id, text=conv_text)


async def handle_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """معالجة إجابات الأزرار للتدريبات وإعطاء التغذية الراجعة الفورية"""
    query = update.callback_query
    await query.answer()
    data = query.data
    user_id = query.from_user.id
    lang = db.get_user(user_id).get("language", "ar")

    # التحقق من صحة الإجابات المفترضة للدرس الأول
    answers_key = {
        "l1_v1": "b", "l1_v2": "a", "l1_v3": "b",
        "l1_g1": "b", "l1_g2": "a", "l1_g3": "b",
        "l1_r1": "b", "l1_r2": "c", "l1_r3": "a",
        "l1_l1": "a", "l1_l2": "b", "l1_l3": "b"
    }

    parts = data.split("|")
    question_id = parts[0]
    user_choice = parts[1]

    if question_id in answers_key:
        correct_choice = answers_key[question_id]
        if user_choice == correct_choice:
            feedback = "إجابة صحيحة! أحسنت. / Doğru cevap! Aferin."
        else:
            feedback = f"إجابة خاطئة. الإجابة الصحيحة هي: {correct_choice.upper()} / Yanlış cevap. Doğru olan: {correct_choice.upper()}"
        
        await query.message.reply_text(feedback)
        
        # الانتقال لتدريب الكتابة تلقائياً بعد إنهاء آخر تدريب استماع
        if question_id == "l1_l3":
            set_active_skill(user_id, "writing")
            writing_prompt = (
                "7. تدريب الكتابة / Yazma Alıştırması\n\n"
                "اكتب فقرة قصيرة من 3 إلى 5 جمل تقدم فيها نفسك باللغة العربية (اذكر اسمك، ومن أين أنت، وعمرك).\n"
                "Kendinizi tanıtan 3-5 cümlelik kısa bir paragraf yazın (isminizi, nereli olduğunuzu ve yaşınızı belirtin).\n\n"
                "أرسل إجابتك الآن وسيقوم البوت بتصحيحها وفحصها!\n"
                "Cevabınızı şimdi gönderin, bot düzeltecektir!"
            )
            await context.bot.send_message(chat_id=user_id, text=writing_prompt)


async def handle_ai_interaction(context: ContextTypes.DEFAULT_TYPE, user_id: int, active_skill: str, student_text: str = None, audio_bytes: bytes = None):
    """معالجة إجابات المحادثة أو الكتابة عبر طبقة الذكاء الاصطناعي مع إرسال إشعار الإتمام للمجموعة"""
    prompt_context = "الدرس الأول: التحيات والتعارف. طالب مستوي A1 يقدم نفسه ويجيب عن الأسئلة (الاسم، البلد، العمر)."
    
    result = None
    if audio_bytes:
        result = ai_service.correct_speaking_audio(audio_bytes, prompt_context, student_lang="tr")
    elif student_text:
        if active_skill == "speaking":
            result = ai_service.correct_speaking_text(student_text, prompt_context, student_lang="tr")
        elif active_skill == "writing":
            result = ai_service.correct_writing(student_text, prompt_context, student_lang="tr")

    if result:
        feedback_msg = (
            f"نتيجة التصحيح الذكي / Akıllı Düzeltme Sonucu:\n\n"
            f"التصحيح: {result.corrected_text}\n"
            f"الشرح: {result.explanation}"
        )
        await context.bot.send_message(chat_id=user_id, text=feedback_msg)

        if result.is_correct:
            set_active_skill(user_id, None)
            
            # إرسال رسالة الإتمام للقروب الإداري (ADMIN_GROUP_ID)
            admin_group_id = os.environ.get("ADMIN_GROUP_ID")
            if admin_group_id:
                user_info = db.get_user(user_id)
                username = user_info.get("username", "مستخدم")
                completion_msg = f"أتم الطالب @{username} الدرس الأول بنجاح وتجاوز تدريبات المحادثة والكتابة!"
                try:
                    await context.bot.send_message(chat_id=admin_group_id, text=completion_msg)
                except Exception:
                    logger.exception("فشل إرسال إشعار الإتمام للمجموعة الإدارية")
    else:
        await context.bot.send_message(chat_id=user_id, text="تعذر تحليل الإجابة الآن. حاول مرة أخرى لاحقاً. / Şu anda cevap analiz edilemedi. Lütfen daha sonra tekrar deneyin.")
        "اسمك = Your name — Ismuka / Ismuki\n"
        "من = From — Min\n"
        "أين = Where — Ayna\n"
        "عمري = My age — 'Umri\n"
        "سنة = Year(s) old — Sanah\n"
        "أنا من = I am from — Ana min"
    )
    await context.bot.send_photo(chat_id=user_id, photo=VOCAB_IMAGE, caption=text)
    await context.bot.send_message(
        chat_id=user_id,
        text="تدريب المفردات 1: ماذا تعني كلمة «اسمي» باللغة الإنجليزية؟",
        reply_markup=quiz_keyboard("v1", ["My name is", "Your name", "I am", "From"]),
    )


async def send_grammar(user_id: int, context) -> None:
    await context.bot.send_message(
        chat_id=user_id,
        text=(
            "3. القواعد\n\n"
            "ضمائر المتكلم:\nأنا = I للمذكر والمؤنث\nنحن = We\n\n"
            "الجملة الاسمية تتكون من مبتدأ + خبر.\n"
            "مثال: أنا طالب = I am a student.\n\n"
            "ملاحظة: الضمائر العربية لا تحتاج إلى فعل «يكون».\n\n"
            "أمثلة:\n"
            "أنا أحمد.\nأنا طالبة.\nأنا من مصر.\nعمري عشرون سنة.\nاسمي نور.\n\n"
            "تدريب القواعد: اختر الجملة الصحيحة التي تعني I am a student."
        ),
        reply_markup=quiz_keyboard("g1", ["أنا طالب", "اسمي طالب", "أنا من طالب", "عمري طالب"]),
    )


async def send_reading(user_id: int, context) -> None:
    await context.bot.send_photo(
        chat_id=user_id,
        photo=READING_IMAGE,
        caption=(
            "4. القراءة — التعارف\n\n"
            "مرحبًا! اسمي أحمد. أنا من ألمانيا. عمري 25 سنة. أنا مهندس. أعمل في شركة كبيرة. "
            "أدرس اللغة العربية الآن لأنني أحب الثقافة العربية.\n\n"
            "أحب السفر والقراءة. في وقت الفراغ، أقرأ الكتب أو أمارس الرياضة.\n\n"
            "أنا سعيد بتعلم اللغة العربية، وأتمنى أن أتحدث بها بطلاقة يومًا ما."
        ),
    )
    await context.bot.send_audio(chat_id=user_id, audio=READING_AUDIO)
    await context.bot.send_message(
        chat_id=user_id,
        text="تدريب القراءة: من أين هو أحمد؟",
        reply_markup=quiz_keyboard("r1", ["مصر", "ألمانيا", "الأردن", "الإمارات"]),
    )


async def send_listening(user_id: int, context) -> None:
    await context.bot.send_photo(chat_id=user_id, photo=LISTENING_IMAGE, caption="5. الاستماع")
    await context.bot.send_audio(chat_id=user_id, audio=LISTENING_AUDIO)
    await context.bot.send_message(
        chat_id=user_id,
        text="تدريب الاستماع: ما اسم المتحدثة؟",
        reply_markup=quiz_keyboard("l1", ["أحمد", "ليلى", "نور", "سارة"]),
    )


async def send_conversation(user_id: int, context) -> None:
    await context.bot.send_message(
        chat_id=user_id,
        text=(
            "6. المحادثة\n\n"
            "أجب عن الأسئلة التالية بالعربية، وسيساعدك الذكاء الاصطناعي في التصحيح:\n"
            "1. ما اسمك؟\n2. من أين أنت؟\n3. كم عمرك؟\n4. ماذا تعمل أو تدرس؟\n"
            "5. ماذا تحب أن تفعل في وقت الفراغ؟\n\n"
            "نموذج حوار:\n"
            "أحمد: مرحبًا! ما اسمك؟\n"
            "سارة: اسمي سارة. وأنت؟\n"
            "أحمد: أنا أحمد. من أين أنت؟\n"
            "سارة: أنا من الأردن. وأنت؟\n"
            "أحمد: أنا من السعودية. كم عمرك؟\n"
            "سارة: عمري 20 سنة. وأنت؟"
        ),
    )


async def send_writing(user_id: int, context) -> None:
    await context.bot.send_message(
        chat_id=user_id,
        text=(
            "7. الكتابة\n\n"
            "اكتب فقرة قصيرة من 3 إلى 5 جمل تقدم فيها نفسك بالعربية. اذكر اسمك، ومن أين أنت، وعمرك، وماذا تعمل أو تدرس.\n\n"
            "نموذج إجابة:\n"
            "مرحبًا! اسمي محمد. أنا من مصر. عمري 24 سنة. أنا طالب في الجامعة. "
            "أدرس الهندسة. أحب كرة القدم والسفر.\n\n"
            "أرسل فقرتك الآن، وسيقوم الذكاء الاصطناعي بتصحيحها."
        ),
    )


def quiz_keyboard(question_id: str, options: list[str]) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup([
        [InlineKeyboardButton(option, callback_data=f"lesson1:{question_id}:{index}")]
        for index, option in enumerate(options)
    ])


QUIZES = {
    "v1": (0, "اسمي = My name is"),
    "g1": (0, "أنا طالب = I am a student"),
    "r1": (1, "أحمد من ألمانيا. الإجابة الصحيحة هي: ألمانيا."),
    "l1": (1, "المتحدثة هي ليلى."),
}


async def handle_callback(query, context) -> None:
    """معالجة إجابات الاختيار من متعدد للدرس الأول."""
    _, question_id, selected = query.data.split(":")
    selected = int(selected)
    correct_index, explanation = QUIZES[question_id]
    await query.answer()

    if selected == correct_index:
        await query.edit_message_text(f"✅ إجابة صحيحة!\n\n{explanation}")
        return True
    await query.answer("إجابة غير صحيحة، حاول مرة أخرى.", show_alert=True)
    return False
