# -*- coding: utf-8 -*-
"""
bot.py
نقطة التشغيل الرئيسية لـ "نور بوت". مسؤول فقط عن:
    Telegram، المستخدمين، الإعدادات، الجدولة، التقدّم، الاشتراك، واستدعاء الدروس.
لا يحتوي محتوى أي درس — كل درس في ملفه <level>/lessonN.py المستقل.

تسلسل التسجيل الكامل (8 خطوات):
    1. /start -> اختيار اللغة (11 لغة) -> كل شيء لاحقًا بهذه اللغة
    2. رسالة التعريف بالمنهج (المستويات، عدد الدروس، التجربة المجانية والاشتراك)
    3. اختيار المستوى (A0-B2) مع رابط اختياري لاختبار تحديد المستوى
    4. اختيار الجنس -> توجيه لرابط القروب المناسب
    5. اختيار وقت الدرس اليومي
    6. اختيار يومي إجازة أسبوعيًا (اختيار حر، وليس يومين ثابتين)
    7. ملخص شامل لكل الاختيارات + تلميح لإمكانية التعديل عبر /settings
    8. الجدولة الفعلية عبر scheduler.py بناءً على المستوى والوقت وأيام الإجازة

أوامر إضافية:
    /progress — تقدّم الطالب الحالي
    /settings — تعديل أي عنصر من عناصر التسجيل
    /export   — إداري فقط (ADMIN_USER_IDS في config.py): يرسل Excel بكل بيانات الطلاب

يشغّل هذا الملف أيضًا سيرفر HTTP داخلي بسيط (health_server.py) لتوافق الاستضافة
على Render كـ Web Service، والتي تحتاج البوت يستمع على منفذ HTTP.
"""

import os
import re
import logging

from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    Application, CommandHandler, CallbackQueryHandler, MessageHandler,
    ContextTypes, filters,
)

import database as db
from translations import (
    t, language_keyboard_rows, vacation_day_keyboard_rows, weekday_name,
)
from config import AVAILABLE_TIMES, PLACEMENT_TEST_BOT_LINK, ADMIN_USER_IDS, HEALTH_CHECK_PORT
from scheduler import (
    schedule_daily_lesson, restore_all_schedules, trigger_first_lesson_if_today,
)
from lesson_engine import (
    handle_answer_callback, handle_ai_answer, get_active_ai_skill,
    check_and_complete_if_ready, send_lesson,
)
from export_service import generate_students_excel
from health_server import start_health_server

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)
logger = logging.getLogger(__name__)

BOT_TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN")
TIME_PATTERN = re.compile(r"^([01]?\d|2[0-3]):([0-5]\d)$")


# ---------------------------------------------------------------------------
# 1) /start واختيار اللغة
# ---------------------------------------------------------------------------

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    db.create_user_if_missing(user.id, username=user.username, first_name=user.first_name)

    rows = language_keyboard_rows()
    keyboard = InlineKeyboardMarkup([[InlineKeyboardButton(label, callback_data=cb)] for label, cb in rows])
    await update.message.reply_text(t("choose_language"), reply_markup=keyboard)


