# -*- coding: utf-8 -*-
"""
bot.py
نقطة التشغيل الرئيسية لـ "نور بوت".
"""

import os
import logging
import threading
from flask import Flask

from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, InputFile
from telegram.ext import (
    Application, CommandHandler, CallbackQueryHandler, MessageHandler,
    ContextTypes, filters,
)

import database as db
from translations import t, language_keyboard_rows
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

# رابط Tribute الخاص بك للاشتراك
TRIBUTE_PAYMENT_LINK = "https://t.me/tribute/app?startapp=s152f"

# عدد الدروس المجانية المسموحة قبل طلب الاشتراك (ضبطت على 5 دروس)
TRIAL_LIMIT = 5 

app_flask = Flask(__name__)

@app_flask.route('/')
def home():
    return "Nuur Bot is running!"

def run_flask():
    port = int(os.environ.get("PORT", 10000))
    app_flask.run(host="0.0.0.0", port=port)


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
        # 1. رسالة الترحيب
        await context.bot.send_message(chat_id=user_id, text=t("welcome", lang))
        # 2. رسالة التعريف عن المستويات والدروس والاشتراك
        await context.bot.send_message(chat_id=user_id, text=t("intro_levels_info", lang))
        # 3. إرسال خيارات تحديد المستوى أو البدء من A0
        await _send_level_selection(context.bot, user_id, lang)


async def _send_level_selection(bot, user_id: int, lang: str):
    keyboard = InlineKeyboardMarkup([
        # ربط زر اختبار تحديد المستوى بالبوت الخارجي المخصص للاختبار
        [InlineKeyboardButton(t("btn_take_placement_test", lang), url="https://t.me/Nurarabictestbot")],
        [
            InlineKeyboardButton("A0", callback_data="level|A0"),
            InlineKeyboardButton("A1", callback_data="level|A1"),
            InlineKeyboardButton("A2", callback_data="level|A2"),
        ],
        [
            InlineKeyboardButton("B1", callback_data="level|B1"),
            InlineKeyboardButton("B2", callback_data="level|B2"),
        ]
    ])
    await bot.send_message(chat_id=user_id, text=t("ask_level_selection", lang), reply_markup=keyboard)


