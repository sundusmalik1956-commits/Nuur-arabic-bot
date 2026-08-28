# bot.py
import os
import logging
import asyncio
from datetime import datetime, time
from typing import Dict, Optional, Any

from telegram import (
    Update, InlineKeyboardButton, InlineKeyboardMarkup,
    ReplyKeyboardMarkup, KeyboardButton
)
from telegram.ext import (
    Application, CommandHandler, CallbackQueryHandler,
    MessageHandler, filters, ContextTypes, JobQueue
)
from telegram.constants import ParseMode
from dotenv import load_dotenv

from database import Database
from translations import get_text, get_languages, get_times
from gemini_service import GeminiService

# تحميل المتغيرات البيئية
load_dotenv()

# إعداد التسجيل
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# المتغيرات الأساسية
BOT_TOKEN = os.getenv('8840764246:AAFhMuZBDxXjAWybAcYO1MeH6mQi-EOGfk8')
GEMINI_API_KEY = os.getenv('iXp2hUjxXlJmdVc_xwTT7DEpVb1b1MqUJOSi-lQ')
ACHIEVEMENT_GROUP_ID = os.getenv('ACHIEVEMENT_GROUP_ID', '-1004491283200')

# التحقق من المتغيرات الأساسية
if not BOT_TOKEN:
    raise ValueError("BOT_TOKEN غير موجود في ملف .env")

# تهيئة الخدمات
db = Database()
gemini = GeminiService(GEMINI_API_KEY) if GEMINI_API_KEY else None

# المهارات المطلوبة لإكمال الدرس
REQUIRED_SKILLS = [
    'introduction',  # التمهيد
    'vocabulary',    # المفردات
    'grammar',       # القواعد
    'reading',       # القراءة
    'listening',     # الاستماع
    'conversation',  # المحادثة
    'writing'        # الكتابة
]

