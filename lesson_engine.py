# -*- coding: utf-8 -*-
"""
lesson_engine.py
المحرك المشترك الذي تستدعيه كل ملفات lessonN.py عبر واجهة موحّدة send_lesson().
مسؤول عن:
  - إرسال كل مهارة (تمهيد/مفردات/قواعد/قراءة/استماع/محادثة/كتابة) في وقتها عبر JobQueue
    (بدون أي مهمة معلّقة تنتظر anyio.sleep طوال الدرس).
  - بناء أزرار الاختيار من متعدد وتسجيل كل إجابة في قاعدة البيانات.
  - عدم اعتبار الدرس مكتملًا إلا بعد تحقّق شروط إتمام كل مهاراته فعليًا.
  - إعلان الإنجاز في قروب المناقشة بعد التحقق الفعلي فقط.

هيكل بيانات الدرس المتوقع من كل lessonN.py (dict LESSON) موثّق في lesson_schema.py
"""

import logging
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes

import database as db
from translations import t
from config import ACHIEVEMENT_GROUP_ID
from services import ai_service

logger = logging.getLogger(__name__)

def _bilingual(entry: dict, lang: str) -> str:
    """يعرض النص بالعربية دائمًا، ويضيف ترجمة لغة الطالب أسفلها إن كانت لغته غير العربية.
    entry: قاموس مثل {"ar": "...", "en": "...", "tr": "..."}"""
    ar_text = entry.get("ar", "")
    if lang == "ar" or lang not in entry:
        return ar_text
    other_text = entry.get(lang, "")
    if not other_text or other_text == ar_text:
        return ar_text
    return f"{ar_text}\n{other_text}"


SKILL_TITLE_KEY = {
    "intro": "skill_intro",
    "vocab": "skill_vocab",
    "grammar": "skill_grammar",
    "reading": "skill_reading",
    "listening": "skill_listening",
    "speaking": "skill_speaking",
    "writing": "skill_writing",
}

# مهارات تُعتبر "مكتملة تلقائيًا" بمجرد قراءة المحتوى (لا تدريبات اختيارية فيها)
CONTENT_ONLY_SKILLS = {"intro"}
# مهارات تُصحَّح بواسطة AI ولا تحتوي على أزرار اختيار من متعدد
AI_SKILLS = {"speaking", "writing"}


async def send_lesson(bot, user_id: int, language: str, lesson_number: int, context: ContextTypes.DEFAULT_TYPE):
    """نقطة الدخول الموحّدة: تبدأ درسًا لطالب (تُستدعى من الجدولة اليومية أو /lesson للاختبار)."""
    lesson = _load_lesson_module(lesson_number)
    if lesson is None:
        logger.warning(f"لا يوجد محتوى بعد للدرس رقم {lesson_number} (المستخدم {user_id}).")
        return

    db.reset_lesson_progress(user_id, lesson_number)
    db.mark_lesson_started_today(user_id)

    await _send_step(context, user_id, lesson_number, step_index=0)


def _load_lesson_module(lesson_number: int):
    import importlib
    module_name = f"lesson{lesson_number}"
    try:
        module = importlib.import_module(module_name)
        importlib.reload(module)
        return module.LESSON
    except ModuleNotFoundError:
        return None
    except Exception:
        logger.exception(f"خطأ أثناء تحميل {module_name}")
        return None


def _build_choice_keyboard(lesson_number: int, skill: str, question_key: str, options: list) -> InlineKeyboardMarkup:
    buttons = []
    for i, opt in enumerate(options):
        callback_data = f"ans|{lesson_number}|{skill}|{question_key}|{i}"
        buttons.append([InlineKeyboardButton(opt, callback_data=callback_data)])
    return InlineKeyboardMarkup(buttons)


async def _send_step(context: ContextTypes.DEFAULT_TYPE, user_id: int, lesson_number: int, step_index: int):
    try:
        await _send_step_inner(context, user_id, lesson_number, step_index)
    except Exception:
        logger.exception(f"خطأ أثناء إرسال خطوة الدرس {lesson_number} (step {step_index}) للمستخدم {user_id}")
        user = db.get_user(user_id)
        lang = user.get("language") if user else "ar"
        try:
            await context.bot.send_message(chat_id=user_id, text=t("generic_error", lang or "ar"))
        except Exception:
            pass