async def handle_language_choice(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    user_id = query.from_user.id
    lang = query.data.split("|")[1]
    db.set_language(user_id, lang)
    await query.edit_message_reply_markup(reply_markup=None)

    user = db.get_user(user_id)
    is_first_time = user.get("level") is None  # لم يُكمل التسجيل بعد -> هذه أول مرة يختار فيها لغة

    await context.bot.send_message(chat_id=user_id, text=t("language_changed", lang))

    if is_first_time:
        # 2) رسالة التعريف بالمنهج، ثم 3) اختيار المستوى
        await context.bot.send_message(chat_id=user_id, text=t("curriculum_intro", lang))
        await _send_level_picker(context.bot, user_id, lang)
    # إن كان تغييرًا لاحقًا عبر /settings، لا داعٍ لإعادة كل التسلسل


# ---------------------------------------------------------------------------
# 3) اختيار المستوى
# ---------------------------------------------------------------------------

LEVEL_LABELS = {"A0": "A0", "A1": "A1", "A2": "A2", "B1": "B1", "B2": "B2"}


async def _send_level_picker(bot, user_id: int, lang: str):
    buttons = [InlineKeyboardButton(label, callback_data=f"level|{code}") for code, label in LEVEL_LABELS.items()]
    rows = [buttons[i:i + 3] for i in range(0, len(buttons), 3)]
    keyboard = InlineKeyboardMarkup(rows)

    await bot.send_message(chat_id=user_id, text=t("level_a0_note", lang))

    test_keyboard = InlineKeyboardMarkup([
        [InlineKeyboardButton(t("placement_test_button", lang), url=PLACEMENT_TEST_BOT_LINK)]
    ])
    await bot.send_message(chat_id=user_id, text=t("placement_test_offer", lang), reply_markup=test_keyboard)

    await bot.send_message(chat_id=user_id, text=t("choose_level", lang), reply_markup=keyboard)


async def handle_level_choice(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    user_id = query.from_user.id
    level = query.data.split("|")[1]

    user = db.get_user(user_id)
    lang = user.get("language", "ar") if user else "ar"
    is_first_time = user.get("gender") is None if user else True

    db.set_level(user_id, level)
    await query.edit_message_reply_markup(reply_markup=None)
    await context.bot.send_message(chat_id=user_id, text=t("level_confirmed", lang, level=level))

    if is_first_time:
        # 4) اختيار الجنس
        await _send_gender_picker(context.bot, user_id, lang)


# ---------------------------------------------------------------------------
# 4) الجنس والقروب
# ---------------------------------------------------------------------------

async def _send_gender_picker(bot, user_id: int, lang: str):
    keyboard = InlineKeyboardMarkup([
        [InlineKeyboardButton(t("gender_male", lang), callback_data="gender|male")],
        [InlineKeyboardButton(t("gender_female", lang), callback_data="gender|female")],
    ])
    await bot.send_message(chat_id=user_id, text=t("choose_gender", lang), reply_markup=keyboard)


async def handle_gender_choice(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    user_id = query.from_user.id
    gender = query.data.split("|")[1]

    user = db.get_user(user_id)
    lang = user.get("language", "ar") if user else "ar"
    is_first_time = user.get("lesson_time") is None if user else True

    db.set_gender_and_group(user_id, gender)
    user = db.get_user(user_id)  # إعادة القراءة لجلب group_link المحدَّث
    await query.edit_message_reply_markup(reply_markup=None)
    await context.bot.send_message(chat_id=user_id, text=t("group_invite", lang, link=user.get("group_link", "")))

    if is_first_time:
        # 5) وقت الدرس
        await _send_time_picker(context.bot, user_id, lang)


# ---------------------------------------------------------------------------
# 5) وقت الدرس
# ---------------------------------------------------------------------------

async def _send_time_picker(bot, user_id: int, lang: str):
    buttons = [InlineKeyboardButton(time_str, callback_data=f"time|{time_str}") for time_str in AVAILABLE_TIMES]
    rows = [buttons[i:i + 4] for i in range(0, len(buttons), 4)]
    keyboard = InlineKeyboardMarkup(rows)
    await bot.send_message(chat_id=user_id, text=t("ask_time", lang), reply_markup=keyboard)


async def handle_time_choice(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    user_id = query.from_user.id
    time_str = query.data.split("|")[1]
    hour, minute = map(int, time_str.split(":"))

    user = db.get_user(user_id)
    lang = user.get("language", "ar")
    is_first_time = user.get("vacation_day_1") is None

    db.set_lesson_time(user_id, time_str)
    schedule_daily_lesson(context.job_queue, user_id, hour, minute)

    await query.edit_message_reply_markup(reply_markup=None)
    await context.bot.send_message(chat_id=user_id, text=t("time_confirmed", lang, time=time_str))

    if is_first_time:
        # 6) أيام الإجازة
        await _send_vacation_day_picker(context.bot, user_id, lang, step=1)
    else:
        # تعديل لاحق عبر /settings: فعّلي إرسال اليوم فورًا إن كان مناسبًا
        starts_today = trigger_first_lesson_if_today(context.job_queue, user_id, hour, minute)
        if starts_today:
            await context.bot.send_message(chat_id=user_id, text=t("lesson_starting_today", lang))
        else:
            await context.bot.send_message(chat_id=user_id, text=t("lesson_starting_next_study_day", lang))


# ---------------------------------------------------------------------------
# 6) أيام الإجازة (اختيار حر ليومين)
# ---------------------------------------------------------------------------

async def _send_vacation_day_picker(bot, user_id: int, lang: str, step: int, exclude: int = None):
    rows = vacation_day_keyboard_rows(lang, exclude=exclude)
    buttons = [[InlineKeyboardButton(label, callback_data=cb)] for label, cb in rows]
    keyboard = InlineKeyboardMarkup(buttons)

    if step == 1:
        text = t("ask_vacation_days", lang)
    else:
        day1_name = weekday_name(exclude, lang)
        text = t("vacation_day_selected", lang, day=day1_name)

    await bot.send_message(chat_id=user_id, text=text, reply_markup=keyboard)


async def handle_vacation_day_choice(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    user_id = query.from_user.id
    day_num = int(query.data.split("|")[1])

    user = db.get_user(user_id)
    lang = user.get("language", "ar")
    was_already_set = user.get("vacation_day_1") is not None  # قبل هذا الاختيار -> يحدد أول مرة أم تعديل
    await query.edit_message_reply_markup(reply_markup=None)

    first_day_pending = context.user_data.get("pending_vacation_day_1")

    if first_day_pending is None:
        # هذا أول يوم يختاره الطالب الآن -> اطلب اليوم الثاني
        context.user_data["pending_vacation_day_1"] = day_num
        await _send_vacation_day_picker(context.bot, user_id, lang, step=2, exclude=day_num)
        return

    # هذا اليوم الثاني -> احفظ الاثنين معًا
    day1, day2 = first_day_pending, day_num
    context.user_data.pop("pending_vacation_day_1", None)

    db.set_vacation_days(user_id, day1, day2)

    # أعد جدولة الطالب بأيام الإجازة الجديدة (يشمل حالة أول تسجيل وحالة تعديل لاحق عبر /settings)
    time_str = user.get("lesson_time")
    if time_str:
        hour, minute = map(int, time_str.split(":"))
        schedule_daily_lesson(context.job_queue, user_id, hour, minute)

    day1_name = weekday_name(day1, lang)
    day2_name = weekday_name(day2, lang)
    await context.bot.send_message(
        chat_id=user_id, text=t("vacation_days_confirmed", lang, day1=day1_name, day2=day2_name),
    )

    if not was_already_set:
        # 7) الملخص الشامل (فقط عند إتمام التسجيل لأول مرة، وليس عند تعديل لاحق عبر /settings)
        await _send_summary(context.bot, user_id, lang)


# ---------------------------------------------------------------------------
# 7) الملخص الشامل
# ---------------------------------------------------------------------------

async def _send_summary(bot, user_id: int, lang: str):
    user = db.get_user(user_id)
    if not user:
        return

    name = user.get("first_name") or user.get("username") or "-"
    level = user.get("level", "-")
    time_str = user.get("lesson_time", "-")
    day1 = weekday_name(user.get("vacation_day_1"), lang) if user.get("vacation_day_1") is not None else "-"
    day2 = weekday_name(user.get("vacation_day_2"), lang) if user.get("vacation_day_2") is not None else "-"
    vacation = f"{day1}, {day2}"
    group = user.get("group_link", "-")

    body = t(
        "summary_body", lang,
        name=name, level=level, time=time_str, vacation=vacation, group=group,
    )
    text = f"{t('summary_title', lang)}\n\n{body}\n\n{t('summary_edit_hint', lang)}"
    await bot.send_message(chat_id=user_id, text=text)


# ---------------------------------------------------------------------------
# /progress
# ---------------------------------------------------------------------------

async def progress_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    user = db.get_user(user_id)
    if not user or not user.get("level"):
        await update.message.reply_text(t("no_active_program", user.get("language", "ar") if user else "ar"))
        return
    lang = user.get("language", "ar")
    level = user["level"]
    total = db.total_lessons_for_level(level)
    text = f"{t('progress_title', lang)}\n\n" + t(
        "progress_body", lang,
        level=level, completed=user.get("completed_lessons", 0), total=total,
        current=user.get("current_lesson", 1),
    )
    await update.message.reply_text(text)


# ---------------------------------------------------------------------------
# /settings — تعديل أي عنصر في أي وقت
# ---------------------------------------------------------------------------

async def settings_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    user = db.get_user(user_id)
    lang = user.get("language", "ar") if user else "ar"

    keyboard = InlineKeyboardMarkup([
        [InlineKeyboardButton(t("settings_change_language", lang), callback_data="settings|lang")],
        [InlineKeyboardButton(t("settings_change_level", lang), callback_data="settings|level")],
        [InlineKeyboardButton(t("settings_change_gender", lang), callback_data="settings|gender")],
        [InlineKeyboardButton(t("settings_change_time", lang), callback_data="settings|time")],
        [InlineKeyboardButton(t("settings_change_vacation", lang), callback_data="settings|vacation")],
        [InlineKeyboardButton(t("settings_view_summary", lang), callback_data="settings|summary")],
    ])
    await update.message.reply_text(t("settings_title", lang), reply_markup=keyboard)


async def handle_settings_choice(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    user_id = query.from_user.id
    user = db.get_user(user_id)
    lang = user.get("language", "ar") if user else "ar"

    choice = query.data.split("|")[1]
    await query.edit_message_reply_markup(reply_markup=None)

    # كل مسارات التعديل من /settings تُعامَل كـ "ليست أول مرة"، فلا تُشغّل بقية سلسلة
    # التسجيل التلقائية بعد الحفظ (تلك السلاسل تعتمد على is_first_time المبني على
    # الحقل التالي في التسلسل كونه فارغًا، وهو غير فارغ هنا لأن التسجيل مكتمل أصلاً)
    if choice == "lang":
        from translations import language_keyboard_rows as _lang_rows
        rows = _lang_rows()
        keyboard = InlineKeyboardMarkup([[InlineKeyboardButton(label, callback_data=cb)] for label, cb in rows])
        await context.bot.send_message(chat_id=user_id, text=t("choose_language", lang), reply_markup=keyboard)
    elif choice == "level":
        await _send_level_picker(context.bot, user_id, lang)
    elif choice == "gender":
        await _send_gender_picker(context.bot, user_id, lang)
    elif choice == "time":
        await _send_time_picker(context.bot, user_id, lang)
    elif choice == "vacation":
        context.user_data.pop("pending_vacation_day_1", None)
        await _send_vacation_day_picker(context.bot, user_id, lang, step=1)
    elif choice == "summary":
        await _send_summary(context.bot, user_id, lang)


# ---------------------------------------------------------------------------
# استقبال ردود المحادثة (صوت) والكتابة (نص) لتصحيحها بالذكاء الاصطناعي
# ---------------------------------------------------------------------------

async def handle_text_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    user = db.get_user(user_id)
    if not user:
        return

    active_skill = get_active_ai_skill(user_id)
    if active_skill is None:
        return  # لا مهارة AI نشطة بانتظار رد؛ نتجاهل الرسالة بصمت

    await handle_ai_answer(context, user_id, active_skill, student_text=update.message.text)
    await check_and_complete_if_ready(context, user_id)


async def handle_voice_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    user = db.get_user(user_id)
    if not user:
        return

    active_skill = get_active_ai_skill(user_id)
    if active_skill is None:
        return

    try:
        voice_file = await context.bot.get_file(update.message.voice.file_id)
        audio_bytes = await voice_file.download_as_bytearray()
        await handle_ai_answer(context, user_id, active_skill, audio_bytes=bytes(audio_bytes))
    except Exception:
        logger.exception("فشل تحميل الرسالة الصوتية")
        lang = user.get("language", "ar")
        await update.message.reply_text(t("ai_correction_unavailable", lang))
        return

    await check_and_complete_if_ready(context, user_id)


async def handle_answer_callback_and_check(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await handle_answer_callback(update, context)
    user_id = update.callback_query.from_user.id
    await check_and_complete_if_ready(context, user_id)


# ---------------------------------------------------------------------------
# /export — أمر إداري محصور على ADMIN_USER_IDS فقط: يرسل ملف Excel بكل بيانات الطلاب
# ---------------------------------------------------------------------------

async def export_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    if user_id not in ADMIN_USER_IDS:
        return  # لا رد إطلاقًا لغير المخوَّلين، حتى لا يُعرَف أن الأمر موجود أصلاً

    file_path = generate_students_excel()
    with open(file_path, "rb") as f:
        await context.bot.send_document(
            chat_id=user_id, document=f, filename=os.path.basename(file_path),
            caption="📊 بيانات كل الطلاب المسجَّلين حاليًا في نور بوت",
        )


# ---------------------------------------------------------------------------
# اختبار يدوي (مفيد أثناء التطوير فقط)
# ---------------------------------------------------------------------------

async def force_lesson(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    user = db.get_user(user_id)
    if not user or not user.get("level"):
        await update.message.reply_text(t("no_active_program", user.get("language", "ar") if user else "ar"))
        return
    await send_lesson(
        context.bot, user_id, user.get("language", "ar"), user["level"], user["current_lesson"], context,
    )


# ---------------------------------------------------------------------------
# معالج أخطاء عام
# ---------------------------------------------------------------------------

async def error_handler(update: object, context: ContextTypes.DEFAULT_TYPE):
    logger.error("خطأ غير متوقع أثناء معالجة تحديث", exc_info=context.error)


# ---------------------------------------------------------------------------
# التشغيل
# ---------------------------------------------------------------------------

def main():
    if not BOT_TOKEN:
        raise RuntimeError("يجب تعيين TELEGRAM_BOT_TOKEN في متغيرات البيئة.")

    db.init_db()

    # سيرفر صحة داخلي بسيط — مطلوب فقط لأن الاستضافة على Render Web Service (وليس
    # Background Worker)، والتي تحتاج منفذ HTTP يرد على فحوصاتها الدورية. لا يؤثر
    # على منطق البوت نفسه بأي شكل.
    start_health_server(HEALTH_CHECK_PORT)

    app = Application.builder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("progress", progress_command))
    app.add_handler(CommandHandler("settings", settings_command))
    app.add_handler(CommandHandler("export", export_command))  # إداري فقط، محصور على ADMIN_USER_IDS
    app.add_handler(CommandHandler("lesson", force_lesson))  # للاختبار فقط

    app.add_handler(CallbackQueryHandler(handle_language_choice, pattern=r"^lang\|"))
    app.add_handler(CallbackQueryHandler(handle_level_choice, pattern=r"^level\|"))
    app.add_handler(CallbackQueryHandler(handle_gender_choice, pattern=r"^gender\|"))
    app.add_handler(CallbackQueryHandler(handle_time_choice, pattern=r"^time\|"))
    app.add_handler(CallbackQueryHandler(handle_vacation_day_choice, pattern=r"^vacday\|"))
    app.add_handler(CallbackQueryHandler(handle_settings_choice, pattern=r"^settings\|"))
    app.add_handler(CallbackQueryHandler(handle_answer_callback_and_check, pattern=r"^ans\|"))

    app.add_handler(MessageHandler(filters.VOICE, handle_voice_message))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_text_message))

    app.add_error_handler(error_handler)

    restore_all_schedules(app.job_queue)

    logger.info("نور بوت يعمل الآن...")
    app.run_polling()


if __name__ == "__main__":
    main()
