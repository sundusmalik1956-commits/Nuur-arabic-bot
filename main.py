import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, MessageHandler, filters, ContextTypes
from config import Config
from languages import LANGUAGES, LANGUAGE_CODES
from database import Database
from lessons import lessons_manager
from scheduler import LessonScheduler
from excel_exporter import excel_exporter
from ai_tutor import ai_tutor
import json
from datetime import datetime

# إعداد التسجيل
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', 
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# تهيئة قاعدة البيانات
db = Database()

class ArabicLearningBot:
    def __init__(self):
        self.application = None
        self.scheduler = None
        
        # حالات المستخدمين (لتتبع مرحلة الإعداد)
        self.user_states = {}
        
        # بيانات مؤقتة للمستخدمين أثناء الإعداد
        self.temp_data = {}
    
    def run(self):
        """تشغيل البوت"""
        # إنشاء التطبيق
        self.application = Application.builder().token(Config.BOT_TOKEN).build()
        
        # إضافة معالجات الأوامر
        self.application.add_handler(CommandHandler("start", self.start_command))
        self.application.add_handler(CommandHandler("menu", self.menu_command))
        self.application.add_handler(CommandHandler("settings", self.settings_command))
        self.application.add_handler(CommandHandler("lessons", self.lessons_command))
        self.application.add_handler(CommandHandler("practice", self.practice_command))
        self.application.add_handler(CommandHandler("progress", self.progress_command))
        self.application.add_handler(CommandHandler("export", self.export_command))  # للأدمن فقط
        
        # معالجات الاستعلامات
        self.application.add_handler(CallbackQueryHandler(self.handle_callback))
        
        # معالجات الرسائل النصية
        self.application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, self.handle_message))
        
        # بدء الجدولة
        self.scheduler = LessonScheduler(self.application.bot)
        
        # تشغيل البوت
        logger.info("Bot is starting...")
        self.application.run_polling(allowed_updates=Update.ALL_TYPES)
    
    async def start_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """معالج أمر /start"""
        user = update.effective_user
        user_id = user.id
        
        # حفظ معلومات المستخدم
        db.create_user(
            user_id=user_id,
            username=user.username,
            first_name=user.first_name,
            last_name=user.last_name
        )
        
        # عرض اختيار اللغة
        await self.show_language_selection(update, context)
    
    async def show_language_selection(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """عرض اختيار اللغة"""
        keyboard = []
        row = []
        for code in LANGUAGE_CODES:
            lang = LANGUAGES[code]
            row.append(InlineKeyboardButton(f"{lang['flag']} {lang['name']}", callback_data=f"lang_{code}"))
            if len(row) == 2:
                keyboard.append(row)
                row = []
        if row:
            keyboard.append(row)
        
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        message = "🌍 *مرحباً بك في بوت تعلم اللغة العربية!* 🌍\n\n"
        message += "اختر لغتك المفضلة:\n"
        message += "Choose your preferred language:\n"
        message += "Tercih ettiğiniz dili seçin:\n"
        message += "Elija su idioma preferido:\n"
        message += "Choisissez votre langue préférée:\n"
        message += "Выберите предпочитаемый язык:\n"
        message += "选择您的首选语言:\n"
        message += "اپنی پسندیدہ زبان منتخب کریں:\n"
        message += "अपनी पसंदीदा भाषा चुनें:\n"
        message += "زبان مورد نظر خود را انتخاب کنید:\n"
        message += "Pilih bahasa preferensi Anda:"
        
        await update.message.reply_text(
            message,
            reply_markup=reply_markup,
            parse_mode='Markdown'
        )
    
    async def handle_callback(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """معالج الاستعلامات"""
        query = update.callback_query
        await query.answer()
        
        data = query.data
        user_id = query.from_user.id
        
        # معالجة اختيار اللغة
        if data.startswith('lang_'):
            lang_code = data.split('_')[1]
            db.update_user(user_id, language=lang_code)
            context.user_data['language'] = lang_code
            
            # عرض رسالة الترحيب والتعريف بالمنهج
            await self.show_welcome_message(query, lang_code)
            return
        
        # معالجة اختيار المستوى
        if data.startswith('level_'):
            level = data.split('_')[1]
            db.update_user(user_id, level=level)
            context.user_data['level'] = level
            
            # عرض اختيار الجنس
            await self.show_gender_selection(query, user_id)
            return
        
        # معالجة اختيار الجنس
        if data.startswith('gender_'):
            gender = data.split('_')[1]
            db.update_user(user_id, gender=gender)
            context.user_data['gender'] = gender
            
            # عرض رابط القروب المناسب
            await self.show_group_link(query, user_id, gender)
            return
        
        # معالجة اختيار الوقت
        if data.startswith('time_'):
            time = data.split('_')[1]
            db.update_user(user_id, lesson_time=time)
            context.user_data['lesson_time'] = time
            
            # عرض اختيار أيام الإجازة
            await self.show_days_off_selection(query, user_id)
            return
        
        # معالجة اختيار أيام الإجازة
        if data.startswith('dayoff_'):
            day = data.split('_')[1]
            
            # الحصول على الأيام المحددة حالياً
            if user_id not in self.temp_data:
                self.temp_data[user_id] = {}
            if 'days_off' not in self.temp_data[user_id]:
                self.temp_data[user_id]['days_off'] = []
            
            days_off = self.temp_data[user_id]['days_off']
            
            if day in days_off:
                days_off.remove(day)
            else:
                if len(days_off) < 2:
                    days_off.append(day)
            
            # تحديث العرض
            await self.update_days_off_selection(query, user_id)
            return
        
        # معالجة تأكيد أيام الإجازة
        if data == 'confirm_days_off':
            days_off = self.temp_data.get(user_id, {}).get('days_off', [])
            db.update_user(user_id, days_off=days_off)
            context.user_data['days_off'] = days_off
            
            # عرض الملخص النهائي
            await self.show_final_summary(query, user_id)
            return
        
        # معالجة تغيير الإعدادات
        if data.startswith('change_'):
            setting = data.split('_')[1]
            await self.handle_setting_change(query, user_id, setting)
            return
        
        # معالجة عرض القائمة الرئيسية
        if data == 'main_menu':
            await self.show_main_menu(query, user_id)
            return
        
        # معالجة عرض المستويات
        if data == 'show_levels':
            await self.show_levels(query, user_id)
            return
        
        # معالجة عرض الدروس
        if data.startswith('show_lessons_'):
            level = data.split('_')[2]
            await self.show_lessons(query, user_id, level)
            return
        
        # معالجة عرض درس معين
        if data.startswith('lesson_'):
            parts = data.split('_')
            level = parts[1]
            lesson_id = int(parts[2])
            await self.show_lesson(query, user_id, level, lesson_id)
            return
        
        # معالجة عرض المزيد من الدروس
        if data.startswith('more_lessons_'):
            parts = data.split('_')
            level = parts[2]
            start = int(parts[3]) if len(parts) > 3 else 0
            await self.show_more_lessons(query, user_id, level, start)
            return
        
        # معالجة التدريب
        if data.startswith('practice_'):
            practice_type = data.split('_')[1]
            await self.handle_practice(query, user_id, practice_type)
            return
        
        # معالجة تصحيح النص
        if data == 'correct_text':
            await self.handle_correction(query, user_id)
            return
        
        # معالجة عرض الإعدادات
        if data == 'settings':
            await self.settings_callback(query, user_id)
            return
        
        # معالجة عرض التقدم
        if data == 'progress':
            await self.progress_callback(query, user_id)
            return
        
        # معالجة عرض دروسي
        if data == 'my_lessons':
            user = db.get_user(user_id)
            level = user.get('level', 'A1')
            await self.show_lessons(query, user_id, level)
            return
    
    async def show_welcome_message(self, query, lang_code: str):
        """عرض رسالة الترحيب والتعريف بالمنهج"""
        user_id = query.from_user.id
        lang = LANGUAGES[lang_code]
        
        message = f"🌟 *{lang.get('welcome', 'مرحباً')}* 🌟\n\n"
        message += "📚 *المنهج الدراسي:*\n"
        message += "• 5 مستويات: A0, A1, A2, B1, B2\n"
        message += "• كل مستوى يحتوي على 18 درساً\n"
        message += "• أول 5 دروس مجانية في كل مستوى\n"
        message += f"• سعر الاشتراك: {Config.SUBSCRIPTION_PRICE}$ للمستوى الكامل\n\n"
        message += "🔍 *اختبار تحديد المستوى:*\n"
        message += f"قم بزيارة {Config.LEVEL_TEST_BOT} لتحديد مستواك المناسب\n\n"
        message += f"📖 *مستوى A0:* مخصص لمن لا يعرف الحروف تماماً (4 دروس فقط)"
        
        # أزرار اختيار المستوى
        keyboard = []
        for level in ['A0', 'A1', 'A2', 'B1', 'B2']:
            keyboard.append([InlineKeyboardButton(f"📚 {level}", callback_data=f"level_{level}")])
        keyboard.append([InlineKeyboardButton("🔙 رجوع", callback_data="main_menu")])
        
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await query.edit_message_text(
            message,
            reply_markup=reply_markup,
            parse_mode='Markdown'
        )
    
    async def show_gender_selection(self, query, user_id: int):
        """عرض اختيار الجنس"""
        user = db.get_user(user_id)
        lang_code = user.get('language', 'ar')
        lang = LANGUAGES[lang_code]
        
        message = f"👤 *{lang.get('choose_gender', 'اختر جنسك')}*"
        
        keyboard = [
            [
                InlineKeyboardButton(f"👨 {lang.get('gender_male', 'رجل')}", callback_data="gender_male"),
                InlineKeyboardButton(f"👩 {lang.get('gender_female', 'إمرأة')}", callback_data="gender_female")
            ],
            [InlineKeyboardButton("🔙 رجوع", callback_data="main_menu")]
        ]
        
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await query.edit_message_text(
            message,
            reply_markup=reply_markup,
            parse_mode='Markdown'
        )
    
    async def show_group_link(self, query, user_id: int, gender: str):
        """عرض رابط القروب المناسب"""
        user = db.get_user(user_id)
        lang_code = user.get('language', 'ar')
        lang = LANGUAGES[lang_code]
        
        group_link = Config.WOMEN_GROUP if gender == 'female' else Config.MEN_GROUP
        group_name = "النساء" if gender == 'female' else "الرجال"
        
        message = f"👥 *{lang.get('group_joined', 'تم توجيهك إلى قروب الدردشة المناسب')}*\n\n"
        message += f"🔗 رابط قروب {group_name}:\n"
        message += f"{group_link}\n\n"
        message += "⏰ *الآن، اختر وقت إرسال الدروس:*"
        
        # عرض اختيار الوقت
        keyboard = []
        for hour in range(0, 24):
            time_str = f"{hour:02d}:00"
            keyboard.append([InlineKeyboardButton(f"🕐 {time_str}", callback_data=f"time_{time_str}")])
        
        keyboard.append([InlineKeyboardButton("🔙 رجوع", callback_data="main_menu")])
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await query.edit_message_text(
            message,
            reply_markup=reply_markup,
            parse_mode='Markdown'
        )
    
    async def show_days_off_selection(self, query, user_id: int):
        """عرض اختيار أيام الإجازة"""
        user = db.get_user(user_id)
        lang_code = user.get('language', 'ar')
        lang = LANGUAGES[lang_code]
        
        # الحصول على أيام الأسبوع بلغة المستخدم
        days = Config.DAYS_OF_WEEK.get(lang_code, Config.DAYS_OF_WEEK['en'])
        
        # تهيئة البيانات المؤقتة
        if user_id not in self.temp_data:
            self.temp_data[user_id] = {}
        self.temp_data[user_id]['days_off'] = []
        
        await self.update_days_off_selection(query, user_id)
    
    async def update_days_off_selection(self, query, user_id: int):
        """تحديث عرض اختيار أيام الإجازة"""
        user = db.get_user(user_id)
        lang_code = user.get('language', 'ar')
        lang = LANGUAGES[lang_code]
        
        days = Config.DAYS_OF_WEEK.get(lang_code, Config.DAYS_OF_WEEK['en'])
        days_off = self.temp_data.get(user_id, {}).get('days_off', [])
        
        message = f"📅 *{lang.get('choose_days_off', 'اختر أيام الإجازة')}*\n\n"
        message += f"✅ تم اختيار: {', '.join(days_off) if days_off else 'لم يتم اختيار أي يوم'}\n"
        message += f"📌 يمكنك اختيار يومين كحد أقصى\n\n"
        
        keyboard = []
        for day in days:
            is_selected = day in days_off
            button_text = f"✅ {day}" if is_selected else f"⬜ {day}"
            keyboard.append([InlineKeyboardButton(button_text, callback_data=f"dayoff_{day}")])
        
        keyboard.append([
            InlineKeyboardButton("✅ تأكيد", callback_data="confirm_days_off"),
            InlineKeyboardButton("🔙 رجوع", callback_data="main_menu")
        ])
        
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await query.edit_message_text(
            message,
            reply_markup=reply_markup,
            parse_mode='Markdown'
        )
    
    async def show_final_summary(self, query, user_id: int):
        """عرض الملخص النهائي"""
        user = db.get_user(user_id)
        lang_code = user.get('language', 'ar')
        lang = LANGUAGES[lang_code]
        
        message = f"📋 *{lang.get('summary', 'ملخص بياناتك')}*\n\n"
        message += f"{lang.get('name_label', '👤 الاسم')} {user.get('first_name', '')}\n"
        message += f"{lang.get('level_label', '📚 المستوى')} {user.get('level', 'غير محدد')}\n"
        message += f"{lang.get('time_label', '⏰ وقت الدرس')} {user.get('lesson_time', 'غير محدد')}\n"
        message += f"{lang.get('days_off_label', '📅 أيام الإجازة')} {', '.join(user.get('days_off', [])) if user.get('days_off') else 'غير محددة'}\n"
        
        # إضافة رابط القروب
        group_link = Config.WOMEN_GROUP if user.get('gender') == 'female' else Config.MEN_GROUP
        message += f"{lang.get('group_label', '👥 رابط القروب')} {group_link}\n\n"
        
        message += "🔧 *يمكنك تغيير أي إعداد من الأزرار أدناه:*"
        
        keyboard = [
            [
                InlineKeyboardButton(lang.get('change_name', 'تغيير الاسم'), callback_data="change_name"),
                InlineKeyboardButton(lang.get('change_level', 'تغيير المستوى'), callback_data="change_level")
            ],
            [
                InlineKeyboardButton(lang.get('change_time', 'تغيير الوقت'), callback_data="change_time"),
                InlineKeyboardButton(lang.get('change_days', 'تغيير أيام الإجازة'), callback_data="change_days")
            ],
            [InlineKeyboardButton("📚 القائمة الرئيسية", callback_data="main_menu")]
        ]
        
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await query.edit_message_text(
            message,
            reply_markup=reply_markup,
            parse_mode='Markdown'
        )
        
        # إرسال رسالة ترحيب إضافية
        await query.message.reply_text(
            "🎉 *تهانينا! تم إعداد حسابك بنجاح.*\n\n"
            "📚 ستبدأ رحلة تعلم اللغة العربية قريباً.\n"
            "سيتم إرسال الدروس في الوقت المحدد.\n\n"
            "💡 *نصيحة:* استخدم الأزرار لتصفح الدروس والتدريبات في أي وقت.",
            parse_mode='Markdown'
        )
    
    async def show_main_menu(self, query, user_id: int):
        """عرض القائمة الرئيسية"""
        user = db.get_user(user_id)
        lang_code = user.get('language', 'ar')
        lang = LANGUAGES[lang_code]
        
        message = f"📚 *{lang.get('main_menu', 'القائمة الرئيسية')}*\n\n"
        message += "اختر ما تريد القيام به:"
        
        keyboard = [
            [InlineKeyboardButton("📖 عرض المستويات", callback_data="show_levels")],
            [InlineKeyboardButton("📚 دروسي", callback_data="my_lessons")],
            [InlineKeyboardButton("🗣️ تدريب المحادثة", callback_data="practice_conversation")],
            [InlineKeyboardButton("✍️ تدريب الكتابة", callback_data="practice_writing")],
            [InlineKeyboardButton("🔍 تصحيح النص", callback_data="correct_text")],
            [InlineKeyboardButton("⚙️ الإعدادات", callback_data="settings")],
            [InlineKeyboardButton("📊 تقدمي", callback_data="progress")]
        ]
        
        # إضافة زر التصدير للأدمن
        if user_id == Config.ADMIN_ID:
            keyboard.append([InlineKeyboardButton("📊 تصدير بيانات الطلاب", callback_data="admin_export")])
        
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await query.edit_message_text(
            message,
            reply_markup=reply_markup,
            parse_mode='Markdown'
        )
    
    async def show_levels(self, query, user_id: int):
        """عرض المستويات"""
        user = db.get_user(user_id)
        lang_code = user.get('language', 'ar')
        lang = LANGUAGES[lang_code]
        
        message = f"📚 *{lang.get('choose_level', 'اختر مستواك')}*\n\n"
        
        levels_info = {
            'A0': lang.get('level_a0_desc', 'مستوى A0: للمبتدئين الذين لا يعرفون الحروف العربية (4 دروس)'),
            'A1': lang.get('level_a1_desc', 'مستوى A1: مبتدئ (18 درس)'),
            'A2': lang.get('level_a2_desc', 'مستوى A2: ما قبل المتوسط (18 درس)'),
            'B1': lang.get('level_b1_desc', 'مستوى B1: متوسط (18 درس)'),
            'B2': lang.get('level_b2_desc', 'مستوى B2: فوق المتوسط (18 درس)')
        }
        
        keyboard = []
        for level, desc in levels_info.items():
            is_current = user.get('level') == level
            button_text = f"✅ {level}" if is_current else f"📚 {level}"
            keyboard.append([InlineKeyboardButton(button_text, callback_data=f"show_lessons_{level}")])
        
        keyboard.append([InlineKeyboardButton("🔙 رجوع", callback_data="main_menu")])
        
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await query.edit_message_text(
            message,
            reply_markup=reply_markup,
            parse_mode='Markdown'
        )
    
    async def show_lessons(self, query, user_id: int, level: str):
        """عرض دروس المستوى"""
        user = db.get_user(user_id)
        lang_code = user.get('language', 'ar')
        lang = LANGUAGES[lang_code]
        
        lessons = lessons_manager.get_level_lessons(level)
        completed_lessons = db.get_completed_lessons(user_id)
        
        message = f"📚 *مستوى {level}*\n\n"
        
        # عرض معلومات المستوى
        if level == 'A0':
            message += "📖 4 دروس (جميعها مجانية)\n"
        else:
            message += f"📖 18 درساً (أول 5 دروس مجانية)\n"
            message += f"💰 الاشتراك: {Config.SUBSCRIPTION_PRICE}$\n"
        
        message += "\n📋 *الدروس:*\n\n"
        
        keyboard = []
        # عرض أول 10 دروس
        for lesson in lessons[:10]:
            is_completed = lesson['id'] in completed_lessons
            is_free = lesson.get('is_free', False)
            status = "✅" if is_completed else "📖"
            if not is_free and not user.get('is_subscribed', False):
                status = "🔒"
            button_text = f"{status} {lesson['id']}. {lesson.get('title', '')}"
            keyboard.append([InlineKeyboardButton(button_text, callback_data=f"lesson_{level}_{lesson['id']}")])
        
        if len(lessons) > 10:
            keyboard.append([InlineKeyboardButton("📖 عرض المزيد...", callback_data=f"more_lessons_{level}_10")])
        
        keyboard.append([InlineKeyboardButton("🔙 رجوع", callback_data="show_levels")])
        
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await query.edit_message_text(
            message,
            reply_markup=reply_markup,
            parse_mode='Markdown'
        )
    
    async def show_more_lessons(self, query, user_id: int, level: str, start: int):
        """عرض المزيد من الدروس"""
        user = db.get_user(user_id)
        lessons = lessons_manager.get_level_lessons(level)
        completed_lessons = db.get_completed_lessons(user_id)
        
        end = min(start + 10, len(lessons))
        
        message = f"📚 *مستوى {level} - الدروس {start+1} إلى {end}*\n\n"
        
        keyboard = []
        for lesson in lessons[start:end]:
            is_completed = lesson['id'] in completed_lessons
            is_free = lesson.get('is_free', False)
            status = "✅" if is_completed else "📖"
            if not is_free and not user.get('is_subscribed', False):
                status = "🔒"
            button_text = f"{status} {lesson['id']}. {lesson.get('title', '')}"
            keyboard.append([InlineKeyboardButton(button_text, callback_data=f"lesson_{level}_{lesson['id']}")])
        
        navigation = []
        if start > 0:
            navigation.append(InlineKeyboardButton("⬅️ السابق", callback_data=f"more_lessons_{level}_{max(0, start-10)}"))
        if end < len(lessons):
            navigation.append(InlineKeyboardButton("التالي ➡️", callback_data=f"more_lessons_{level}_{end}"))
        if navigation:
            keyboard.append(navigation)
        
        keyboard.append([InlineKeyboardButton("🔙 رجوع", callback_data=f"show_lessons_{level}")])
        
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await query.edit_message_text(
            message,
            reply_markup=reply_markup,
            parse_mode='Markdown'
        )
    
    async def show_lesson(self, query, user_id: int, level: str, lesson_id: int):
        """عرض درس معين"""
        user = db.get_user(user_id)
        lang_code = user.get('language', 'ar')
        lang = LANGUAGES[lang_code]
        
        lesson = lessons_manager.get_lesson(level, lesson_id)
        if not lesson:
            await query.edit_message_text("⚠️ الدرس غير موجود")
            return
        
        is_free = lesson.get('is_free', False)
        is_subscribed = user.get('is_subscribed', False)
        
        if not is_free and not is_subscribed:
            message = f"🔒 *{lesson.get('title', 'الدرس')}*\n\n"
            message += lang.get('lesson_locked', 'هذا الدرس مدفوع. اشترك الآن للحصول على جميع الدروس!')\
                .replace('🔒', '') + "\n\n"
            message += f"💰 {lang.get('payment_info', 'سعر الاشتراك: 5$ للمستوى الكامل (18 درس)')}\n"
            message += f"🔗 {lang.get('payment_link', 'رابط الدفع:')} {Config.PAYMENT_LINK}"
            
            keyboard = [
                [InlineKeyboardButton("💰 اشترك الآن", url=Config.PAYMENT_LINK)],
                [InlineKeyboardButton("🔙 رجوع", callback_data=f"show_lessons_{level}")]
            ]
            reply_markup = InlineKeyboardMarkup(keyboard)
            
            await query.edit_message_text(message, reply_markup=reply_markup, parse_mode='Markdown')
            return
        
        # عرض محتوى الدرس
        content = lessons_manager.get_lesson_content_for_telegram(lesson, lang_code)
        
        keyboard = [
            [InlineKeyboardButton("📝 تدريب", callback_data=f"practice_lesson_{level}_{lesson_id}")],
            [InlineKeyboardButton("🔙 رجوع", callback_data=f"show_lessons_{level}")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await query.edit_message_text(content, reply_markup=reply_markup, parse_mode='Markdown')
        
        # إرسال الفيديو إذا وجد
        if lesson.get('video_url'):
            video_embed = lessons_manager.get_drive_file_embed(lesson['video_url'])
            if video_embed:
                try:
                    await query.message.reply_video(
                        video=video_embed,
                        caption="🎬 فيديو الدرس"
                    )
                except Exception as e:
                    logger.error(f"Error sending video: {e}")
                    await query.message.reply_text(f"🎬 رابط الفيديو: {lesson['video_url']}")
        
        # إرسال الصوت إذا وجد
        if lesson.get('audio_url'):
            audio_embed = lessons_manager.get_drive_file_embed(lesson['audio_url'])
            if audio_embed:
                try:
                    await query.message.reply_audio(
                        audio=audio_embed,
                        caption="🎵 تسجيل صوتي للدرس"
                    )
                except Exception as e:
                    logger.error(f"Error sending audio: {e}")
                    await query.message.reply_text(f"🎵 رابط الصوت: {lesson['audio_url']}")
        
        # إرسال الصورة إذا وجدت
        if lesson.get('image_url'):
            image_embed = lessons_manager.get_drive_file_embed(lesson['image_url'])
            if image_embed:
                try:
                    await query.message.reply_photo(
                        photo=image_embed,
                        caption="🖼️ صورة توضيحية"
                    )
                except Exception as e:
                    logger.error(f"Error sending image: {e}")
                    await query.message.reply_text(f"🖼️ رابط الصورة: {lesson['image_url']}")
    
    async def handle_practice(self, query, user_id: int, practice_type: str):
        """معالج التدريبات"""
        user = db.get_user(user_id)
        lang_code = user.get('language', 'ar')
        lang = LANGUAGES[lang_code]
        level = user.get('level', 'A1')
        
        if practice_type == 'conversation':
            # تدريب المحادثة
            conversation = ai_tutor.generate_conversation(level, language=lang_code)
            message = f"🗣️ *{lang.get('conversation_practice', 'تدريب المحادثة')}*\n\n"
            message += conversation
            message += "\n\n📝 *ملاحظة:* يمكنك كتابة أي نص وسأقوم بتصحيحه!"
            
            keyboard = [
                [InlineKeyboardButton("🔄 محادثة جديدة", callback_data="practice_conversation")],
                [InlineKeyboardButton("🔙 رجوع", callback_data="main_menu")]
            ]
            reply_markup = InlineKeyboardMarkup(keyboard)
            
            await query.edit_message_text(message, reply_markup=reply_markup, parse_mode='Markdown')
        
        elif practice_type == 'writing':
            # تدريب الكتابة
            topic = ai_tutor.generate_writing_prompt(level, lang_code)
            message = f"✍️ *{lang.get('writing_practice', 'تدريب الكتابة')}*\n\n"
            message += f"📝 *اكتب عن الموضوع التالي:*\n\n"
            message += f"_{topic}_\n\n"
            message += "📤 اكتب نصك في الرسالة التالية وسأقوم بتقييمه."
            
            keyboard = [
                [InlineKeyboardButton("🔄 موضوع جديد", callback_data="practice_writing")],
                [InlineKeyboardButton("🔙 رجوع", callback_data="main_menu")]
            ]
            reply_markup = InlineKeyboardMarkup(keyboard)
            
            await query.edit_message_text(message, reply_markup=reply_markup, parse_mode='Markdown')
            
            # حفظ حالة المستخدم لتلقي النص
            self.user_states[user_id] = 'writing_practice'
        
        elif practice_type.startswith('lesson_'):
            # تدريب درس معين
            parts = practice_type.split('_')
            level = parts[1]
            lesson_id = int(parts[2])
            
            lesson = lessons_manager.get_lesson(level, lesson_id)
            if lesson and lesson.get('exercises'):
                exercises = lesson['exercises']
                message = f"📝 *تدريب الدرس {lesson_id}*\n\n"
                for i, ex in enumerate(exercises[:3], 1):
                    message += f"{i}. {ex}\n"
                message += "\n✏️ أجب عن الأسئلة في رسالة جديدة."
                
                self.user_states[user_id] = f'exercise_{level}_{lesson_id}'
                
                keyboard = [[InlineKeyboardButton("🔙 رجوع", callback_data=f"lesson_{level}_{lesson_id}")]]
                reply_markup = InlineKeyboardMarkup(keyboard)
                
                await query.edit_message_text(message, reply_markup=reply_markup, parse_mode='Markdown')
            else:
                await query.edit_message_text(
                    "⚠️ لا توجد تدريبات لهذا الدرس حالياً",
                    reply_markup=InlineKeyboardMarkup([[
                        InlineKeyboardButton("🔙 رجوع", callback_data=f"lesson_{level}_{lesson_id}")
                    ]])
                )
    
    async def handle_correction(self, query, user_id: int):
        """معالج تصحيح النص"""
        self.user_states[user_id] = 'awaiting_correction'
        
        await query.edit_message_text(
            "📝 *أرسل النص الذي تريد تصحيحه*\n\n"
            "سأقوم بتصحيح الأخطاء الإملائية والنحوية.",
            parse_mode='Markdown'
        )
    
    async def handle_message(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """معالج الرسائل النصية"""
        user_id = update.effective_user.id
        text = update.message.text
        
        state = self.user_states.get(user_id)
        
        if state == 'writing_practice':
            # تقييم النص الكتابي
            user = db.get_user(user_id)
            level = user.get('level', 'A1')
            lang_code = user.get('language', 'ar')
            
            await update.message.reply_text("⏳ جاري تقييم النص...")
            
            evaluation = ai_tutor.evaluate_writing(text, level, lang_code)
            
            message = f"📝 *تقييم النص:*\n\n"
            message += evaluation
            
            keyboard = [[InlineKeyboardButton("📝 تدريب جديد", callback_data="practice_writing")]]
            reply_markup = InlineKeyboardMarkup(keyboard)
            
            await update.message.reply_text(message, reply_markup=reply_markup, parse_mode='Markdown')
            self.user_states[user_id] = None
        
        elif state == 'awaiting_correction':
            # تصحيح النص
            await update.message.reply_text("⏳ جاري التصحيح...")
            
            correction = ai_tutor.correct_text(text)
            
            message = f"🔍 *النص المصحح:*\n\n"
            message += correction
            
            keyboard = [[InlineKeyboardButton("📝 تصحيح جديد", callback_data="correct_text")]]
            reply_markup = InlineKeyboardMarkup(keyboard)
            
            await update.message.reply_text(message, reply_markup=reply_markup, parse_mode='Markdown')
            self.user_states[user_id] = None
        
        elif state == 'change_name':
            # تغيير الاسم
            db.update_user(user_id, first_name=text)
            self.user_states[user_id] = None
            
            await update.message.reply_text(
                f"✅ تم تغيير الاسم إلى: {text}\n\n"
                "📋 يمكنك عرض الملخص من القائمة الرئيسية.",
                reply_markup=InlineKeyboardMarkup([[
                    InlineKeyboardButton("📚 القائمة الرئيسية", callback_data="main_menu")
                ]])
            )
        
        elif state and state.startswith('exercise_'):
            # معالجة إجابات التدريبات
            parts = state.split('_')
            level = parts[1]
            lesson_id = int(parts[2])
            
            await update.message.reply_text(
                f"✅ تم استلام إجابتك!\n\n"
                f"📝 سيتم تقييم إجابتك قريباً.\n"
                f"📚 يمكنك متابعة دروسك من القائمة الرئيسية.",
                reply_markup=InlineKeyboardMarkup([[
                    InlineKeyboardButton("📚 القائمة الرئيسية", callback_data="main_menu")
                ]])
            )
            self.user_states[user_id] = None
        
        else:
            # رسالة عادية - عرض القائمة
            await update.message.reply_text(
                "👋 استخدم الأزرار للتنقل في البوت، أو اكتب /menu للقائمة الرئيسية.",
                reply_markup=InlineKeyboardMarkup([[
                    InlineKeyboardButton("📚 القائمة الرئيسية", callback_data="main_menu")
                ]])
            )
    
    async def settings_callback(self, query, user_id: int):
        """عرض الإعدادات"""
        user = db.get_user(user_id)
        lang_code = user.get('language', 'ar')
        lang = LANGUAGES[lang_code]
        
        message = f"⚙️ *الإعدادات*\n\n"
        message += f"{lang.get('name_label', '👤 الاسم')} {user.get('first_name', '')}\n"
        message += f"{lang.get('level_label', '📚 المستوى')} {user.get('level', 'غير محدد')}\n"
        message += f"{lang.get('time_label', '⏰ وقت الدرس')} {user.get('lesson_time', 'غير محدد')}\n"
        message += f"{lang.get('days_off_label', '📅 أيام الإجازة')} {', '.join(user.get('days_off', [])) if user.get('days_off') else 'غير محددة'}\n\n"
        
        message += "🔧 *اختر ما تريد تغييره:*"
        
        keyboard = [
            [
                InlineKeyboardButton(lang.get('change_name', 'تغيير الاسم'), callback_data="change_name"),
                InlineKeyboardButton(lang.get('change_level', 'تغيير المستوى'), callback_data="change_level")
            ],
            [
                InlineKeyboardButton(lang.get('change_time', 'تغيير الوقت'), callback_data="change_time"),
                InlineKeyboardButton(lang.get('change_days', 'تغيير أيام الإجازة'), callback_data="change_days")
            ],
            [InlineKeyboardButton("🔙 رجوع", callback_data="main_menu")]
        ]
        
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await query.edit_message_text(message, reply_markup=reply_markup, parse_mode='Markdown')
    
    async def settings_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """عرض الإعدادات عبر الأمر"""
        user_id = update.effective_user.id
        user = db.get_user(user_id)
        lang_code = user.get('language', 'ar')
        lang = LANGUAGES[lang_code]
        
        message = f"⚙️ *الإعدادات*\n\n"
        message += f"{lang.get('name_label', '👤 الاسم')} {user.get('first_name', '')}\n"
        message += f"{lang.get('level_label', '📚 المستوى')} {user.get('level', 'غير محدد')}\n"
        message += f"{lang.get('time_label', '⏰ وقت الدرس')} {user.get('lesson_time', 'غير محدد')}\n"
        message += f"{lang.get('days_off_label', '📅 أيام الإجازة')} {', '.join(user.get('days_off', [])) if user.get('days_off') else 'غير محددة'}\n\n"
        
        message += "🔧 *اختر ما تريد تغييره:*"
        
        keyboard = [
            [
                InlineKeyboardButton(lang.get('change_name', 'تغيير الاسم'), callback_data="change_name"),
                InlineKeyboardButton(lang.get('change_level', 'تغيير المستوى'), callback_data="change_level")
            ],
            [
                InlineKeyboardButton(lang.get('change_time', 'تغيير الوقت'), callback_data="change_time"),
                InlineKeyboardButton(lang.get('change_days', 'تغيير أيام الإجازة'), callback_data="change_days")
            ],
            [InlineKeyboardButton("🔙 رجوع", callback_data="main_menu")]
        ]
        
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await update.message.reply_text(message, reply_markup=reply_markup, parse_mode='Markdown')
    
    async def handle_setting_change(self, query, user_id: int, setting: str):
        """معالج تغيير الإعدادات"""
        user = db.get_user(user_id)
        lang_code = user.get('language', 'ar')
        lang = LANGUAGES[lang_code]
        
        if setting == 'name':
            await query.edit_message_text(
                "✏️ *أرسل اسمك الجديد*\n\n"
                "اكتب اسمك في رسالة جديدة.",
                parse_mode='Markdown'
            )
            self.user_states[user_id] = 'change_name'
        
        elif setting == 'level':
            # عرض اختيار المستوى
            keyboard = []
            for level in ['A0', 'A1', 'A2', 'B1', 'B2']:
                keyboard.append([InlineKeyboardButton(f"📚 {level}", callback_data=f"level_{level}")])
            keyboard.append([InlineKeyboardButton("🔙 رجوع", callback_data="settings")])
            
            reply_markup = InlineKeyboardMarkup(keyboard)
            
            await query.edit_message_text(
                f"📚 *{lang.get('choose_level', 'اختر مستواك')}*",
                reply_markup=reply_markup,
                parse_mode='Markdown'
            )
        
        elif setting == 'time':
            # عرض اختيار الوقت
            keyboard = []
            for hour in range(0, 24):
                time_str = f"{hour:02d}:00"
                keyboard.append([InlineKeyboardButton(f"🕐 {time_str}", callback_data=f"time_{time_str}")])
            keyboard.append([InlineKeyboardButton("🔙 رجوع", callback_data="settings")])
            
            reply_markup = InlineKeyboardMarkup(keyboard)
            
            await query.edit_message_text(
                f"⏰ *{lang.get('choose_time', 'اختر وقت إرسال الدرس')}*",
                reply_markup=reply_markup,
                parse_mode='Markdown'
            )
        
        elif setting == 'days':
            # عرض اختيار أيام الإجازة
            days = Config.DAYS_OF_WEEK.get(lang_code, Config.DAYS_OF_WEEK['en'])
            days_off = user.get('days_off', [])
            
            message = f"📅 *{lang.get('choose_days_off', 'اختر أيام الإجازة')}*\n\n"
            message += f"✅ تم اختيار: {', '.join(days_off) if days_off else 'لم يتم اختيار أي يوم'}\n"
            message += f"📌 يمكنك اختيار يومين كحد أقصى\n\n"
            
            keyboard = []
            for day in days:
                is_selected = day in days_off
                button_text = f"✅ {day}" if is_selected else f"⬜ {day}"
                keyboard.append([InlineKeyboardButton(button_text, callback_data=f"dayoff_{day}")])
            
            keyboard.append([
                InlineKeyboardButton("✅ تأكيد", callback_data="confirm_days_off"),
                InlineKeyboardButton("🔙 رجوع", callback_data="settings")
            ])
            
            reply_markup = InlineKeyboardMarkup(keyboard)
            
            await query.edit_message_text(
                message,
                reply_markup=reply_markup,
                parse_mode='Markdown'
            )
    
    async def menu_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """عرض القائمة الرئيسية عبر الأمر"""
        user_id = update.effective_user.id
        await self.show_main_menu_inline(update, user_id)
    
    async def show_main_menu_inline(self, update, user_id: int):
        """عرض القائمة الرئيسية في رسالة جديدة"""
        user = db.get_user(user_id)
        lang_code = user.get('language', 'ar')
        lang = LANGUAGES[lang_code]
        
        message = f"📚 *{lang.get('main_menu', 'القائمة الرئيسية')}*\n\n"
        message += "اختر ما تريد القيام به:"
        
        keyboard = [
            [InlineKeyboardButton("📖 عرض المستويات", callback_data="show_levels")],
            [InlineKeyboardButton("📚 دروسي", callback_data="my_lessons")],
            [InlineKeyboardButton("🗣️ تدريب المحادثة", callback_data="practice_conversation")],
            [InlineKeyboardButton("✍️ تدريب الكتابة", callback_data="practice_writing")],
            [InlineKeyboardButton("🔍 تصحيح النص", callback_data="correct_text")],
            [InlineKeyboardButton("⚙️ الإعدادات", callback_data="settings")],
            [InlineKeyboardButton("📊 تقدمي", callback_data="progress")]
        ]
        
        # إضافة زر التصدير للأدمن
        if user_id == Config.ADMIN_ID:
            keyboard.append([InlineKeyboardButton("📊 تصدير بيانات الطلاب", callback_data="admin_export")])
        
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await update.message.reply_text(message, reply_markup=reply_markup, parse_mode='Markdown')
    
    async def lessons_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """عرض دروس المستخدم"""
        user_id = update.effective_user.id
        user = db.get_user(user_id)
        level = user.get('level', 'A1')
        
        await self.show_lessons_for_user(update, user_id, level)
    
    async def show_lessons_for_user(self, update, user_id: int, level: str):
        """عرض دروس المستخدم"""
        user = db.get_user(user_id)
        lang_code = user.get('language', 'ar')
        lang = LANGUAGES[lang_code]
        
        lessons = lessons_manager.get_level_lessons(level)
        completed_lessons = db.get_completed_lessons(user_id)
        
        message = f"📚 *مستوى {level}*\n\n"
        
        keyboard = []
        for lesson in lessons[:10]:
            is_completed = lesson['id'] in completed_lessons
            is_free = lesson.get('is_free', False)
            status = "✅" if is_completed else "📖"
            if not is_free and not user.get('is_subscribed', False):
                status = "🔒"
            button_text = f"{status} {lesson['id']}. {lesson.get('title', '')}"
            keyboard.append([InlineKeyboardButton(button_text, callback_data=f"lesson_{level}_{lesson['id']}")])
        
        if len(lessons) > 10:
            keyboard.append([InlineKeyboardButton("📖 عرض المزيد...", callback_data=f"more_lessons_{level}_10")])
        
        keyboard.append([InlineKeyboardButton("🔙 رجوع", callback_data="main_menu")])
        
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await update.message.reply_text(message, reply_markup=reply_markup, parse_mode='Markdown')
    
    async def practice_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """عرض خيارات التدريب"""
        user_id = update.effective_user.id
        user = db.get_user(user_id)
        lang_code = user.get('language', 'ar')
        lang = LANGUAGES[lang_code]
        
        message = f"🗣️ *التدريبات*\n\n"
        message += "اختر نوع التدريب:"
        
        keyboard = [
            [InlineKeyboardButton("🗣️ تدريب المحادثة", callback_data="practice_conversation")],
            [InlineKeyboardButton("✍️ تدريب الكتابة", callback_data="practice_writing")],
            [InlineKeyboardButton("🔍 تصحيح النص", callback_data="correct_text")],
            [InlineKeyboardButton("🔙 رجوع", callback_data="main_menu")]
        ]
        
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await update.message.reply_text(message, reply_markup=reply_markup, parse_mode='Markdown')
    
    async def progress_callback(self, query, user_id: int):
        """عرض التقدم"""
        user = db.get_user(user_id)
        level = user.get('level', 'A1')
        
        lessons = lessons_manager.get_level_lessons(level)
        completed_lessons = db.get_completed_lessons(user_id)
        
        total = len(lessons)
        completed = len(completed_lessons)
        progress = (completed / total * 100) if total > 0 else 0
        
        message = f"📊 *تقدمك في التعلم*\n\n"
        message += f"📚 المستوى: {level}\n"
        message += f"📖 الدروس المكتملة: {completed}/{total}\n"
        message += f"📈 نسبة التقدم: {progress:.1f}%\n\n"
        
        # شريط التقدم
        bar_length = 20
        filled = int(progress / 100 * bar_length)
        bar = "█" * filled + "░" * (bar_length - filled)
        message += f"`{bar}`\n\n"
        
        if user.get('is_subscribed', False):
            message += "✅ *مشترك* - لديك حق الوصول لجميع الدروس"
        else:
            message += f"🔓 *دروس مجانية*: {min(5, total - completed)} دروس متبقية\n"
            message += f"💰 اشترك للحصول على جميع الدروس: {Config.PAYMENT_LINK}"
        
        keyboard = [[InlineKeyboardButton("🔙 رجوع", callback_data="main_menu")]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await query.edit_message_text(message, reply_markup=reply_markup, parse_mode='Markdown')
    
    async def progress_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """عرض التقدم عبر الأمر"""
        user_id = update.effective_user.id
        user = db.get_user(user_id)
        level = user.get('level', 'A1')
        
        lessons = lessons_manager.get_level_lessons(level)
        completed_lessons = db.get_completed_lessons(user_id)
        
        total = len(lessons)
        completed = len(completed_lessons)
        progress = (completed / total * 100) if total > 0 else 0
        
        message = f"📊 *تقدمك في التعلم*\n\n"
        message += f"📚 المستوى: {level}\n"
        message += f"📖 الدروس المكتملة: {completed}/{total}\n"
        message += f"📈 نسبة التقدم: {progress:.1f}%\n\n"
        
        # شريط التقدم
        bar_length = 20
        filled = int(progress / 100 * bar_length)
        bar = "█" * filled + "░" * (bar_length - filled)
        message += f"`{bar}`\n\n"
        
        if user.get('is_subscribed', False):
            message += "✅ *مشترك* - لديك حق الوصول لجميع الدروس"
        else:
            message += f"🔓 *دروس مجانية*: {min(5, total - completed)} دروس متبقية\n"
            message += f"💰 اشترك للحصول على جميع الدروس: {Config.PAYMENT_LINK}"
        
        keyboard = [[InlineKeyboardButton("🔙 رجوع", callback_data="main_menu")]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await update.message.reply_text(message, reply_markup=reply_markup, parse_mode='Markdown')
    
    # ========== دالة تصدير بيانات الطلاب للأدمن ==========
    async def export_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """تصدير بيانات الطلاب إلى Excel وإرسالها للأدمن"""
        user_id = update.effective_user.id
        
        # التحقق من صلاحيات الأدمن
        if user_id != Config.ADMIN_ID:
            await update.message.reply_text("⚠️ هذا الأمر مخصص للأدمن فقط.")
            return
        
        await update.message.reply_text("⏳ جاري تصدير بيانات الطلاب...")
        
        try:
            # تصدير البيانات إلى Excel
            excel_data = excel_exporter.export_users_to_excel()
            stats = excel_exporter.get_user_stats()
            
            # إرسال الملف
            await update.message.reply_document(
                document=excel_data,
                filename=f'students_data_{datetime.now().strftime("%Y%m%d_%H%M%S")}.xlsx',
                caption=f"📊 *إحصائيات الطلاب*\n\n"
                       f"👥 إجمالي الطلاب: {stats['total_users']}\n"
                       f"✅ المشتركين: {stats['subscribed_users']}\n"
                       f"❌ غير المشتركين: {stats['free_users']}\n\n"
                       f"📚 المستويات:\n"
                       + "\n".join([f"• {k}: {v}" for k, v in stats['levels'].items()])
            )
        except Exception as e:
            logger.error(f"Error exporting data: {e}")
            await update.message.reply_text(f"⚠️ حدث خطأ في تصدير البيانات: {e}")
    
    # ========== معالج تصدير البيانات من الأزرار ==========
    async def export_callback(self, query, user_id: int):
        """معالج تصدير البيانات من الأزرار"""
        # التحقق من صلاحيات الأدمن
        if user_id != Config.ADMIN_ID:
            await query.edit_message_text("⚠️ هذا الأمر مخصص للأدمن فقط.")
            return
        
        await query.edit_message_text("⏳ جاري تصدير بيانات الطلاب...")
        
        try:
            # تصدير البيانات إلى Excel
            excel_data = excel_exporter.export_users_to_excel()
            stats = excel_exporter.get_user_stats()
            
            # إرسال الملف
            await query.message.reply_document(
                document=excel_data,
                filename=f'students_data_{datetime.now().strftime("%Y%m%d_%H%M%S")}.xlsx',
                caption=f"📊 *إحصائيات الطلاب*\n\n"
                       f"👥 إجمالي الطلاب: {stats['total_users']}\n"
                       f"✅ المشتركين: {stats['subscribed_users']}\n"
                       f"❌ غير المشتركين: {stats['free_users']}\n\n"
                       f"📚 المستويات:\n"
                       + "\n".join([f"• {k}: {v}" for k, v in stats['levels'].items()])
            )
            
            await query.edit_message_text("✅ تم تصدير البيانات بنجاح!")
        except Exception as e:
            logger.error(f"Error exporting data: {e}")
            await query.edit_message_text(f"⚠️ حدث خطأ في تصدير البيانات: {e}")

def main():
    """الدالة الرئيسية لتشغيل البوت"""
    bot = ArabicLearningBot()
    bot.run()

if __name__ == '__main__':
    main()