async def _send_step_inner(context: ContextTypes.DEFAULT_TYPE, user_id: int, lesson_number: int, step_index: int):
    user = db.get_user(user_id)
    if not user or not user.get("active", 1):
        return
    lang = user.get("language", "ar")

    lesson = _load_lesson_module(lesson_number)
    if lesson is None:
        return
    steps = lesson["steps"]

    if step_index >= len(steps):
        await _finalize_lesson(context, user_id, lesson_number, lesson, lang)
        return

    step = steps[step_index]
    skill = step["skill"]
    title = t(SKILL_TITLE_KEY.get(skill, "skill_intro"), lang)

    db.start_skill(user_id, lesson_number, skill)

    if skill == "intro":
        await _send_intro(context, user_id, step, title)
        db.complete_skill(user_id, lesson_number, skill)

    elif skill == "vocab":
        await _send_vocab(context, user_id, lang, lesson_number, step, title)

    elif skill == "grammar":
        await _send_grammar(context, user_id, lang, lesson_number, step, title)

    elif skill == "reading":
        await _send_reading(context, user_id, lang, lesson_number, step, title)

    elif skill == "listening":
        await _send_listening(context, user_id, lang, lesson_number, step, title)

    elif skill == "speaking":
        await _send_ai_prompt(context, user_id, lang, step, title, "speaking_prompt_note")

    elif skill == "writing":
        await _send_ai_prompt(context, user_id, lang, step, title, "writing_prompt_note")

    # جدولة الخطوة التالية (لا ننتظر هنا، JobQueue يتكفّل بالتوقيت)
    next_index = step_index + 1
    delay_seconds = steps[next_index].get("delay_minutes", 1) * 60 if next_index < len(steps) else 30

    context.job_queue.run_once(
        _step_job,
        when=delay_seconds,
        data={"user_id": user_id, "lesson_number": lesson_number, "step_index": next_index},
        name=f"lesson_step_{user_id}_{lesson_number}_{next_index}",
    )


async def _step_job(context: ContextTypes.DEFAULT_TYPE):
    data = context.job.data
    await _send_step(context, data["user_id"], data["lesson_number"], data["step_index"])


# ---------------------------------------------------------------------------
# إرسال كل نوع مهارة
# ---------------------------------------------------------------------------

async def _send_intro(context, user_id, step, title):
    user = db.get_user(user_id)
    lang = user.get("language", "ar")
    body = _bilingual(step["text"], lang)
    message = f"{title}\n\n{body}"
    if step.get("motivational_question"):
        question = _bilingual(step["motivational_question"], lang)
        message += f"\n\n💬 {question}"

    image = step.get("image")
    if image:
        await context.bot.send_photo(chat_id=user_id, photo=image, caption=message)
    else:
        await context.bot.send_message(chat_id=user_id, text=message)


def _format_grammar_table(table_rows: list, lang: str) -> str:
    """table_rows: [{"pronoun": "أنا", "meaning": {"en": "I", "tr": "Ben"}, "example": "أنا أحدثك"}, ...]"""
    lines = []
    for row in table_rows:
        meaning = row.get("meaning", {}).get(lang, row.get("meaning", {}).get("en", ""))
        line = f"• {row['pronoun']}"
        if lang != "ar" and meaning:
            line += f" ({meaning})"
        line += f" — {row.get('example', '')}"
        lines.append(line)
    return "\n".join(lines)


def _lang(user_id):
    user = db.get_user(user_id)
    return user.get("language", "ar") if user else "ar"


async def _send_vocab(context, user_id, lang, lesson_number, step, title):
    lines = []
    for item in step.get("vocab_table", []):
        meaning = item["meaning"].get(lang, item["meaning"].get("en", ""))
        pronunciation = item.get("transliteration", "")
        lines.append(f"• {item['ar']} ({pronunciation}) — {meaning}")
    message = f"{title}\n\n" + "\n".join(lines)

    image = step.get("image")
    if image:
        await context.bot.send_photo(chat_id=user_id, photo=image, caption=message)
    else:
        await context.bot.send_message(chat_id=user_id, text=message)

    exercises = step.get("exercises", [])
    if exercises:
        await _send_exercises(context, user_id, lang, lesson_number, "vocab", exercises)
    else:
        db.complete_skill(user_id, lesson_number, "vocab")


