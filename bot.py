# -*- coding: utf-8 -*-
"""
bot.py
الملف الرئيسي لتشغيل بوت تيليجرام لإدارة رحلة تعلم اللغة العربية.
يدعم تعدد اللغات، واختار أيام الإجازة المخصصة، وتوجيه الطلاب لقروبات الدردشة.
"""

import logging
import os
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    CallbackQueryHandler,
    ContextTypes,
)

import database as db
import config
from scheduler import schedule_daily_lesson, restore_all_schedules
from translations import t, language_codes, language_keyboard_rows, get_days_list

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)


async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    db.create_user_if_missing(user.id, user.username, user.first_name)
    
    # رسالة ترحيبية واختيار اللغة
    keyboard = InlineKeyboardMarkup(language_keyboard_rows())
    welcome_text = (
        "مرحباً بك في أكاديمية نور لتعليم اللغة العربية 🌙📖\n"
        "Welcome to Nour Arabic Academy!\n\n"
        "الرجاء اختيار لغتك المفضلة / Please select your preferred language:"
    )
    await update.message.reply_text(welcome_text, reply_markup=keyboard)


async def handle_language_choice(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    
    data = query.data
    if not data.startswith("lang|"):
        return
        
    lang_code = data.split("|")[1]
    if lang_code not in language_codes():
        return
        
    user_id = query.from_user.id
    db.set_language(user_id, lang_code)
    
    msg = "✅ تم حفظ لغتك بنجاح." if lang_code == "ar" else "✅ Language saved successfully."
    await query.edit_message_text(text=msg)
    
    # الخطوة التالية: اختيار الجنس أولاً لتوجيهه للقروب المناسب
    await _send_gender_picker(context.bot, user_id, lang_code)


async def _send_gender_picker(bot, user_id: int, lang: str):
    keyboard = InlineKeyboardMarkup([
        [InlineKeyboardButton(t("btn_male", lang), callback_data="gender|male")],
        [InlineKeyboardButton(t("btn_female", lang), callback_data="gender|female")]
    ])
    msg_text = (
        "👤 يرجى اختيار الجنس (لتوجيهك إلى قروب الدردشة التحفيزي المناسب):" 
        if lang == "ar" 
        else "👤 Please select your gender to direct you to the appropriate motivational chat group:"
    )
    await bot.send_message(chat_id=user_id, text=msg_text, reply_markup=keyboard)


async def handle_gender_choice(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    
    user_id = query.from_user.id
    user = db.get_user(user_id)
    lang = user.get("language", "ar") if user else "ar"
    
    gender = query.data.split("|")[1]
    
    # تعيين معرف القروب بناءً على الجنس
    if gender == "male":
        group_id = -1004491283200
    else:
        group_id = -5548247537
        
    db.update_user_fields(user_id, gender=gender, group_id=group_id)
    
    msg = "✅ تم حفظ الجنس." if lang == "ar" else "✅ Gender saved."
    await query.edit_message_text(text=msg)
    
    # الخطوة التالية: اختيار أيام الإجازة بلغة الطالب
    await _send_rest_days_picker(context.bot, user_id, lang)


async def _send_rest_days_picker(bot, user_id: int, lang: str, selected=None):
    if selected is None:
        selected = []
        context.user_data["temp_rest_days"] = selected
        
    localized_days = get_days_list(lang) # أسماء الأيام مترجمة (الأحد إلى السبت)
    codes = ["Sun", "Mon", "Tue", "Wed", "Thu", "Fri", "Sat"]
    
    keyboard_rows = []
    for code, label in zip(codes, localized_days):
        check = "✅ " if code in selected else "⬜ "
        keyboard_rows.append([InlineKeyboardButton(f"{check} {label}", callback_data=f"rest|toggle|{code}")])
        
    keyboard_rows.append([InlineKeyboardButton(t("btn_save_rest_days", lang), callback_data="rest|save")])
    keyboard = InlineKeyboardMarkup(keyboard_rows)
    
    msg_text = (
        "🗓️ اختر يومي إجازة في الأسبوع (لن يتم إرسال دروس فيهما):\n(اضغط على اليوم لتحديده أو إلغائه، ثم اضغط حفظ)" 
        if lang == "ar" 
        else "🗓️ Choose your 2 rest days per week where no lessons will be sent:\n(Tap to select/deselect, then click save)"
    )
    await bot.send_message(chat_id=user_id, text=msg_text, reply_markup=keyboard)


async def handle_rest_days_choice(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    
    user_id = query.from_user.id
    user = db.get_user(user_id)
    lang = user.get("language", "ar") if user else "ar"
    
    data_parts = query.data.split("|")
    action = data_parts[1]
    
    if "temp_rest_days" not in context.user_data:
        context.user_data["temp_rest_days"] = []
        
    selected = context.user_data["temp_rest_days"]
    
    if action == "toggle":
        code = data_parts[2]
        if code in selected:
            selected.remove(code)
        else:
            if len(selected) < 2:
                selected.append(code)
            else:
                alert_text = (
                    "يمكنك اختيار يومي إجازة فقط كحد أقصى." 
                    if lang == "ar" 
                    else "You can select a maximum of 2 rest days."
                )
                await query.answer(alert_text, show_alert=True)
                return
                
        localized_days = get_days_list(lang)
        codes = ["Sun", "Mon", "Tue", "Wed", "Thu", "Fri", "Sat"]
        
        keyboard_rows = []
        for code_item, label in zip(codes, localized_days):
            check = "✅ " if code_item in selected else "⬜ "
            keyboard_rows.append([InlineKeyboardButton(f"{check} {label}", callback_data=f"rest|toggle|{code_item}")])
        keyboard_rows.append([InlineKeyboardButton(t("btn_save_rest_days", lang), callback_data="rest|save")])
        
        try:
            await query.edit_message_reply_markup(reply_markup=InlineKeyboardMarkup(keyboard_rows))
        except Exception:
            pass
            
    elif action == "save":
        if len(selected) != 2:
            alert_text = (
                "الرجاء اختيار يومي إجازة بالضبط قبل الحفظ." 
                if lang == "ar" 
                else "Please select exactly 2 rest days before saving."
            )
            await query.answer(alert_text, show_alert=True)
            return
            
        rest_days_str = ",".join(selected)
        db.update_user_fields(user_id, rest_days=rest_days_str)
        
        msg = "✅ تم حفظ أيام الإجازة." if lang == "ar" else "✅ Rest days saved."
        await query.edit_message_text(text=msg)
        
        # الخطوة التالية: اختيار وقت الدرس اليومي
        await _send_time_picker(context.bot, user_id, lang)


async def _send_time_picker(bot, user_id: int, lang: str):
    keyboard_rows = []
    row = []
    for time_str in config.AVAILABLE_TIMES:
        row.append(InlineKeyboardButton(time_str, callback_data=f"time|{time_str}"))
        if len(row) == 3:
            keyboard_rows.append(row)
            row = []
    if row:
        keyboard_rows.append(row)
        
    keyboard = InlineKeyboardMarkup(keyboard_rows)
    msg_text = (
        "⏰ اختر الوقت المناسب لوصول درسك اليومي:" 
        if lang == "ar" 
        else "⏰ Choose the time you'd like your daily lesson to arrive:"
    )
    await bot.send_message(chat_id=user_id, text=msg_text, reply_markup=keyboard)


async def handle_time_choice(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    
    user_id = query.from_user.id
    user = db.get_user(user_id)
    lang = user.get("language", "ar") if user else "ar"
    
    time_str = query.data.split("|")[1]
    db.set_lesson_time(user_id, time_str)
    
    try:
        hour, minute = map(int, time_str.split(":"))
        schedule_daily_lesson(context.job_queue, user_id, hour, minute)
    except Exception as e:
        logger.error(f"خطأ في جدولة الوقت للمستخدم {user_id}: {e}")
        
    # جلب معلومات المستخدم لإظهار ملخص التسجيل وقروب الدردشة التحفيزي الخاص به
    updated_user = db.get_user(user_id)
    name = updated_user.get("first_name", "Student")
    level = updated_user.get("level", "A1")
    rest_days = updated_user.get("rest_days", "")
    
    # تحديد رابط قروب الدردشة التحفيزي بناءً على القروب المختار
    group_id = updated_user.get("group_id")
    if group_id == -1004491283200:
        chat_link = "https://t.me/+YourMenGroupInviteLink"  # استبدله برابط دعوة قروب الرجال إذا أردت
    else:
        chat_link = "https://t.me/+YourWomenGroupInviteLink"  # استبدله برابط دعوة قروب النساء إذا أردت

    summary_text = t("registration_summary", lang).format(
        name=name,
        level=level,
        time=time_str,
        rest_days=rest_days,
        chat_link=chat_link
    )
    
    await query.edit_message_text(text=summary_text, disable_web_page_preview=True)


def main():
    token = os.environ.get("TELEGRAM_BOT_TOKEN")
    if not token:
        logger.error("لم يتم العثور على توكن البوت TELEGRAM_BOT_TOKEN في متغيرات البيئة!")
        return
        
    db.init_db()
    
    application = ApplicationBuilder().token(token).build()
    
    application.add_handler(CommandHandler("start", start_command))
    application.add_handler(CallbackQueryHandler(handle_language_choice, pattern="^lang\\|"))
    application.add_handler(CallbackQueryHandler(handle_gender_choice, pattern="^gender\\|"))
    application.add_handler(CallbackQueryHandler(handle_rest_days_choice, pattern="^rest\\|"))
    application.add_handler(CallbackQueryHandler(handle_time_choice, pattern="^time\\|"))
    
    # استعادة الجدولة السابقة عند الإقلاع
    restore_all_schedules(application.job_queue)
    
    PORT = int(os.environ.get("PORT", "8443"))
    RENDER_EXTERNAL_URL = os.environ.get("RENDER_EXTERNAL_URL")
    
    logger.info("البوت يعمل الآن بنظام الـ Webhook...")
    
    if RENDER_EXTERNAL_URL:
        application.run_webhook(
            listen="0.0.0.0",
            port=PORT,
            url_path=token,
            webhook_url=f"{RENDER_EXTERNAL_URL}/{token}"
        )
    else:
        application.run_polling()


if __name__ == "__main__":
    main()