async def handle_level_choice(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    user_id = query.from_user.id
    user = db.get_user(user_id)
    lang = user.get("language", "ar") if user else "ar"

    choice = query.data.split("|")[1]
    await query.edit_message_reply_markup(reply_markup=None)

    # حفظ المستوى المختار (A0, A1, A2, B1, B2)
    if hasattr(db, "set_user_level"):
        db.set_user_level(user_id, choice)
        
    await context.bot.send_message(chat_id=user_id, text=t("level_chosen", lang, level=choice))
    # الانتقال لاختيار وقت الدراسة اليومي
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


async def send_subscription_prompt(chat_id, context, lang="ar"):
    btn_subscribe = "💳 اشترك عبر Tribute" if lang != "tr" else "💳 Tribute ile Abone Ol"
    btn_check = "🔄 تحقق من الاشتراك" if lang != "tr" else "🔄 Aboneliği Kontrol Et"
    
    keyboard = [
        [InlineKeyboardButton(btn_subscribe, url=TRIBUTE_PAYMENT_LINK)],
        [InlineKeyboardButton(btn_check, callback_data="check_subscription")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    text = t("paywall_tribute", lang)
    await context.bot.send_message(chat_id=chat_id, text=text, reply_markup=reply_markup)


async def stats_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    all_users = db.get_all_users() if hasattr(db, "get_all_users") else {}
    if not all_users:
        await update.message.reply_text("📊 نظام الإحصائيات جاهز، ولكن لا يوجد مستخدمين مسجلين بعد.")
        return

    stats_msg = f"📊 **قائمة بيانات الطلاب المسجلين (الإجمالي: {len(all_users)}):**\n\n"
    for uid, udata in all_users.items():
        sub_status = udata.get("subscription_status", "trial")
        status_label = "مدفوع ⭐" if sub_status == "active" else "مجاني / تجريبي 🆓"
        stats_msg += f"• الطالب: [{udata.get('first_name', 'طالب')}](tg://user?id={uid})\n"
        stats_msg += f"  - اللغة: `{udata.get('language', 'ar')}`\n"
        stats_msg += f"  - الدروس المكتملة: {udata.get('completed_lessons', 0)}\n"
        stats_msg += f"  - الحالة: {status_label}\n\n"

    await update.message.reply_text(stats_msg, parse_mode="Markdown")


async def download_excel_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    excel_path = os.path.join(os.path.dirname(__file__), "students_data.xlsx")
    if os.path.exists(excel_path):
        with open(excel_path, "rb") as f:
            await update.message.reply_document(document=InputFile(f, filename="students_data.xlsx"), caption="📊 ملف بيانات الطلاب المحدث.")
    else:
        await update.message.reply_text("⚠️ ملف بيانات الطلاب غير موجود بعد.")


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


async def handle_text_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    user = db.get_user(user_id)
    if not user:
        return

    lang = user.get("language", "ar")
    completed = user.get("completed_lessons", 0)
    sub_status = user.get("subscription_status", "trial")
    
    if completed >= TRIAL_LIMIT and sub_status != "active":
        await send_subscription_prompt(user_id, context, lang)
        return

    active_skill = get_active_ai_skill(user_id)
    if active_skill is None:
        msg = (
            "Lütfen şu anda serbest metin göndermeyin; aktif bir alıştırma veya ders adımı bekleniyor."
            if lang == "tr" else
            "⚠️ عذراً، لا يوجد تمرين كتابة نشط حالياً لاستقبال إجابتك. يرجى انتظار سؤال الدرس أو استخدام الأزرار المتاحة."
        )
        await update.message.reply_text(msg)
        return

    await handle_ai_answer(context, user_id, active_skill, student_text=update.message.text)
    await check_and_complete_if_ready(context, user_id)


async def handle_voice_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    user = db.get_user(user_id)
    if not user:
        return

    lang = user.get("language", "ar")
    completed = user.get("completed_lessons", 0)
    sub_status = user.get("subscription_status", "trial")
    
    if completed >= TRIAL_LIMIT and sub_status != "active":
        await send_subscription_prompt(user_id, context, lang)
        return

    active_skill = get_active_ai_skill(user_id)
    if active_skill is None:
        await update.message.reply_text("⚠️ تنبيه: لا توجد مهارة محادثة نشطة حالياً لهذه الخطوة.")
        return

    await update.message.reply_text("🎙️ جاري استماع وتحليل الصوت...")

    try:
        msg_file = update.message.voice or update.message.audio
        voice_file = await context.bot.get_file(msg_file.file_id)
        audio_bytes = await voice_file.download_as_bytearray()
        await handle_ai_answer(context, user_id, active_skill, audio_bytes=bytes(audio_bytes))
    except Exception as e:
        logger.exception("فشل تحميل الرسالة الصوتية")
        await update.message.reply_text(f"خطأ تقني في تحميل الصوت: {e}")
        return

    await check_and_complete_if_ready(context, user_id)


async def handle_answer_callback_and_check(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    user_id = query.from_user.id
    user = db.get_user(user_id)
    lang = user.get("language", "ar") if user else "ar"

    if query.data == "check_subscription":
        await query.answer()
        db.set_subscription_status(user_id, "active")
        success_msg = (
            "✅ Abonelik başarıyla doğrulandı! Hesabınız etkinleştirildi ve tüm derslerin kilidi açıldı."
            if lang == "tr" else
            "✅ تم التحقق من الاشتراك بنجاح! تم تفعيل حسابك وفتح كافة الدروس."
        )
        await query.message.reply_text(success_msg)
        return

    completed = user.get("completed_lessons", 0) if user else 0
    sub_status = user.get("subscription_status", "trial") if user else "trial"
    
    if completed >= TRIAL_LIMIT and sub_status != "active":
        await query.answer()
        await send_subscription_prompt(user_id, context, lang)
        return

    await handle_answer_callback(update, context)
    await check_and_complete_if_ready(context, user_id)


async def force_lesson(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    user = db.get_user(user_id)
    if not user:
        await update.message.reply_text(t("no_active_program"))
        return
    
    lang = user.get("language", "ar")
    completed = user.get("completed_lessons", 0)
    sub_status = user.get("subscription_status", "trial")
    
    if completed >= TRIAL_LIMIT and sub_status != "active":
        await send_subscription_prompt(user_id, context, lang)
        return

    await send_lesson(context.bot, user_id, lang, user["current_lesson"], context)


async def error_handler(update: object, context: ContextTypes.DEFAULT_TYPE):
    logger.error("خطأ غير متوقع أثناء معالجة تحديث", exc_info=context.error)


def main():
    if not BOT_TOKEN:
        raise RuntimeError("يجب تعيين TELEGRAM_BOT_TOKEN في متغيرات البيئة.")

    threading.Thread(target=run_flask, daemon=True).start()

    db.init_db()

    app = Application.builder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("progress", progress_command))
    app.add_handler(CommandHandler("settings", settings_command))
    app.add_handler(CommandHandler("lesson", force_lesson))
    app.add_handler(CommandHandler("stats", stats_command))
    app.add_handler(CommandHandler("excel", download_excel_command))

    app.add_handler(CallbackQueryHandler(handle_language_choice, pattern=r"^lang\|"))
    app.add_handler(CallbackQueryHandler(handle_level_choice, pattern=r"^level\|"))
    app.add_handler(CallbackQueryHandler(handle_time_choice, pattern=r"^time\|"))
    app.add_handler(CallbackQueryHandler(handle_settings_choice, pattern=r"^settings\|"))
    app.add_handler(CallbackQueryHandler(handle_answer_callback_and_check))

    app.add_handler(MessageHandler(filters.VOICE | filters.AUDIO, handle_voice_message))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_text_message))

    app.add_error_handler(error_handler)

    restore_all_schedules(app.job_queue)

    logger.info("نور بوت يعمل الآن...")
    app.run_polling()


if __name__ == "__main__":
    main()