async def _send_grammar(context, user_id, lang, lesson_number, step, title):
    explanation = _bilingual(step["explanation"], lang)
    examples = "\n".join(step.get("examples", []))
    message = f"{title}\n\n{explanation}\n\n📝 أمثلة:\n{examples}"
    if step.get("table"):
        message += "\n\n" + _format_grammar_table(step["table"], lang)
    await context.bot.send_message(chat_id=user_id, text=message)

    exercises = step.get("exercises", [])
    if exercises:
        await _send_exercises(context, user_id, lang, lesson_number, "grammar", exercises)
    else:
        db.complete_skill(user_id, lesson_number, "grammar")


async def _send_reading(context, user_id, lang, lesson_number, step, title):
    message = f"{title}\n\n{step.get('reading_text', '')}"
    image = step.get("image")
    if image:
        await context.bot.send_photo(chat_id=user_id, photo=image, caption=message)
    else:
        await context.bot.send_message(chat_id=user_id, text=message)

    if step.get("audio"):
        await context.bot.send_audio(chat_id=user_id, audio=step["audio"])

    exercises = step.get("exercises", [])
    if exercises:
        await _send_exercises(context, user_id, lang, lesson_number, "reading", exercises)
    else:
        db.complete_skill(user_id, lesson_number, "reading")


async def _send_listening(context, user_id, lang, lesson_number, step, title):
    image = step.get("image")
    if image:
        await context.bot.send_photo(chat_id=user_id, photo=image, caption=title)
    else:
        await context.bot.send_message(chat_id=user_id, text=title)

    if step.get("audio"):
        await context.bot.send_audio(chat_id=user_id, audio=step["audio"])

    exercises = step.get("exercises", [])
    if exercises:
        await _send_exercises(context, user_id, lang, lesson_number, "listening", exercises)
    else:
        db.complete_skill(user_id, lesson_number, "listening")


async def _send_ai_prompt(context, user_id, lang, step, title, note_key):
    questions = step.get("questions", [])
    q_lines = [f"{i+1}. {_bilingual(q, lang)}" for i, q in enumerate(questions)]
    q_text = "\n".join(q_lines)
    message = f"{title}\n\n{q_text}\n\n{t(note_key, lang)}"
    await context.bot.send_message(chat_id=user_id, text=message)
    # لا نُكمل المهارة هنا؛ تُكمَل عند وصول رد الطالب ونجاح تصحيح AI (انظر bot.py)


async def _send_exercises(context, user_id, lang, lesson_number, skill, exercises):
    for i, exercise in enumerate(exercises):
        if exercise.get("type") != "multiple_choice":
            continue
        question_key = exercise.get("key", str(i))
        question_text = _bilingual(exercise["question"], lang)
        options = _localized_options(exercise, lang)
        keyboard = _build_choice_keyboard(lesson_number, skill, question_key, options)
        await context.bot.send_message(chat_id=user_id, text=f"❓ {question_text}", reply_markup=keyboard)


def _localized_options(exercise: dict, lang: str) -> list:
    """يدعم شكلين لـ options: قائمة نصوص جاهزة، أو قائمة قواميس {"ar": "...", "en": "...", "tr": "..."}
    في الحالة الثانية يعرض الخيار بالعربية + لغة الطالب معًا."""
    options = exercise["options"]
    if not options:
        return options
    if isinstance(options[0], dict):
        return [_bilingual(opt, lang).replace("\n", " / ") for opt in options]
    return options


# ---------------------------------------------------------------------------
# معالجة إجابات الأزرار
# ---------------------------------------------------------------------------

