from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger
from datetime import datetime, timedelta
import pytz
from database import Database
from lessons import lessons_manager
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class LessonScheduler:
    def __init__(self, bot_instance):
        self.scheduler = BackgroundScheduler()
        self.db = Database()
        self.bot = bot_instance
        self._setup_jobs()
    
    def _setup_jobs(self):
        """إعداد المهام المجدولة"""
        # جدولة مهمة كل دقيقة للتحقق من الدروس المستحقة
        self.scheduler.add_job(
            self.check_lessons,
            CronTrigger(minute='*'),  # كل دقيقة
            id='check_lessons',
            replace_existing=True
        )
        
        # جدولة مهمة كل يوم للتنظيف
        self.scheduler.add_job(
            self.cleanup,
            CronTrigger(hour=3, minute=0),  # الساعة 3 صباحاً
            id='cleanup',
            replace_existing=True
        )
        
        # بدء الجدولة
        self.scheduler.start()
        logger.info("Scheduler started successfully")
    
    def check_lessons(self):
        """التحقق من الدروس المستحقة لكل مستخدم"""
        now = datetime.now()
        current_time = now.strftime("%H:%M")
        current_day = now.strftime("%A")  # يوم باللغة الإنجليزية
        
        try:
            # الحصول على المستخدمين الذين لديهم درس في هذا الوقت
            hour, minute = current_time.split(':')
            users = self.db.get_users_by_time(int(hour), int(minute))
            
            for user in users:
                try:
                    # التحقق من أن اليوم ليس يوم إجازة
                    days_off = user.get('days_off', [])
                    if current_day in days_off or current_day.lower() in [d.lower() for d in days_off]:
                        # يوم إجازة، تخطي إرسال الدرس
                        continue
                    
                    # إرسال الدرس للمستخدم
                    self.send_lesson(user)
                    
                except Exception as e:
                    logger.error(f"Error processing user {user.get('user_id')}: {e}")
                    continue
                    
        except Exception as e:
            logger.error(f"Error in check_lessons: {e}")
    
    def send_lesson(self, user):
        """إرسال الدرس للمستخدم"""
        try:
            user_id = user['user_id']
            level = user.get('level', 'A1')
            current_lesson = user.get('current_lesson', 0)
            language = user.get('language', 'ar')
            is_subscribed = user.get('is_subscribed', False)
            
            # الحصول على الدرس التالي
            lesson = lessons_manager.get_next_lesson(level, current_lesson)
            
            if not lesson:
                # لا يوجد دروس جديدة، إرسال رسالة إكمال المستوى
                self.bot.send_message(
                    chat_id=user_id,
                    text="🎉 مبروك! لقد أكملت جميع دروس هذا المستوى."
                )
                return
            
            # التحقق من إذا كان الدرس مدفوعاً
            if not lesson.get('is_free', False) and not is_subscribed:
                # إرسال رسالة الدفع
                payment_message = (
                    f"🔒 *{lesson.get('title', 'الدرس')}*\n\n"
                    "هذا الدرس مدفوع. يرجى الاشتراك للحصول على جميع الدروس!\n\n"
                    f"💰 سعر الاشتراك: 5$ للمستوى الكامل\n"
                    f"🔗 [اضغط هنا للاشتراك]({Config.PAYMENT_LINK})"
                )
                self.bot.send_message(
                    chat_id=user_id,
                    text=payment_message,
                    parse_mode='Markdown'
                )
                return
            
            # إرسال محتوى الدرس
            content = lessons_manager.get_lesson_content_for_telegram(lesson, language)
            
            # إرسال النص
            self.bot.send_message(
                chat_id=user_id,
                text=content,
                parse_mode='Markdown'
            )
            
            # إرسال الفيديو إذا وجد
            if lesson.get('video_url'):
                video_embed = lessons_manager.get_drive_file_embed(lesson['video_url'])
                if video_embed:
                    try:
                        self.bot.send_video(
                            chat_id=user_id,
                            video=video_embed,
                            caption="🎬 فيديو الدرس"
                        )
                    except Exception as e:
                        logger.error(f"Error sending video: {e}")
                        self.bot.send_message(
                            chat_id=user_id,
                            text=f"🎬 رابط الفيديو: {lesson['video_url']}"
                        )
            
            # إرسال الصوت إذا وجد
            if lesson.get('audio_url'):
                audio_embed = lessons_manager.get_drive_file_embed(lesson['audio_url'])
                if audio_embed:
                    try:
                        self.bot.send_audio(
                            chat_id=user_id,
                            audio=audio_embed,
                            caption="🎵 تسجيل صوتي للدرس"
                        )
                    except Exception as e:
                        logger.error(f"Error sending audio: {e}")
                        self.bot.send_message(
                            chat_id=user_id,
                            text=f"🎵 رابط الصوت: {lesson['audio_url']}"
                        )
            
            # إرسال الصورة إذا وجدت
            if lesson.get('image_url'):
                image_embed = lessons_manager.get_drive_file_embed(lesson['image_url'])
                if image_embed:
                    try:
                        self.bot.send_photo(
                            chat_id=user_id,
                            photo=image_embed,
                            caption="🖼️ صورة توضيحية"
                        )
                    except Exception as e:
                        logger.error(f"Error sending image: {e}")
                        self.bot.send_message(
                            chat_id=user_id,
                            text=f"🖼️ رابط الصورة: {lesson['image_url']}"
                        )
            
            # تحديث الدرس الحالي للمستخدم
            self.db.update_user(user_id, current_lesson=lesson['id'])
            
            # تسجيل إكمال الدرس
            self.db.record_lesson_completion(user_id, lesson['id'])
            
            logger.info(f"Lesson {lesson['id']} sent to user {user_id}")
            
        except Exception as e:
            logger.error(f"Error sending lesson: {e}")
    
    def cleanup(self):
        """تنظيف المهام القديمة"""
        logger.info("Running cleanup job")
    
    def stop(self):
        """إيقاف الجدولة"""
        self.scheduler.shutdown()