class NoorBot:
    """النظام الرئيسي للبوت"""
    
    def __init__(self):
        self.app = None
        self.job_queue = None
        
    async def start(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """رسالة /start"""
        user_id = update.effective_user.id
        username = update.effective_user.username
        first_name = update.effective_user.first_name
        
        # التحقق من وجود المستخدم في قاعدة البيانات
        user = db.get_user(user_id)
        
        if user:
            # المستخدم موجود - عرض القائمة الرئيسية
            lang = user['language'] or 'ar'
            await self.show_main_menu(update, context, lang)
            return
        
        # مستخدم جديد - اختيار اللغة
        keyboard = []
        for code, name in get_languages().items():
            flag = '🇸🇦' if code == 'ar' else '🇬🇧' if code == 'en' else '🇹🇷'
            keyboard.append([InlineKeyboardButton(
                f"{flag} {name}", callback_data=f"lang_{code}"
            )])
        
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await update.message.reply_text(
            "🌍 مرحباً بك في نور بوت!\n\n"
            "اختر لغة التعليم / Choose your language / Eğitim dilinizi seçin:",
            reply_markup=reply_markup
        )
    
    async def show_main_menu(self, update: Update, context: ContextTypes.DEFAULT_TYPE, lang: str):
        """عرض القائمة الرئيسية"""
        user_id = update.effective_user.id
        user = db.get_user(user_id)
        
        if not user:
            await update.message.reply_text(
                get_text('start', lang)
            )
            return
        
        completed = user['completed_lessons'] or 0
        current = user['current_lesson'] or 1
        
        # التحقق من حالة الاشتراك
        if user['subscription_status'] == 'expired':
            await self.show_subscription_expired(update, context, lang)
            return
        
        keyboard = [
            [InlineKeyboardButton(
                get_text('continue_lesson', lang),
                callback_data='continue_lesson'
            )],
            [InlineKeyboardButton(
                f"📊 {get_text('progress', lang)} ({completed}/18)",
                callback_data='show_progress'
            )],
            [InlineKeyboardButton(
                f"⚙️ {get_text('settings', lang)}",
                callback_data='settings'
            )]
        ]
        
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        message = get_text('main_menu', lang).format(
            name=user['first_name'] or '👤',
            current=current,
            completed=completed
        )
        
        await update.message.reply_text(message, reply_markup=reply_markup)
    
    async def language_selected(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """معالج اختيار اللغة"""
        query = update.callback_query
        await query.answer()
        
        user_id = update.effective_user.id
        username = update.effective_user.username
        first_name = update.effective_user.first_name
        
        lang = query.data.split('_')[1]
        
        # حفظ اللغة في قاعدة البيانات
        db.add_user(user_id, username, first_name, lang)
        
        await query.edit_message_text(
            get_text('language_selected', lang).format(lang=get_languages()[lang])
        )
        
        # عرض اختيار الوقت
        await self.ask_time(update, context, lang)
    
    async def ask_time(self, update: Update, context: ContextTypes.DEFAULT_TYPE, lang: str):
        """طلب اختيار وقت الدرس"""
        keyboard = []
        for t in get_times():
            keyboard.append([InlineKeyboardButton(t, callback_data=f"time_{t}")])
        
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        if update.callback_query:
            await update.callback_query.message.reply_text(
                get_text('choose_time', lang),
                reply_markup=reply_markup
            )
        else:
            await update.message.reply_text(
                get_text('choose_time', lang),
                reply_markup=reply_markup
            )
    
    async def time_selected(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """معالج اختيار الوقت"""
        query = update.callback_query
        await query.answer()
        
        user_id = update.effective_user.id
        selected_time = query.data.split('_')[1]
        
        user = db.get_user(user_id)
        if not user:
            await query.edit_message_text("حدث خطأ. الرجاء استخدام /start")
            return
        
        lang = user['language'] or 'ar'
        
        # حفظ الوقت
        db.update_user(user_id, {'lesson_time': selected_time})
        
        await query.edit_message_text(
            get_text('time_selected', lang).format(time=selected_time)
        )
        
        # جدولة الدرس
        await self.schedule_lesson(user_id, selected_time)
        
        # عرض القائمة الرئيسية
        await self.show_main_menu_from_callback(query, lang)
    
    async def show_main_menu_from_callback(self, query, lang: str):
        """عرض القائمة الرئيسية من خلال callback"""
        user = db.get_user(query.from_user.id)
        completed = user['completed_lessons'] or 0
        current = user['current_lesson'] or 1
        
        keyboard = [
            [InlineKeyboardButton(
                get_text('continue_lesson', lang),
                callback_data='continue_lesson'
            )],
            [InlineKeyboardButton(
                f"📊 {get_text('progress', lang)} ({completed}/18)",
                callback_data='show_progress'
            )],
            [InlineKeyboardButton(
                f"⚙️ {get_text('settings', lang)}",
                callback_data='settings'
            )]
        ]
        
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await query.message.reply_text(
            get_text('main_menu', lang).format(
                name=user['first_name'] or '👤',
                current=current,
                completed=completed
            ),
            reply_markup=reply_markup
        )
    
    async def schedule_lesson(self, user_id: int, lesson_time: str):
        """جدولة الدرس للطالب"""
        if not self.job_queue:
            logger.warning("JobQueue غير متاحة")
            return
        
        # تحويل الوقت إلى ساعات ودقائق
        try:
            hour, minute = map(int, lesson_time.split(':'))
        except:
            logger.error(f"تنسيق وقت غير صحيح: {lesson_time}")
            return
        
        # أيام الدراسة (الأحد - الخميس)
        days = [0, 1, 2, 3, 4]  # 0 = الأحد, 4 = الخميس
        
        # إلغاء الجدولة القديمة إذا وجدت
        current_jobs = self.job_queue.jobs()
        for job in current_jobs:
            if job.name == f"lesson_{user_id}":
                job.schedule_removal()
        
        # إنشاء جدولة جديدة
        job = self.job_queue.run_daily(
            self.send_scheduled_lesson,
            time=time(hour=hour, minute=minute),
            days=tuple(days),
            name=f"lesson_{user_id}",
            data={'user_id': user_id}
        )
        
        logger.info(f"تم جدولة الدرس للمستخدم {user_id} في {lesson_time}")
    
    async def send_scheduled_lesson(self, context: ContextTypes.DEFAULT_TYPE):
        """إرسال الدرس المجدول"""
        data = context.job.data
        user_id = data['user_id']
        
        user = db.get_user(user_id)
        if not user:
            logger.warning(f"المستخدم {user_id} غير موجود")
            return
        
        # التحقق من حالة الاشتراك
        if user['subscription_status'] == 'expired':
            return
        
        lang = user['language'] or 'ar'
        current_lesson = user['current_lesson'] or 1
        
        # إرسال الدرس
        await self.send_lesson(user_id, current_lesson, lang)
    
    async def send_lesson(self, user_id: int, lesson_num: int, lang: str):
        """إرسال محتوى الدرس"""
        # استيراد الدرس ديناميكياً
        try:
            lesson_module = __import__(f'lesson{lesson_num}')
            await lesson_module.send_lesson(user_id, lang)
            logger.info(f"تم إرسال الدرس {lesson_num} للمستخدم {user_id}")
        except ImportError:
            logger.error(f"ملف الدرس {lesson_num} غير موجود")
            # إرسال رسالة للمستخدم
            bot = self.app.bot
            await bot.send_message(
                user_id,
                get_text('lesson_not_found', lang)
            )
        except Exception as e:
            logger.error(f"خطأ في إرسال الدرس {lesson_num}: {e}")
    
    async def continue_lesson(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """متابعة الدرس الحالي"""
        query = update.callback_query
        await query.answer()
        
        user_id = query.from_user.id
        user = db.get_user(user_id)
        
        if not user:
            await query.edit_message_text("حدث خطأ. الرجاء استخدام /start")
            return
        
        lang = user['language'] or 'ar'
        current_lesson = user['current_lesson'] or 1
        
        # التحقق من اكتمال الدروس المدفوعة
        if current_lesson > 5 and user['subscription_status'] != 'active':
            await self.show_subscription_expired_callback(query, lang)
            return
        
        # إرسال الدرس
        await self.send_lesson(user_id, current_lesson, lang)
    
    async def show_progress(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """عرض التقدم"""
        query = update.callback_query
        await query.answer()
        
        user_id = query.from_user.id
        user = db.get_user(user_id)
        
        if not user:
            await query.edit_message_text("حدث خطأ. الرجاء استخدام /start")
            return
        
        lang = user['language'] or 'ar'
        completed = user['completed_lessons'] or 0
        current = user['current_lesson'] or 1
        
        # حساب النسبة المئوية
        percentage = (completed / 18) * 100
        
        # إنشاء شريط التقدم
        progress_bar = "█" * int(percentage // 5) + "░" * (20 - int(percentage // 5))
        
        message = get_text('progress_details', lang).format(
            completed=completed,
            total=18,
            percentage=percentage,
            progress_bar=progress_bar,
            current=current
        )
        
        await query.edit_message_text(message)
        
        # إعادة عرض القائمة
        await self.show_main_menu_from_callback(query, lang)
    
    async def settings(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """عرض الإعدادات"""
        query = update.callback_query
        await query.answer()
        
        user_id = query.from_user.id
        user = db.get_user(user_id)
        
        if not user:
            await query.edit_message_text("حدث خطأ. الرجاء استخدام /start")
            return
        
        lang = user['language'] or 'ar'
        
        keyboard = [
            [InlineKeyboardButton(
                f"🌐 {get_text('change_language', lang)}",
                callback_data='change_language'
            )],
            [InlineKeyboardButton(
                f"⏰ {get_text('change_time', lang)}",
                callback_data='change_time'
            )],
            [InlineKeyboardButton(
                f"🔙 {get_text('back', lang)}",
                callback_data='back_to_menu'
            )]
        ]
        
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await query.edit_message_text(
            get_text('settings_menu', lang),
            reply_markup=reply_markup
        )
    
    async def change_language(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """تغيير اللغة"""
        query = update.callback_query
        await query.answer()
        
        user_id = query.from_user.id
        user = db.get_user(user_id)
        current_lang = user['language'] or 'ar'
        
        keyboard = []
        for code, name in get_languages().items():
            flag = '🇸🇦' if code == 'ar' else '🇬🇧' if code == 'en' else '🇹🇷'
            is_current = " ✅" if code == current_lang else ""
            keyboard.append([InlineKeyboardButton(
                f"{flag} {name}{is_current}", callback_data=f"newlang_{code}"
            )])
        
        keyboard.append([InlineKeyboardButton(
            "🔙 " + get_text('back', current_lang),
            callback_data='back_to_settings'
        )])
        
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await query.edit_message_text(
            get_text('select_language', current_lang),
            reply_markup=reply_markup
        )
    
    async def change_time(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """تغيير وقت الدرس"""
        query = update.callback_query
        await query.answer()
        
        user_id = query.from_user.id
        user = db.get_user(user_id)
        lang = user['language'] or 'ar'
        
        keyboard = []
        for t in get_times():
            keyboard.append([InlineKeyboardButton(t, callback_data=f"newtime_{t}")])
        
        keyboard.append([InlineKeyboardButton(
            "🔙 " + get_text('back', lang),
            callback_data='back_to_settings'
        )])
        
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await query.edit_message_text(
            get_text('choose_new_time', lang),
            reply_markup=reply_markup
        )
    
    async def new_language_selected(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """معالج تغيير اللغة"""
        query = update.callback_query
        await query.answer()
        
        user_id = query.from_user.id
        new_lang = query.data.split('_')[1]
        
        db.update_user(user_id, {'language': new_lang})
        
        # إعادة جدولة الدرس
        user = db.get_user(user_id)
        if user and user['lesson_time']:
            await self.schedule_lesson(user_id, user['lesson_time'])
        
        await query.edit_message_text(
            get_text('language_updated', new_lang).format(lang=get_languages()[new_lang])
        )
        
        # العودة للإعدادات
        await self.settings(update, context)
    
    async def new_time_selected(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """معالج تغيير الوقت"""
        query = update.callback_query
        await query.answer()
        
        user_id = query.from_user.id
        new_time = query.data.split('_')[1]
        
        user = db.get_user(user_id)
        if not user:
            await query.edit_message_text("حدث خطأ. الرجاء استخدام /start")
            return
        
        lang = user['language'] or 'ar'
        
        db.update_user(user_id, {'lesson_time': new_time})
        await self.schedule_lesson(user_id, new_time)
        
        await query.edit_message_text(
            get_text('time_updated', lang).format(time=new_time)
        )
        
        # العودة للإعدادات
        await self.settings(update, context)
    
    async def back_to_menu(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """العودة للقائمة الرئيسية"""
        query = update.callback_query
        await query.answer()
        
        user_id = query.from_user.id
        user = db.get_user(user_id)
        
        if not user:
            await query.edit_message_text("حدث خطأ. الرجاء استخدام /start")
            return
        
        lang = user['language'] or 'ar'
        await self.show_main_menu_from_callback(query, lang)
    
    async def back_to_settings(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """العودة للإعدادات"""
        query = update.callback_query
        await query.answer()
        await self.settings(update, context)
    
    async def show_subscription_expired(self, update: Update, context: ContextTypes.DEFAULT_TYPE, lang: str):
        """عرض رسالة انتهاء الاشتراك"""
        keyboard = [
            [InlineKeyboardButton(
                "📚 " + get_text('subscription_info', lang),
                url="https://t.me/NoorBotSupport"
            )],
            [InlineKeyboardButton(
                get_text('back', lang),
                callback_data='back_to_menu'
            )]
        ]
        
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await update.message.reply_text(
            get_text('subscription_expired', lang),
            reply_markup=reply_markup
        )
    
    async def show_subscription_expired_callback(self, query, lang: str):
        """عرض رسالة انتهاء الاشتراك من callback"""
        keyboard = [
            [InlineKeyboardButton(
                "📚 " + get_text('subscription_info', lang),
                url="https://t.me/NoorBotSupport"
            )],
            [InlineKeyboardButton(
                get_text('back', lang),
                callback_data='back_to_menu'
            )]
        ]
        
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await query.edit_message_text(
            get_text('subscription_expired', lang),
            reply_markup=reply_markup
        )
    
    async def handle_button(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """معالج الأزرار العامة"""
        query = update.callback_query
        await query.answer()
        
        # تمرير المعالجة للدروس
        # سيتم إضافة هذا لاحقاً عند إنشاء الدروس
    
    async def handle_message(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """معالج الرسائل النصية"""
        user_id = update.effective_user.id
        user = db.get_user(user_id)
        
        if not user:
            await update.message.reply_text(
                "الرجاء استخدام /start للبدء"
            )
            return
        
        # سيتم معالجة رسائل المحادثة والكتابة في الدروس
    
    async def progress_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """الأمر /progress"""
        user_id = update.effective_user.id
        user = db.get_user(user_id)
        
        if not user:
            await update.message.reply_text("الرجاء استخدام /start للبدء")
            return
        
        lang = user['language'] or 'ar'
        completed = user['completed_lessons'] or 0
        current = user['current_lesson'] or 1
        
        percentage = (completed / 18) * 100
        progress_bar = "█" * int(percentage // 5) + "░" * (20 - int(percentage // 5))
        
        message = get_text('progress_details', lang).format(
            completed=completed,
            total=18,
            percentage=percentage,
            progress_bar=progress_bar,
            current=current
        )
        
        await update.message.reply_text(message)
    
    async def settings_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """الأمر /settings"""
        user_id = update.effective_user.id
        user = db.get_user(user_id)
        
        if not user:
            await update.message.reply_text("الرجاء استخدام /start للبدء")
            return
        
        # محاكاة الضغط على زر الإعدادات
        class MockQuery:
            def __init__(self, user_id, message):
                self.from_user = type('obj', (object,), {'id': user_id})()
                self.message = message
            
            async def answer(self):
                pass
            
            async def edit_message_text(self, text, reply_markup=None):
                await message.edit_text(text, reply_markup=reply_markup)
        
        message = await update.message.reply_text("...")
        mock_query = MockQuery(user_id, message)
        
        await self.settings(
            type('obj', (object,), {'callback_query': mock_query, 'message': message})(),
            context
        )
    
    async def check_lesson_completion(self, user_id: int, lesson_num: int):
        """التحقق من إكمال الدرس"""
        user = db.get_user(user_id)
        if not user:
            return
        
        completed_skills = user.get('completed_skills', {})
        lesson_skills = completed_skills.get(str(lesson_num), [])
        
        # التحقق من إكمال جميع المهارات
        if all(skill in lesson_skills for skill in REQUIRED_SKILLS):
            await self.complete_lesson(user_id, lesson_num)
    
    async def complete_lesson(self, user_id: int, lesson_num: int):
        """إكمال الدرس"""
        user = db.get_user(user_id)
        if not user:
            return
        
        lang = user['language'] or 'ar'
        completed = user['completed_lessons'] or 0
        
        # التحقق من عدم اكتمال الدرس سابقاً
        if lesson_num <= completed:
            return
        
        # تحديث عدد الدروس المكتملة
        db.update_user(user_id, {'completed_lessons': lesson_num})
        
        # تحديث الدرس الحالي
        if lesson_num < 18:
            db.update_user(user_id, {'current_lesson': lesson_num + 1})
        
        # التحقق من اكتمال جميع الدروس
        if lesson_num == 18:
            await self.certificate_completion(user_id, lang)
        
        # إرسال إعلان للإنجاز
        await self.send_achievement(user_id, lesson_num, lang)
        
        # إرسال رسالة للطالب
        bot = self.app.bot
        await bot.send_message(
            user_id,
            get_text('lesson_completed', lang).format(lesson=lesson_num)
        )
        
        # إذا كان هناك درس تالي
        if lesson_num < 18:
            next_lesson = lesson_num + 1
            await bot.send_message(
                user_id,
                get_text('next_lesson', lang).format(next=next_lesson)
            )
            
            # التحقق من الاشتراك للدرس السادس
            if next_lesson == 6 and user['subscription_status'] != 'active':
                await bot.send_message(
                    user_id,
                    get_text('subscription_expired', lang)
                )
    
    async def send_achievement(self, user_id: int, lesson_num: int, lang: str):
        """إرسال إعلان الإنجاز للقروب"""
        try:
            bot = self.app.bot
            user = db.get_user(user_id)
            
            if not user:
                return
            
            # جلب اسم الدرس
            lesson_name = get_text(f'lesson_{lesson_num}_name', 'ar')
            
            message = get_text('achievement_announcement', 'ar').format(
                name=user['first_name'] or 'طالب',
                lesson_num=lesson_num,
                lesson_name=lesson_name
            )
            
            await bot.send_message(
                ACHIEVEMENT_GROUP_ID,
                message,
                parse_mode=ParseMode.HTML
            )
            
            logger.info(f"تم إرسال إعلان إنجاز للمستخدم {user_id} - الدرس {lesson_num}")
        except Exception as e:
            logger.error(f"خطأ في إرسال إعلان الإنجاز: {e}")
    
    async def certificate_completion(self, user_id: int, lang: str):
        """إصدار شهادة إتمام البرنامج"""
        bot = self.app.bot
        user = db.get_user(user_id)
        
        if not user:
            return
        
        # هذه نسخة مبسطة - سيتم تطويرها لاحقاً
        await bot.send_message(
            user_id,
            get_text('certificate_completion', lang).format(name=user['first_name'] or 'طالب')
        )
    
    async def skill_completed(self, update: Update, context: ContextTypes.DEFAULT_TYPE, skill: str):
        """تسجيل إكمال مهارة"""
        query = update.callback_query
        user_id = query.from_user.id
        
        user = db.get_user(user_id)
        if not user:
            return
        
        current_lesson = user['current_lesson'] or 1
        
        # تحديث المهارات المكتملة
        completed_skills = user.get('completed_skills', {})
        lesson_skills = completed_skills.get(str(current_lesson), [])
        
        if skill not in lesson_skills:
            lesson_skills.append(skill)
            completed_skills[str(current_lesson)] = lesson_skills
            db.update_user(user_id, {'completed_skills': completed_skills})
        
        # التحقق من اكتمال الدرس
        await self.check_lesson_completion(user_id, current_lesson)
    
    def setup_handlers(self):
        """إعداد معالجات الأوامر"""
        # أوامر البوت
        self.app.add_handler(CommandHandler("start", self.start))
        self.app.add_handler(CommandHandler("progress", self.progress_command))
        self.app.add_handler(CommandHandler("settings", self.settings_command))
        
        # معالجات الـ Callback
        self.app.add_handler(CallbackQueryHandler(
            self.language_selected, pattern="^lang_"
        ))
        self.app.add_handler(CallbackQueryHandler(
            self.time_selected, pattern="^time_"
        ))
        self.app.add_handler(CallbackQueryHandler(
            self.new_language_selected, pattern="^newlang_"
        ))
        self.app.add_handler(CallbackQueryHandler(
            self.new_time_selected, pattern="^newtime_"
        ))
        self.app.add_handler(CallbackQueryHandler(
            self.continue_lesson, pattern="^continue_lesson$"
        ))
        self.app.add_handler(CallbackQueryHandler(
            self.show_progress, pattern="^show_progress$"
        ))
        self.app.add_handler(CallbackQueryHandler(
            self.settings, pattern="^settings$"
        ))
        self.app.add_handler(CallbackQueryHandler(
            self.change_language, pattern="^change_language$"
        ))
        self.app.add_handler(CallbackQueryHandler(
            self.change_time, pattern="^change_time$"
        ))
        self.app.add_handler(CallbackQueryHandler(
            self.back_to_menu, pattern="^back_to_menu$"
        ))
        self.app.add_handler(CallbackQueryHandler(
            self.back_to_settings, pattern="^back_to_settings$"
        ))
        
        # معالج الأزرار العامة (للدروس)
        self.app.add_handler(CallbackQueryHandler(
            self.handle_button, pattern="^skill_"
        ))
        
        # معالج الرسائل النصية
        self.app.add_handler(MessageHandler(
            filters.TEXT & ~filters.COMMAND, self.handle_message
        ))
    
    async def initialize(self):
        """تهيئة البوت"""
        # إنشاء التطبيق
        self.app = Application.builder().token(BOT_TOKEN).build()
        
        # حفظ JobQueue
        self.job_queue = self.app.job_queue
        
        # إعداد المعالجات
        self.setup_handlers()
        
        # استعادة الجدولة للمستخدمين النشطين
        await self.restore_schedules()
        
        # بدء البوت
        await self.app.initialize()
        await self.app.start()
        await self.app.updater.start_polling()
    
    async def restore_schedules(self):
        """استعادة الجدولة عند إعادة التشغيل"""
        users = db.get_active_users()
        restored = 0
        
        for user in users:
            user_id = user['user_id']
            lesson_time = user['lesson_time']
            
            if lesson_time:
                try:
                    await self.schedule_lesson(user_id, lesson_time)
                    restored += 1
                except Exception as e:
                    logger.error(f"خطأ في استعادة جدولة المستخدم {user_id}: {e}")
        
        logger.info(f"تم استعادة جدولة {restored} مستخدم")
    
    async def start_bot(self):
        """تشغيل البوت"""
        try:
            logger.info("جارٍ تشغيل نور بوت...")
            await self.initialize()
            
            # الحفاظ على تشغيل البوت
            while True:
                await asyncio.sleep(1)
        except KeyboardInterrupt:
            logger.info("تم إيقاف البوت")
        except Exception as e:
            logger.error(f"خطأ في تشغيل البوت: {e}")
        finally:
            if self.app:
                await self.app.updater.stop()
                await self.app.stop()
                await self.app.shutdown()

def main():
    """الدالة الرئيسية"""
    bot = NoorBot()
    asyncio.run(bot.start_bot())

if __name__ == "__main__":
    main()
