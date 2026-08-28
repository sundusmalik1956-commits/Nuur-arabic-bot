"""الدرس الأول: التعريف بالنفس

كل مهارة تُرسل في مهمة مستقلة، مع فاصل دقيقة واحدة بين المهارات.
"""

from telegram import InlineKeyboardButton, InlineKeyboardMarkup


INTRO_IMAGE = "https://drive.google.com/uc?export=download&id=1fDorqrKC-QvoElNesKW6T_Eb6ezHc10R"
VOCAB_IMAGE = "https://drive.google.com/uc?export=download&id=16ilPf6aByU4RsuVGYHwoSc-fGrt-KNep"
READING_IMAGE = "https://drive.google.com/uc?export=download&id=1B_dVPhx23mVpU9rX0v1op-aSdjxREevF"
READING_AUDIO = "https://drive.google.com/uc?export=download&id=1iKsBknxnPN23W6YQn8k7n7B7DeiWKrZM"
LISTENING_IMAGE = "https://drive.google.com/uc?export=download&id=1lZ22At0hJHFUdG6frxZh54TpiEyeOWb7"
LISTENING_AUDIO = "https://drive.google.com/uc?export=download&id=1xdl-V241ySJetMjdCmYY7qwuPLwot8Xs"


async def send_lesson(user_id: int, context) -> None:
    """جدولة المهارات السبع؛ يبدأ كل جزء بعد دقيقة من الجزء السابق."""
    skills = [
        "send_introduction",
        "send_vocabulary",
        "send_grammar",
        "send_reading",
        "send_listening",
        "send_conversation",
        "send_writing",
    ]

    for index, skill_name in enumerate(skills):
        context.job_queue.run_once(
            send_skill_job,
            when=index * 60,
            data={"user_id": user_id, "skill_name": skill_name},
            name=f"lesson1:{user_id}:{skill_name}",
        )

    await context.bot.send_message(
        chat_id=user_id,
        text="بدأ الدرس الأول: التعريف بالنفس.\nستصلك كل مهارة بعد دقيقة واحدة من المهارة السابقة.",
    )


async def send_skill_job(context) -> None:
    data = context.job.data
    user_id = data["user_id"]
    skill_name = data["skill_name"]
    function = globals()[skill_name]
    await function(user_id, context)

    # حفظ المهارة الحالية حتى تُنسب إجابات المحادثة والكتابة إلى مكانها الصحيح.
    from bot import announce_lesson_completion, record_progress, update_student
    update_student(user_id, current_skill=skill_name)
    # التمهيد يكتمل عند عرضه، أما بقية المهارات فتكتمل بعد إجابة التدريب أو مهمة AI.
    if skill_name == "introduction":
        finished = record_progress(user_id, 1, skill_name)
        if finished:
            await announce_lesson_completion(user_id, 1, context)


async def send_introduction(user_id: int, context) -> None:
    await context.bot.send_photo(
        chat_id=user_id,
        photo=INTRO_IMAGE,
        caption=(
            "📝 الدرس الأول: التعريف بالنفس\n\n"
            "مرحبًا بك في أول درس لك في اللغة العربية!\n\n"
            "اليوم سنتعلم كيف نعرّف عن أنفسنا بالعربية. هذه المهارة مهمة لأنها تساعدك في التعرف على الآخرين وبناء علاقات جديدة.\n\n"
            "في هذا الدرس ستتعلم:\n"
            "• كيف تقول اسمك\n• كيف تسأل عن اسم الآخرين\n• من أين أنت\n• كيف تصف عمرك ومهنتك\n\n"
            "السؤال التحفيزي:\nكيف تقدم نفسك بالعربية لشخص تقابله لأول مرة؟"
        ),
    )


async def send_vocabulary(user_id: int, context) -> None:
    text = (
        "2. المفردات\n\n"
        "أنا = I — Ana\n"
        "اسمي = My name is — Ismi\n"
        "ماذا = What — Mādha\n"
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
