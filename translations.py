# -*- coding: utf-8 -*-
"""
translations.py
كل نصوص واجهة البوت (التعليمات، الأزرار، الرسائل) — وليس محتوى الدرس العربي نفسه.

إضافة لغة جديدة (مثال فرنسي):
    1. أضف "fr" لقائمة SUPPORTED_LANGUAGES أدناه مع اسمها وعلمها.
    2. أضف "fr": "..." داخل كل مفتاح في TEXTS.
    لا حاجة لتعديل أي ملف درس أو أي كود آخر.
"""

# كل لغة مدعومة: الكود -> (الاسم المعروض، العلم)
SUPPORTED_LANGUAGES = {
    "ar": ("العربية", "🇸🇦"),
    "en": ("English", "🇬🇧"),
    "tr": ("Türkçe", "🇹🇷"),
    # "fr": ("Français", "🇫🇷"),
    # "es": ("Español", "🇪🇸"),
    # "de": ("Deutsch", "🇩🇪"),
}

DEFAULT_LANG = "ar"

TEXTS = {
    "choose_language": {
        "ar": "أهلاً بك 🌙\nاختر لغة التعليم:",
        "en": "Welcome 🌙\nChoose your learning language:",
        "tr": "Hoş geldiniz 🌙\nEğitim dilinizi seçin:",
    },
    "welcome": {
        "ar": "أهلاً وسهلاً بك في نور بوت 🌙📖\nبرنامج من 18 درسًا لتعلّم اللغة العربية خطوة بخطوة.",
        "en": "Welcome to Noor Bot 🌙📖\nAn 18-lesson program to learn Arabic step by step.",
        "tr": "Nur Bot'a hoş geldiniz 🌙📖\nArapçayı adım adım öğrenmek için 18 derslik bir program.",
    },
    "trial_info": {
        "ar": "🎁 أول 5 دروس مجانية تمامًا.\nبعدها يتطلب الاشتراك (5$/برنامج).\n📅 أيام الدراسة: الأحد إلى الخميس (لا دروس الجمعة والسبت).",
        "en": "🎁 The first 5 lessons are completely free.\nAfter that a subscription is required ($5/program).\n📅 Study days: Sunday to Thursday (no lessons on Friday or Saturday).",
        "tr": "🎁 İlk 5 ders tamamen ücretsizdir.\nSonrasında abonelik gereklidir (program başına 5$).\n📅 Ders günleri: Pazar-Perşembe (Cuma ve Cumartesi ders yok).",
    },
    "ask_time": {
        "ar": "اختر الوقت المناسب لوصول درسك اليومي:",
        "en": "Choose the time you'd like your daily lesson to arrive:",
        "tr": "Günlük dersinizin gelmesini istediğiniz saati seçin:",
    },
    "time_confirmed": {
        "ar": "✅ تم! سيصلك الدرس يوميًا (الأحد-الخميس) الساعة {time}.",
        "en": "✅ Done! Your lesson will arrive daily (Sun-Thu) at {time}.",
        "tr": "✅ Tamam! Dersiniz her gün (Pazar-Perşembe) saat {time}'de gelecek.",
    },
    "lesson_starting_today": {
        "ar": "سيبدأ درسك الأول اليوم في هذا الوقت 🎉",
        "en": "Your first lesson will start today at this time 🎉",
        "tr": "İlk dersiniz bugün bu saatte başlayacak 🎉",
    },
    "lesson_starting_next_study_day": {
        "ar": "سيبدأ درسك الأول في أقرب يوم دراسي القادم، في هذا الوقت 🎉",
        "en": "Your first lesson will start on the next study day, at this time 🎉",
        "tr": "İlk dersiniz bir sonraki ders gününde bu saatte başlayacak 🎉",
    },
    "skill_intro": {"ar": "🔹 التمهيد", "en": "🔹 Warm-up", "tr": "🔹 Giriş"},
    "skill_vocab": {"ar": "🔹 المفردات", "en": "🔹 Vocabulary", "tr": "🔹 Kelime Bilgisi"},
    "skill_grammar": {"ar": "🔹 القواعد", "en": "🔹 Grammar", "tr": "🔹 Dil Bilgisi"},
    "skill_reading": {"ar": "🔹 القراءة", "en": "🔹 Reading", "tr": "🔹 Okuma"},
    "skill_listening": {"ar": "🔹 الاستماع", "en": "🔹 Listening", "tr": "🔹 Dinleme"},
    "skill_speaking": {"ar": "🔹 المحادثة", "en": "🔹 Speaking", "tr": "🔹 Konuşma"},
    "skill_writing": {"ar": "🔹 الكتابة", "en": "🔹 Writing", "tr": "🔹 Yazma"},
    "correct_answer": {"ar": "✅ إجابة صحيحة!", "en": "✅ Correct!", "tr": "✅ Doğru!"},
    "wrong_answer_retry": {
        "ar": "❌ ليست صحيحة تمامًا. حاول مرة أخرى.",
        "en": "❌ Not quite. Try again.",
        "tr": "❌ Tam olarak değil. Tekrar deneyin.",
    },
    "speaking_prompt_note": {
        "ar": "🎙️ أرسل إجابتك كتسجيل صوتي أو رسالة نصية، وسيصحّحها الذكاء الاصطناعي فورًا.",
        "en": "🎙️ Send your answer as a voice message or text, and AI will correct it right away.",
        "tr": "🎙️ Cevabınızı sesli mesaj veya yazı olarak gönderin, yapay zeka hemen düzeltecek.",
    },
    "writing_prompt_note": {
        "ar": "✍️ اكتب إجابتك، وسيصحّحها الذكاء الاصطناعي فورًا.",
        "en": "✍️ Write your answer, and AI will correct it right away.",
        "tr": "✍️ Cevabınızı yazın, yapay zeka hemen düzeltecek.",
    },
    "ai_analyzing": {
        "ar": "⏳ جارٍ تحليل إجابتك...",
        "en": "⏳ Analyzing your answer...",
        "tr": "⏳ Cevabınız analiz ediliyor...",
    },
    "ai_correction_unavailable": {
        "ar": "⚠️ تعذّر تصحيح إجابتك آليًا الآن، لكن تم حفظها وستُراجَع قريبًا.",
        "en": "⚠️ Couldn't auto-correct your answer right now, but it's been saved and will be reviewed soon.",
        "tr": "⚠️ Cevabınız şu anda otomatik düzeltilemedi, ancak kaydedildi ve yakında incelenecek.",
    },
    "lesson_complete": {
        "ar": "🎉 أحسنت! أتممت هذا الدرس بنجاح.",
        "en": "🎉 Well done! You completed this lesson.",
        "tr": "🎉 Aferin! Bu dersi tamamladınız.",
    },
    "program_complete": {
        "ar": "🏆 مبارك! أتممت برنامج نور بالكامل (18/18). شهادتك قيد التجهيز.",
        "en": "🏆 Congratulations! You completed the full Noor program (18/18). Your certificate is being prepared.",
        "tr": "🏆 Tebrikler! Nur programını tamamen bitirdiniz (18/18). Sertifikanız hazırlanıyor.",
    },
    "trial_ended": {
        "ar": "🎓 انتهت الفترة التجريبية المجانية.\nالبرنامج الكامل مدفوع (5$). سيتم تفعيل الاشتراك قريبًا.",
        "en": "🎓 Your free trial has ended.\nThe full program is paid ($5). Subscription activation is coming soon.",
        "tr": "🎓 Ücretsiz deneme süreniz sona erdi.\nTam program ücretlidir (5$). Abonelik yakında etkinleştirilecek.",
    },
    "not_a_study_day": {
        "ar": "اليوم ليس يوم دراسة (الجمعة والسبت إجازة) 🌙",
        "en": "Today is not a study day (Friday & Saturday are off) 🌙",
        "tr": "Bugün ders günü değil (Cuma ve Cumartesi tatil) 🌙",
    },
    "progress_title": {"ar": "📊 تقدّمك", "en": "📊 Your Progress", "tr": "📊 İlerlemeniz"},
    "progress_body": {
        "ar": "الدروس المكتملة: {completed}/18\nالدرس الحالي: {current}",
        "en": "Completed lessons: {completed}/18\nCurrent lesson: {current}",
        "tr": "Tamamlanan dersler: {completed}/18\nMevcut ders: {current}",
    },
    "settings_title": {"ar": "⚙️ الإعدادات", "en": "⚙️ Settings", "tr": "⚙️ Ayarlar"},
    "settings_change_language": {"ar": "🌐 تغيير اللغة", "en": "🌐 Change language", "tr": "🌐 Dili değiştir"},
    "settings_change_time": {"ar": "⏰ تغيير الوقت", "en": "⏰ Change time", "tr": "⏰ Saati değiştir"},
    "language_changed": {"ar": "✅ تم تغيير اللغة.", "en": "✅ Language changed.", "tr": "✅ Dil değiştirildi."},
    "no_active_program": {
        "ar": "لم تبدأ البرنامج بعد. أرسل /start للبدء.",
        "en": "You haven't started the program yet. Send /start to begin.",
        "tr": "Programa henüz başlamadınız. Başlamak için /start gönderin.",
    },
    "generic_error": {
        "ar": "⚠️ حدث خطأ غير متوقع. تم إبلاغ المسؤولين، حاول لاحقًا.",
        "en": "⚠️ An unexpected error occurred. Admins have been notified, please try again later.",
        "tr": "⚠️ Beklenmeyen bir hata oluştu. Yöneticilere bildirildi, lütfen daha sonra tekrar deneyin.",
    },
}


def t(key: str, lang: str = DEFAULT_LANG, **kwargs) -> str:
    """إرجاع النص المترجم؛ يعود للعربية إن لم توجد ترجمة للغة المطلوبة."""
    entry = TEXTS.get(key)
    if entry is None:
        return key
    text = entry.get(lang) or entry.get(DEFAULT_LANG) or ""
    if kwargs:
        text = text.format(**kwargs)
    return text


def language_keyboard_rows():
    """يبني صفوف أزرار اختيار اللغة من SUPPORTED_LANGUAGES تلقائيًا."""
    rows = []
    for code, (name, flag) in SUPPORTED_LANGUAGES.items():
        rows.append((f"{flag} {name}", f"lang|{code}"))
    return rows
