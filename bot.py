# -*- coding: utf-8 -*-
"""
bot.py
الملف الرئيسي لتشغيل بوت تيليجرام لإدارة رحلة تعلم اللغة العربية.
يدعم تعدد اللغات، واختيار أيام الإجازة المخصصة، وتخزين البيانات.
"""

import logging
import os
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    CallbackQueryHandler,
    ContextTypes,
    MessageHandler,
    filters,
)

import database as db
import config
from scheduler import schedule_daily_lesson, restore_all_schedules, remove_daily_lesson
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
        "مرحباً بك في أكاديمية نور لتعليم اللغة العربية!\n"
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
    
    # الانتقال لخطوة اختيار أيام الإجازة
    msg = "✅ تم حفظ لغتك بنجاح." if lang_code == "ar" else "✅ Language saved successfully."
    await query.edit_message_text(text=msg)
    await _send_rest_days_picker(context.bot, user_id, lang_code)


async def _send_rest_days_picker(bot, user_id: int, lang: str, selected=None):
    if selected is None:
        selected = []
        
    localized_days = get_days_list(lang)
    codes = ["Sun", "Mon", "Tue", "Wed", "Thu", "Fri", "Sat"]
    
    keyboard_rows = []
    for code, label in zip(codes, localized_days):
        check = "✅ " if code in selected else "⬜ "
        keyboard_rows.append([InlineKeyboardButton(check + label, callback_data=f"rest|toggle|{code}")])
        
    keyboard_rows.append([InlineKeyboardButton(t("btn_save_rest_days", lang), callback_data="rest|save")])
    keyboard = InlineKeyboardMarkup(keyboard_rows)
    
    msg_text = (
        "الرجاء اختيار يومي إجازة في الأسبوع بدون دروس:" 
        if lang == "ar" 
        else "Please choose your 2 rest days per week:"
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
            keyboard_rows.append([InlineKeyboardButton(check + label, callback_data=f"rest|toggle|{code_item}")])
        keyboard_rows.append([InlineKeyboardButton(t("btn_save_rest_days", lang), callback_data="rest|save")])
        
        try:
            await query.edit_message_reply_markup(reply_markup=InlineKeyboardMarkup(keyboard_rows))
        except Exception:
            pass
            
    elif action == "save":
        if len(selected) != 2:
            alert_text = (
                "الرجاء اختيار يومي إجازة بالضبط." 
                if lang == "ar" 
                else "Please select exactly 2 rest days."
            )
            await query.answer(alert_text, show_alert=True)
            return
            
        rest_days_str = ",".join(selected)
        db.update_user_fields(user_id, rest_days=rest_days_str)
        
        msg = "✅ تم حفظ أيام الإجازة." if lang == "ar" else "✅ Rest days saved."
        await query.edit_message_text(text=msg)
        await _send_gender_picker(context.bot, user_id, lang)


async def _send_gender_picker(bot, user_id: int, lang: str):
    keyboard = InlineKeyboardMarkup([
        [InlineKeyboardButton(t("btn_male", lang), callback_data="gender|male")],
        [InlineKeyboardButton(t("btn_female", lang), callback_data="gender|female")]
    ])
    msg_text = "الرجاء اختيار الجنس لتحديد مجموعة المناقشة المناسبة:" if lang == "ar" else "Please select your gender:"
    await bot.send_message(chat_id=user_id, text=msg_text, reply_markup=keyboard)


async def handle_gender_choice(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    
    user_id = query.from_user.id
    user = db.get_user(user_id)
    lang = user.get("language", "ar") if user else "ar"
    
    gender = query.data.split("|")[1]
    group_id = getattr(config, "MEN_GROUP_ID", None) if gender == "male" else getattr(config, "WOMEN_GROUP_ID", None)
    
    db.update_user_fields(user_id, gender=gender, group_id=group_id)
    await query.edit_message_text(text="تم حفظ بياناتك بنجاح! الآن اختر وقت استلام الدرس اليومي:")
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
    msg_text = "اختر الوقت المناسب لوصول درسك اليومي:" if lang == "ar" else "Choose your daily lesson time:"
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
        
    msg = f"✅ تم! تم ضبط وقت الدرس الساعة {time_str}." if lang == "ar" else f"✅ Done! Lesson time set to {time_str}."
    await query.edit_message_text(text=msg)


def main():
    token = os.environ.get("TELEGRAM_BOT_TOKEN")
    if not token:
        logger.error("لم يتم العثور على توكن البوت TELEGRAM_BOT_TOKEN في متغيرات البيئة!")
        return
        
    db.init_db()
    
    application = ApplicationBuilder().token(token).build()
    
    application.add_handler(CommandHandler("start", start_command))
    application.add_handler(CallbackQueryHandler(handle_language_choice, pattern="^lang\\|"))
    application.add_handler(CallbackQueryHandler(handle_rest_days_choice, pattern="^rest\\|"))
    application.add_handler(CallbackQueryHandler(handle_gender_choice, pattern="^gender\\|"))
    application.add_handler(CallbackQueryHandler(handle_time_choice, pattern="^time\\|"))
    
    # استعادة الجدولة السابقة عند الإقلاع
    restore_all_schedules(application.job_queue)
    
    # جلب المنفذ ورابط المشروع من إعدادات Render
    PORT = int(os.environ.get("PORT", "8443"))
    RENDER_EXTERNAL_URL = os.environ.get("RENDER_EXTERNAL_URL")
    
    logger.info("البوت يعمل الآن بنظام الـ Webhook...")
    
    if RENDER_EXTERNAL_URL:
        # التشغيل الحقيقي على Render بنظام الـ Webhook
        application.run_webhook(
            listen="0.0.0.0",
            port=PORT,
            url_path=token,
            webhook_url=f"{RENDER_EXTERNAL_URL}/{token}"
        )
    else:
        # احتياطي لو تم التشغيل محلياً
        application.run_polling()


if __name__ == "__main__":
    main()
