# translations.py
from typing import Dict, List

# ترجمات الواجهة
TRANSLATIONS = {
    'ar': {
        # رسائل عامة
        'start': "👋 مرحباً بك في نور بوت!\n\nاختر لغة التعليم:",
        'language_selected': "✅ تم اختيار اللغة: {}",
        'choose_time': "⏰ اختر وقت استلام الدروس اليومية:",
        'time_selected': "✅ تم حفظ الوقت: {}\n\nسيتم إرسال الدروس في هذا الوقت يومياً (الأحد - الخميس).",
        'main_menu': "🏠 القائمة الرئيسية\n\n👤 مرحباً {name}!\n📚 الدرس الحالي: {current}\n✅ الدروس المكتملة: {completed}/18",
        'continue_lesson': "📖 متابعة الدرس",
        'progress': "📊 التقدم",
        'settings': "⚙️ الإعدادات",
        'back': "🔙 رجوع",
        'lesson_not_found': "❌ الدرس غير موجود. الرجاء المحاولة مرة أخرى.",
        'lesson_completed': "🎉 مبروك! لقد أكملت الدرس {lesson} بنجاح!",
        'next_lesson': "📚 الدرس التالي: {next}\nسيتم إرساله في الوقت المحدد.",
        'subscription_expired': """🎓 انتهت الفترة التجريبية المجانية.

البرنامج الكامل مدفوع.
السعر: 5$

للاشتراك، يرجى التواصل مع الدعم:
@NoorBotSupport""",
        'subscription_info': "📚 معلومات الاشتراك",
        
        # التقدم
        'progress_details': """📊 **تقدمك في البرنامج**

الدروس المكتملة: {completed}/{total}
النسبة المئوية: {percentage:.1f}%

{progress_bar}

الدرس الحالي: {current}""",
        
        # الإعدادات
        'settings_menu': "⚙️ **الإعدادات**\n\nاختر الإعداد الذي تريد تعديله:",
        'change_language': "🌐 تغيير اللغة",
        'change_time': "⏰ تغيير وقت الدرس",
        'select_language': "🌐 اختر اللغة:",
        'choose_new_time': "⏰ اختر الوقت الجديد:",
        'language_updated': "✅ تم تغيير اللغة إلى: {}",
        'time_updated': "✅ تم تغيير وقت الدرس إلى: {}",
        
        # إعلانات الإنجاز
        'achievement_announcement': """🎉 **إنجاز جديد في نور بوت!**

👤 الطالب: {name}
📚 أتم الدرس {lesson_num}: {lesson_name}

🌟 أحسنت! استمر في التعلم.""",
        
        # أسماء الدروس
        'lesson_1_name': 'التعريف بالنفس',
        'lesson_2_name': 'العائلة والأصدقاء',
        'lesson_3_name': 'الحياة اليومية',
        'lesson_4_name': 'الطعام والشراب',
        'lesson_5_name': 'السفر والتنقل',
        'lesson_6_name': 'التسوق',
        'lesson_7_name': 'الصحة',
        'lesson_8_name': 'الترفيه',
        'lesson_9_name': 'العمل والمهنة',
        'lesson_10_name': 'التعليم',
        'lesson_11_name': 'الطقس والفصول',
        'lesson_12_name': 'المنزل',
        'lesson_13_name': 'الملابس',
        'lesson_14_name': 'الرياضة',
        'lesson_15_name': 'التكنولوجيا',
        'lesson_16_name': 'الثقافة',
        'lesson_17_name': 'الطبيعة',
        'lesson_18_name': 'المستقبل والأحلام',
        
        # أزرار الدروس
        'start_quiz': "📝 بدء الاختبار",
        'start_lesson': "📖 بدء الدرس",
        
        # رسائل الشهادة
        'certificate_completion': """🎓 **شهادة إتمام البرنامج**

تهانينا {name}!

لقد أكملت بنجاح برنامج نور بوت لتعليم اللغة العربية.
18 درساً من التعلم المكثف.

🌟 أنت الآن قادر على:
• التحدث بالعربية في المواقف اليومية
• فهم النصوص العربية
• كتابة نصوص بالعربية

استمر في التعلم والتطور!""",
        
        # رسائل التدريبات
        'correct_answer': "✅ صحيح!",
        'wrong_answer': "❌ غير صحيح. حاول مرة أخرى.",
        'quiz_completed': "🎉 أحسنت! لقد أكملت جميع التدريبات.",
        'try_again': "🔄 حاول مرة أخرى",
        
        # رسائل المحادثة والكتابة
        'conversation_start': "💬 بدأ المحادثة",
        'writing_submit': "✍️ أرسل كتابتك"
    },
    'en': {
        # General messages
        'start': "👋 Welcome to Noor Bot!\n\nChoose your language:",
        'language_selected': "✅ Language selected: {}",
        'choose_time': "⏰ Choose your daily lesson time:",
        'time_selected': "✅ Time saved: {}\n\nLessons will be sent at this time daily (Sunday - Thursday).",
        'main_menu': "🏠 Main Menu\n\n👤 Welcome {name}!\n📚 Current lesson: {current}\n✅ Completed lessons: {completed}/18",
        'continue_lesson': "📖 Continue Lesson",
        'progress': "📊 Progress",
        'settings': "⚙️ Settings",
        'back': "🔙 Back",
        'lesson_not_found': "❌ Lesson not found. Please try again.",
        'lesson_completed': "🎉 Congratulations! You have completed lesson {lesson} successfully!",
        'next_lesson': "📚 Next lesson: {next}\nIt will be sent at the scheduled time.",
        'subscription_expired': """🎓 The free trial period has ended.

The full program is paid.
Price: $5

To subscribe, please contact support:
@NoorBotSupport""",
        'subscription_info': "📚 Subscription Information",
        
        # Progress
        'progress_details': """📊 **Your Progress**

Completed lessons: {completed}/{total}
Percentage: {percentage:.1f}%

{progress_bar}

Current lesson: {current}""",
        
        # Settings
        'settings_menu': "⚙️ **Settings**\n\nChoose what you want to change:",
        'change_language': "🌐 Change Language",
        'change_time': "⏰ Change Lesson Time",
        'select_language': "🌐 Select language:",
        'choose_new_time': "⏰ Choose new time:",
        'language_updated': "✅ Language changed to: {}",
        'time_updated': "✅ Lesson time changed to: {}",
        
        # Achievement announcements
        'achievement_announcement': """🎉 **New Achievement in Noor Bot!**

👤 Student: {name}
📚 Completed lesson {lesson_num}: {lesson_name}

🌟 Well done! Keep learning.""",
        
        # Lesson names
        'lesson_1_name': 'Self Introduction',
        'lesson_2_name': 'Family and Friends',
        'lesson_3_name': 'Daily Life',
        'lesson_4_name': 'Food and Drink',
        'lesson_5_name': 'Travel',
        'lesson_6_name': 'Shopping',
        'lesson_7_name': 'Health',
        'lesson_8_name': 'Entertainment',
        'lesson_9_name': 'Work',
        'lesson_10_name': 'Education',
        'lesson_11_name': 'Weather and Seasons',
        'lesson_12_name': 'Home',
        'lesson_13_name': 'Clothing',
        'lesson_14_name': 'Sports',
        'lesson_15_name': 'Technology',
        'lesson_16_name': 'Culture',
        'lesson_17_name': 'Nature',
        'lesson_18_name': 'Future and Dreams',
        
        # Lesson buttons
        'start_quiz': "📝 Start Quiz",
        'start_lesson': "📖 Start Lesson",
        
        # Certificate messages
        'certificate_completion': """🎓 **Certificate of Completion**

Congratulations {name}!

You have successfully completed the Noor Bot Arabic Language Program.
18 lessons of intensive learning.

🌟 You are now able to:
• Speak Arabic in daily situations
• Understand Arabic texts
• Write in Arabic

Keep learning and growing!""",
        
        # Quiz messages
        'correct_answer': "✅ Correct!",
        'wrong_answer': "❌ Not correct. Try again.",
        'quiz_completed': "🎉 Well done! You have completed all exercises.",
        'try_again': "🔄 Try again",
        
        # Conversation and writing
        'conversation_start': "💬 Conversation started",
        'writing_submit': "✍️ Submit your writing"
    },
    'tr': {
        # Genel mesajlar
        'start': "👻 Noor Bot'a Hoş Geldiniz!\n\nEğitim dilinizi seçin:",
        'language_selected': "✅ Dil seçildi: {}",
        'choose_time': "⏰ Günlük ders saatinizi seçin:",
        'time_selected': "✅ Saat kaydedildi: {}\n\nDersler her gün bu saatte gönderilecektir (Pazar - Perşembe).",
        'main_menu': "🏠 Ana Menü\n\n👻 Hoş geldin {name}!\n📚 Mevcut ders: {current}\n✅ Tamamlanan dersler: {completed}/18",
        'continue_lesson': "📖 Derse Devam Et",
        'progress': "📊 İlerleme",
        'settings': "⚙️ Ayarlar",
        'back': "🔙 Geri",
        'lesson_not_found': "❌ Ders bulunamadı. Lütfen tekrar deneyin.",
        'lesson_completed': "🎉 Tebrikler! {lesson}. dersi başarıyla tamamladınız!",
        'next_lesson': "📚 Sonraki ders: {next}\nBelirlenen saatte gönderilecektir.",
        'subscription_expired': """🎓 Ücretsiz deneme süresi sona erdi.

Tam program ücretlidir.
Fiyat: 5$

Abone olmak için destek ile iletişime geçin:
@NoorBotSupport""",
        'subscription_info': "📚 Abonelik Bilgileri",
        
        # İlerleme
        'progress_details': """📊 **İlerlemeniz**

Tamamlanan dersler: {completed}/{total}
Yüzde: {percentage:.1f}%

{progress_bar}

Mevcut ders: {current}""",
        
        # Ayarlar
        'settings_menu': "⚙️ **Ayarlar**\n\nDeğiştirmek istediğiniz ayarı seçin:",
        'change_language': "🌐 Dili Değiştir",
        'change_time': "⏰ Ders Saatini Değiştir",
        'select_language': "🌐 Dil seçin:",
        'choose_new_time': "⏰ Yeni saat seçin:",
        'language_updated': "✅ Dil değiştirildi: {}",
        'time_updated': "✅ Ders saati değiştirildi: {}",
        
        # Başarı duyuruları
        'achievement_announcement': """🎉 **Noor Bot'ta Yeni Başarı!**

👤 Öğrenci: {name}
📚 {lesson_num}. dersi tamamladı: {lesson_name}

🌟 Aferin! Öğrenmeye devam et.""",
        
        # Ders isimleri
        'lesson_1_name': 'Kendini Tanıtma',
        'lesson_2_name': 'Aile ve Arkadaşlar',
        'lesson_3_name': 'Günlük Hayat',
        'lesson_4_name': 'Yemek ve İçecek',
        'lesson_5_name': 'Seyahat',
        'lesson_6_name': 'Alışveriş',
        'lesson_7_name': 'Sağlık',
        'lesson_8_name': 'Eğlence',
        'lesson_9_name': 'İş',
        'lesson_10_name': 'Eğitim',
        'lesson_11_name': 'Hava ve Mevsimler',
        'lesson_12_name': 'Ev',
        'lesson_13_name': 'Giyim',
        'lesson_14_name': 'Spor',
        'lesson_15_name': 'Teknoloji',
        'lesson_16_name': 'Kültür',
        'lesson_17_name': 'Doğa',
        'lesson_18_name': 'Gelecek ve Hayaller',
        
        # Ders butonları
        'start_quiz': "📝 Teste Başla",
        'start_lesson': "📖 Derse Başla",
        
        # Sertifika mesajları
        'certificate_completion': """🎓 **Tamamlama Sertifikası**

Tebrikler {name}!

Noor Bot Arapça Dil Programını başarıyla tamamladınız.
18 ders yoğun öğrenme.

🌟 Artık şunları yapabiliyorsunuz:
• Günlük durumlarda Arapça konuşma
• Arapça metinleri anlama
• Arapça yazma

Öğrenmeye ve gelişmeye devam edin!""",
        
        # Test mesajları
        'correct_answer': "✅ Doğru!",
        'wrong_answer': "❌ Yanlış. Tekrar dene.",
        'quiz_completed': "🎉 Aferin! Tüm alıştırmaları tamamladınız.",
        'try_again': "🔄 Tekrar dene",
        
        # Konuşma ve yazma
        'conversation_start': "💬 Konuşma başladı",
        'writing_submit': "✍️ Yazınızı gönderin"
    }
}

def get_text(key: str, lang: str = 'ar') -> str:
    """الحصول على النص المترجم"""
    if lang in TRANSLATIONS:
        return TRANSLATIONS[lang].get(key, key)
    return TRANSLATIONS['ar'].get(key, key)

def get_languages() -> Dict[str, str]:
    """الحصول على قائمة اللغات المدعومة"""
    return {
        'ar': 'العربية',
        'en': 'English',
        'tr': 'Türkçe'
    }

def get_times() -> List[str]:
    """الحصول على قائمة الأوقات المتاحة"""
    return [
        '06:00', '07:00', '08:00', '09:00', '10:00',
        '11:00', '12:00', '13:00', '14:00', '15:00',
        '16:00', '17:00', '18:00', '19:00', '20:00',
        '21:00', '22:00', '23:00'
    ]

def get_lesson_name(lesson_num: int, lang: str = 'ar') -> str:
    """الحصول على اسم الدرس"""
    key = f'lesson_{lesson_num}_name'
    return get_text(key, lang)