async def handle_answer_callback(update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    user_id = query.from_user.id
    user = db.get_user(user_id)
    lang = user.get("language", "ar") if user else "ar"

    _, lesson_number_str, skill, question_key, choice_index_str = query.data.split("|")
    lesson_number = int(lesson_number_str)
    choice_index = int(choice_index_str)

    lesson = _load_lesson_module(lesson_number)
    if lesson is None:
        return

    exercise = _find_exercise(lesson, skill, question_key)
    if exercise is None:
        return

    correct_index = exercise["correct_index"]
    options = _localized_options(exercise, lang)
    is_correct = choice_index == correct_index
    selected_text = options[choice_index]

    db.record_answer(user_id, lesson_number, skill, question_key, selected_text, is_correct)

    if is_correct:
        await query.edit_message_reply_markup(reply_markup=None)
        explanation = _bilingual(exercise["explanation"], lang) if exercise.get("explanation") else ""
        msg = t("correct_answer", lang)
        if explanation:
            msg += f"\n{explanation}"
        await query.message.reply_text(msg)

        # تحقق إن كانت كل أسئلة هذه المهارة أُجيبت بشكل صحيح -> اعتبرها مكتملة
        all_keys = _all_question_keys_for_skill(lesson, skill)
        if db.all_questions_answered_correctly(user_id, lesson_number, skill, all_keys):
            db.complete_skill(user_id, lesson_number, skill)
    else:
        keyboard = _build_choice_keyboard(lesson_number, skill, question_key, options)
        try:
            await query.edit_message_reply_markup(reply_markup=keyboard)
        except Exception:
            pass  # نفس المحتوى (ضغطة على نفس الزر الخاطئ)؛ تجاهل خطأ "not modified"
        await query.message.reply_text(t("wrong_answer_retry", lang))


def _find_exercise(lesson, skill, question_key):
    for step in lesson["steps"]:
        if step["skill"] != skill:
            continue
        for i, ex in enumerate(step.get("exercises", [])):
            key = ex.get("key", str(i))
            if key == question_key:
                return ex
    return None


def _all_question_keys_for_skill(lesson, skill):
    keys = []
    for step in lesson["steps"]:
        if step["skill"] != skill:
            continue
        for i, ex in enumerate(step.get("exercises", [])):
            keys.append(ex.get("key", str(i)))
    return keys


# ---------------------------------------------------------------------------
# استقبال إجابات المحادثة/الكتابة (نص أو صوت) وتصحيحها عبر AI
# ---------------------------------------------------------------------------

async def handle_ai_answer(context: ContextTypes.DEFAULT_TYPE, user_id: int, skill: str,
                            student_text: str = None, audio_bytes: bytes = None):
    """skill يجب أن تكون 'speaking' أو 'writing'. يُستدعى من bot.py عند استقبال رسالة/صوت من طالب
    في حال كانت آخر مهارة نشطة له هي هذه."""
    user = db.get_user(user_id)
    if not user:
        return
    lang = user.get("language", "ar")
    lesson_number = user["current_lesson"]

    lesson = _load_lesson_module(lesson_number)
    if lesson is None:
        return
    step = next((s for s in lesson["steps"] if s["skill"] == skill), None)
    if step is None:
        return

    prompt_context = "\n".join(q.get("ar", "") for q in step.get("questions", []))

    await context.bot.send_message(chat_id=user_id, text=t("ai_analyzing", lang))

    result = None
    if audio_bytes is not None:
        result = ai_service.correct_speaking_audio(audio_bytes, prompt_context, lang)
    elif student_text is not None:
        if skill == "writing":
            result = ai_service.correct_writing(student_text, prompt_context, lang)
        else:
            result = ai_service.correct_speaking_text(student_text, prompt_context, lang)

    if result is None:
        await context.bot.send_message(chat_id=user_id, text=t("ai_correction_unavailable", lang))
        # نعتبرها مكتملة رغم فشل AI حتى لا يعلق الطالب بلا داعٍ؛ يمكن تغييره لمراجعة يدوية لاحقًا
        db.complete_skill(user_id, lesson_number, skill)
        return

    if result.is_correct:
        await context.bot.send_message(chat_id=user_id, text=f"✅ Good!\n\n{result.explanation}")
    else:
        await context.bot.send_message(
            chat_id=user_id,
            text=f"❌ \n\nالصحيح:\n{result.corrected_text}\n\nالشرح:\n{result.explanation}",
        )

    db.complete_skill(user_id, lesson_number, skill)


def get_active_ai_skill(user_id: int):
    """يُرجع 'speaking' أو 'writing' إن كانت هذه آخر مهارة بدأها الطالب ولم تكتمل بعد، وإلا None."""
    user = db.get_user(user_id)
    if not user:
        return None
    lesson_number = user["current_lesson"]
    completed = db.get_completed_skills(user_id, lesson_number)
    for skill in ("speaking", "writing"):
        with db.get_conn() as conn:
            row = conn.execute(
                """SELECT status FROM lesson_progress
                   WHERE user_id=? AND lesson_number=? AND skill=?""",
                (user_id, lesson_number, skill),
            ).fetchone()
        if row and row["status"] == "in_progress" and skill not in completed:
            return skill
    return None


# ---------------------------------------------------------------------------
# إتمام الدرس فعليًا + إعلان الإنجاز
# ---------------------------------------------------------------------------

def _lesson_fully_completed(user_id: int, lesson_number: int, lesson: dict) -> bool:
    required_skills = {step["skill"] for step in lesson["steps"]}
    completed = db.get_completed_skills(user_id, lesson_number)
    return required_skills.issubset(completed)


async def _finalize_lesson(context: ContextTypes.DEFAULT_TYPE, user_id: int, lesson_number: int,
                            lesson: dict, lang: str):
    if not _lesson_fully_completed(user_id, lesson_number, lesson):
        # لم تكتمل كل الشروط بعد (مثلاً AI لم يُصحّح بعد) — لا شيء يُفعل الآن.
        # عندما تكتمل آخر مهارة (عبر handle_ai_answer أو handle_answer_callback)
        # يُستدعى check_and_complete_if_ready من bot.py بعد كل حدث تفاعل.
        return
    await _complete_lesson_now(context, user_id, lesson_number, lesson, lang)


async def check_and_complete_if_ready(context: ContextTypes.DEFAULT_TYPE, user_id: int):
    """يُستدعى بعد كل إجابة (زر أو AI) للتحقق: هل اكتملت كل مهارات الدرس الحالي؟"""
    user = db.get_user(user_id)
    if not user:
        return
    lesson_number = user["current_lesson"]
    lesson = _load_lesson_module(lesson_number)
    if lesson is None:
        return
    lang = user.get("language", "ar")
    if _lesson_fully_completed(user_id, lesson_number, lesson):
        # تجنّب التكرار: تحقق أنه لم يُسجَّل إتمامه من قبل
        already_done = _already_logged(user_id, lesson_number)
        if not already_done:
            await _complete_lesson_now(context, user_id, lesson_number, lesson, lang)


def _already_logged(user_id: int, lesson_number: int) -> bool:
    with db.get_conn() as conn:
        row = conn.execute(
            "SELECT id FROM completions WHERE user_id=? AND lesson_number=?",
            (user_id, lesson_number),
        ).fetchone()
        return row is not None


async def _complete_lesson_now(context: ContextTypes.DEFAULT_TYPE, user_id: int, lesson_number: int,
                                lesson: dict, lang: str):
    title = lesson.get("title", {}).get("ar", f"الدرس {lesson_number}")

    await context.bot.send_message(chat_id=user_id, text=t("lesson_complete", lang))

    db.log_completion(user_id, lesson_number, title)
    db.advance_to_next_lesson(user_id)

    await _announce_achievement(context, user_id, lesson_number, title)

    user = db.get_user(user_id)
    if db.program_finished(user):
        await context.bot.send_message(chat_id=user_id, text=t("program_complete", lang))


async def _announce_achievement(context: ContextTypes.DEFAULT_TYPE, user_id: int, lesson_number: int, lesson_title: str):
    if not ACHIEVEMENT_GROUP_ID:
        return
    user = db.get_user(user_id)
    display_name = (user.get("first_name") if user else None) or (user.get("username") if user else None) or "طالب"

    text = (
        "🎉 إنجاز جديد في نور بوت!\n\n"
        f"👤 الطالب: {display_name}\n\n"
        f"📚 أتم الدرس {lesson_number}:\n{lesson_title}\n\n"
        "🌟 أحسنت! استمر في التعلم."
    )
    try:
        await context.bot.send_message(chat_id=ACHIEVEMENT_GROUP_ID, text=text)
    except Exception:
        logger.exception("فشل إرسال إعلان الإنجاز لقروب المناقشة")
