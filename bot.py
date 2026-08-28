# -*- coding: utf-8 -*-
"""
bot.py
نقطة تشغيل بوت "نور بوت" لتعليم اللغة العربية لغير الناطقين بها.

تدفق الاستخدام:
1. /start -> اختيار اللغة (عربي / تركي / إنجليزي) عبر أزرار Inline.
2. رسالة ترحيب + معلومات الأسبوع التجريبي.
3. طلب الوقت المناسب لإرسال الدرس اليومي (نص بصيغة HH:MM).
4. جدولة إرسال أول درس اليوم أو غدًا حسب الوقت، ثم يوميًا بعد ذلك
   (باستثناء الجمعة والسبت).
5. كل درس يُرسل خطوة (مهارة) كل عدة دقائق تلقائيًا عبر lesson_engine.py.
6. إجابات الاختيار من متعدد تُصحَّح فورًا عبر أزرار Inline.
7. إجابات المحادثة (صوت) والكتابة (نص) تُحفظ لتصحيح يدوي/AI لاحقًا.

التشغيل:
    export TELEGRAM_BOT_TOKEN="8629063079:AAHvPGBfbTdCJyHXz2EpHWzPiG8KfgroMMo"
    export GEMINI_API_KEY="iXp2hUjxXlJmdVc_xwTT7DEpVb1b1MqUJOSi-lQ"        # اختياري إن لم تُستخدم دوال ai_correction بعد
    python bot.py
"""

import os
import re
import logging

from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    Application,
    CommandHandler,
    CallbackQueryHandler,
    MessageHandler,
    ContextTypes,
    filters,
)

import database as db
from translations import t
from scheduler import schedule_daily_lesson, restore_all_schedules
from lesson_engine import handle_answer_callback, start_lesson_for_user

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)
logger = logging.getLogger(__name__)

BOT_TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN")
TIME_PATTERN = re.compile(r"^([01]?\d|2[0-3]):([0-5]\d)$")


# ---------------------------------------------------------------------------
# /start و اختيار اللغة
# ---------------------------------------------------------------------------

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    db.create_user_if_missing(user_id)

    keyboard = InlineKeyboardMarkup([
        [InlineKeyboardButton("🇸🇦 العربية", callback_data="lang|ar")],
        [InlineKeyboardButton("🇹🇷 Türkçe", callback_data="lang|tr")],
        [InlineKeyboardButton("🇬🇧 English", callback_data="lang|en")],
    ])
    await update.message.reply_text(t("choose_language", "ar"), reply_markup=keyboard)


async def handle_language_choice(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    user_id = query.from_user.id
    lang = query.data.split("|")[1]
    db.set_language(user_id, lang)

    await query.edit_message_reply_markup(reply_markup=None)
    await context.bot.send_message(chat_id=user_id, text=t("welcome", lang))
    await context.bot.send_message(chat_id=user_id, text=t("trial_info", lang))
    await context.bot.send_message(chat_id=user_id, text=t("ask_time", lang))


# ---------------------------------------------------------------------------
# استقبال الوقت المناسب للدرس اليومي
# ---------------------------------------------------------------------------

async def handle_text_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """يلتقط أي رسالة نصية عادية: أولاً يحاول تفسيرها كوقت (إن لم يكن الوقت محددًا بعد)،
    وإلا يعاملها كإجابة كتابة (writing) بانتظار التصحيح."""
    user_id = update.effective_user.id
    user = db.get_user(user_id)
    if not user:
        db.create_user_if_missing(user_id)
        user = db.get_user(user_id)

    lang = user.get("lang", "ar")
    text = update.message.text.strip()

    if not user.get("lesson_time"):
        match = TIME_PATTERN.match(text)
        if not match:
            await update.message.reply_text(t("invalid_time", lang))
            return

        hour, minute = int(match.group(1)), int(match.group(2))
        db.set_lesson_time(user_id, f"{hour:02d}:{minute:02d}")
        schedule_daily_lesson(context.job_queue, user_id, hour, minute)

        await update.message.reply_text(t("time_confirmed", lang, time=f"{hour:02d}:{minute:02d}"))

        # تحديد ما إذا كان الدرس الأول يبدأ اليوم أو غدًا
        from datetime import datetime
        now = datetime.now()
        today_target = now.replace(hour=hour, minute=minute, second=0, microsecond=0)
        if today_target > now and now.weekday() not in (4, 5):
            await update.message.reply_text(t("lesson_starting_today", lang))
        else:
            await update.message.reply_text(t("lesson_starting_tomorrow", lang))
        return

    # المستخدم لديه وقت مُحدد بالفعل -> هذه رسالة إجابة كتابة (writing)، تُحفظ للتصحيح
    # TODO: ربطها بـ ai_correction.correct_writing() أو بتحويلها لقناة مراجعة يدوية
    await update.message.reply_text(t("correct_answer", lang))


async def handle_voice_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """يلتقط الرسائل الصوتية (إجابات المحادثة speaking) لتصحيحها لاحقًا يدويًا/AI."""
    user_id = update.effective_user.id
    user = db.get_user(user_id)
    lang = user.get("lang", "ar") if user else "ar"

    # TODO: تحميل الملف الصوتي عبر context.bot.get_file(update.message.voice.file_id)
    # ثم تمريره لـ ai_correction.correct_speaking(), أو حفظه لمراجعة يدوية من سندس.
    await update.message.reply_text(t("correct_answer", lang))


# ---------------------------------------------------------------------------
# أمر لبدء درس يدويًا فورًا (اختبار)
# ---------------------------------------------------------------------------

async def force_lesson(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """أمر /lesson لبدء الدرس التالي فورًا يدويًا، مفيد للاختبار."""
    user_id = update.effective_user.id
    await start_lesson_for_user(context, user_id)


# ---------------------------------------------------------------------------
# التشغيل
# ---------------------------------------------------------------------------

def main():
    if not BOT_TOKEN:
        raise RuntimeError("يجب تعيين متغيّر البيئة TELEGRAM_BOT_TOKEN قبل التشغيل.")

    db.init_db()

    app = Application.builder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("lesson", force_lesson))
    app.add_handler(CallbackQueryHandler(handle_language_choice, pattern=r"^lang\|"))
    app.add_handler(CallbackQueryHandler(handle_answer_callback, pattern=r"^ans\|"))
    app.add_handler(MessageHandler(filters.VOICE, handle_voice_message))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_text_message))

    # استعادة جدولة كل المستخدمين المسجلين سابقًا عند إعادة تشغيل البوت
    restore_all_schedules(app.job_queue)

    logger.info("نور بوت يعمل الآن...")
    app.run_polling()


if __name__ == "__main__":
    main()
