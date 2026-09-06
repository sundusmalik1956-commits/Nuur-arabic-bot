import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    BOT_TOKEN = os.getenv('BOT_TOKEN')
    GEMINI_API_KEYS = [
        os.getenv('GEMINI_API_KEY_1'),
        os.getenv('GEMINI_API_KEY_2'),
        os.getenv('GEMINI_API_KEY_3')
    ]
    ADMIN_ID = int(os.getenv('ADMIN_ID'))
    PAYMENT_LINK = os.getenv('PAYMENT_LINK')
    WOMEN_GROUP = os.getenv('WOMEN_GROUP')
    MEN_GROUP = os.getenv('MEN_GROUP')
    LEVEL_TEST_BOT = os.getenv('LEVEL_TEST_BOT')
    
    # إعدادات الدروس
    LESSONS_PER_LEVEL = 18
    FREE_LESSONS = 5
    SUBSCRIPTION_PRICE = 5
    LEVELS = ['A0', 'A1', 'A2', 'B1', 'B2']
    
    # جدول الأوقات المتاحة (24 ساعة)
    AVAILABLE_TIMES = [f"{i:02d}:00" for i in range(24)]
    
    # أيام الأسبوع
    DAYS_OF_WEEK = {
        'en': ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'],
        'ar': ['الإثنين', 'الثلاثاء', 'الأربعاء', 'الخميس', 'الجمعة', 'السبت', 'الأحد'],
        'tr': ['Pazartesi', 'Salı', 'Çarşamba', 'Perşembe', 'Cuma', 'Cumartesi', 'Pazar'],
        'es': ['Lunes', 'Martes', 'Miércoles', 'Jueves', 'Viernes', 'Sábado', 'Domingo'],
        'fr': ['Lundi', 'Mardi', 'Mercredi', 'Jeudi', 'Vendredi', 'Samedi', 'Dimanche'],
        'ru': ['Понедельник', 'Вторник', 'Среда', 'Четверг', 'Пятница', 'Суббота', 'Воскресенье'],
        'zh': ['周一', '周二', '周三', '周四', '周五', '周六', '周日'],
        'ur': ['پیر', 'منگل', 'بدھ', 'جمعرات', 'جمعہ', 'ہفتہ', 'اتوار'],
        'hi': ['सोमवार', 'मंगलवार', 'बुधवार', 'गुरुवार', 'शुक्रवार', 'शनिवार', 'रविवार'],
        'fa': ['دوشنبه', 'سه‌شنبه', 'چهارشنبه', 'پنجشنبه', 'جمعه', 'شنبه', 'یکشنبه'],
        'id': ['Senin', 'Selasa', 'Rabu', 'Kamis', 'Jumat', 'Sabtu', 'Minggu']
    }
