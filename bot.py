# -*- coding: utf-8 -*-
"""
bot.py
نقطة التشغيل الرئيسية لـ "نور بوت". مسؤول فقط عن:
    Telegram، المستخدمين، الإعدادات، الجدولة، التقدّم، الاشتراك، واستدعاء الدروس.
لا يحتوي محتوى أي درس — كل درس في ملفه lessonN.py المستقل.

التسلسل:
    /start -> اختيار اللغة -> ترحيب -> اختيار وقت الدرس -> جدولة -> إرسال تلقائي يومي
"""

import os
import logging
import threading
from flask import Flask

from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    Application, CommandHandler, CallbackQueryHandler, MessageHandler,
    ContextTypes, filters,
)

import database as db
from translations import t, language_keyboard_rows, SUPPORTED_LANGUAGES
from config import AVAILABLE_TIMES
from scheduler import schedule_daily_lesson, restore_all_schedules, next_study_moment_is_today
from lesson_engine import (
    handle_answer_callback, handle_ai_answer, get_active_ai_skill,
    check_and_complete_if_ready, send_lesson,
)

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)
logger = logging.getLogger(__name__)

BOT_TOKEN = os.environ.get("BOT_TOKEN")

# ---------------------------------------------------------------------------
# خادم Flask مصغر لتلبية متطلبات منصة Render وتشغيل الخدمة مجاناً
# ---------------------------------------------------------------------------
app_flask = Flask(__name__)

@app_flask.route('/')
def home():
    return "Nuur Bot is running!"

def run_flask():
    port = int(os.environ.get("PORT", 10000))
    app_flask.run(host="0.0.0.0", port=port)


# ---------------------------------------------------------------------------
# /start
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
    is_settings_change = user.get("lesson_time") is not None

    await context.bot.send_message(chat_id=user_id, text=t("language_changed", lang))

    if not is_settings_change:
        await context.bot.send_message(chat_id=user_id, text=t("welcome", lang))
        await context.bot.send_message(chat_id=user_id, text=t("trial_info", lang))
        await _send_time_picker(context.bot, user_id, lang)


async def _send_time_picker(bot, user_id: int, lang: str):
    buttons = [InlineKeyboardButton(time_str, callback_data=f"time|{time_str}") for time_str in AVAILABLE_TIMES]
    rows = [buttons[i:i + 3] for i in range(0, len(buttons), 3)]
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

    db.set_lesson_time(user_id, time_str)
    schedule_daily_lesson(context.job_queue, user_id, hour, minute)

    await query.edit_message_reply_markup(reply_markup=None)
    await context.bot.send_message(chat_id=user_id, text=t("time_confirmed", lang, time=time_str))

    if next_study_moment_is_today(hour, minute):
        await context.bot.send_message(chat_id=user_id, text=t("lesson_starting_today", lang))
    else:
        await context.bot.send_message(chat_id=user_id, text=t("lesson_starting_next_study_day", lang))


# ---------------------------------------------------------------------------
# /progress
# ---------------------------------------------------------------------------

async def progress_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    user = db.get_user(user_id)
    if not user:
        await update.message.reply_text(t("no_active_program"))
        return
    lang = user.get("language", "ar")
    text = f"{t('progress_title', lang)}\n\n" + t(
        "progress_body", lang,
        completed=user.get("completed_lessons", 0),
        current=user.get("current_lesson", 1),
    )
    await update.message.reply_text(text)


# ---------------------------------------------------------------------------
# /settings
# ---------------------------------------------------------------------------

async def settings_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    user = db.get_user(user_id)
    lang = user.get("language", "ar") if user else "ar"

    keyboard = InlineKeyboardMarkup([
        [InlineKeyboardButton(t("settings_change_language", lang), callback_data="settings|lang")],
        [InlineKeyboardButton(t("settings_change_time", lang), callback_data="settings|time")],
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

    if choice == "lang":
        rows = language_keyboard_rows()
        keyboard = InlineKeyboardMarkup([[InlineKeyboardButton(label, callback_data=cb)] for label, cb in rows])
        await context.bot.send_message(chat_id=user_id, text=t("choose_language", lang), reply_markup=keyboard)
    elif choice == "time":
        await _send_time_picker(context.bot, user_id, lang)


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
# اختبار يدوي (مفيد أثناء التطوير فقط)
# ---------------------------------------------------------------------------

async def force_lesson(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    user = db.get_user(user_id)
    if not user:
        await update.message.reply_text(t("no_active_program"))
        return
    await send_lesson(context.bot, user_id, user.get("language", "ar"), user["current_lesson"], context)


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

    # تشغيل خادم Flask في خلفية مستقلة لفتح المنفذ المطلوب لـ Render
    threading.Thread(target=run_flask, daemon=True).start()

    db.init_db()

    app = Application.builder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("progress", progress_command))
    app.add_handler(CommandHandler("settings", settings_command))
    app.add_handler(CommandHandler("lesson", force_lesson))  # للاختبار فقط

    app.add_handler(CallbackQueryHandler(handle_language_choice, pattern=r"^lang\|"))
    app.add_handler(CallbackQueryHandler(handle_time_choice, pattern=r"^time\|"))
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
