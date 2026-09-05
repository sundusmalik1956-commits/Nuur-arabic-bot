# -*- coding: utf-8 -*-
"""
translations.py
كل نصوص واجهة البوت (التعليمات، الأزرار، الرسائل).
"""

SUPPORTED_LANGUAGES = {
    "ar": ("العربية", "🇸🇦"),
    "en": ("English", "🇬🇧"),
    "tr": ("Türkçe", "🇹🇷"),
    "fr": ("Français", "🇫🇷"),
    "es": ("Español", "🇪🇸"),
    "de": ("Deutsch", "🇩🇪"),
    "ru": ("Русский", "🇷🇺"),
    "id": ("Indonesian", "🇮🇩"),
    "ur": ("اردو", "🇵🇰"),
    "bn": ("বাংলা", "🇧🇩"),
    "fa": ("فارسی", "🇮🇷"),
}

DEFAULT_LANG = "ar"

TEXTS = {
    "choose_language": {
        "ar": "أهلاً بك 🌙\nاختر لغة التعليم:",
        "en": "Welcome 🌙\nChoose your learning language:",
        "tr": "Hoş geldiniz 🌙\nEğitim dilinizi seçin:",
        "fr": "Bienvenue 🌙\nChoisissez votre langue d'apprentissage :",
        "es": "Bienvenido 🌙\nElige tu idioma de aprendizaje:",
        "de": "Willkommen 🌙\nWählen Sie Ihre Sprache:",
        "ru": "Добро пожаловать 🌙\nВыберите язык обучения:",
        "id": "Selamat datang 🌙\nPilih bahasa pembelajaran Anda:",
        "ur": "خوش آمدید 🌙\nاپنی سیکھنے کی زبان منتخب کریں:",
        "bn": "স্বাগত 🌙\nআপনার শেখার ভাষা নির্বাচন করুন:",
        "fa": "خوش آمدید 🌙\nزبان آموزش خود را انتخاب کنید:",
    },
    "welcome": {
        "ar": "أهلاً وسهلاً بك في نور بوت 🌙📖",
        "en": "Welcome to Noor Bot 🌙📖",
        "tr": "Nur Bot'a hoş geldiniz 🌙📖",
        "fr": "Bienvenue sur Noor Bot 🌙📖",
        "es": "Bienvenido a Noor Bot 🌙📖",
        "de": "Willkommen beim Noor Bot 🌙📖",
        "ru": "Добро пожаловать в Noor Bot 🌙📖",
        "id": "Selamat datang di Noor Bot 🌙📖",
        "ur": "نور بوٹ میں خوش آمدید 🌙📖",
        "bn": "নূর বটে স্বাগতম 🌙📖",
        "fa": "به ربات نور خوش آمدید 🌙📖",
    },
    "intro_levels_info": {
        "ar": "📚 يتوفر لدينا محتوى من المستوى A1 إلى B2، وسوف تُضاف باقي المستويات قريبًا.\n\n📌 يحتوي كل مستوى على 18 درسًا.\n🎁 أول 5 دروس مجانية تمامًا، وبعدها يتطلب اشتراك بقيمة 5 دولار فقط للمستوى (18 درسًا).",
        "en": "📚 We currently offer content from level A1 to B2, and other levels will be added soon.\n\n📌 Each level contains 18 lessons.\n🎁 The first 5 lessons are completely free, after which a $5 subscription is required for the 18-lesson level.",
        "tr": "📚 Şu anda A1'den B2'ye kadar içerik sunuyoruz ve diğer seviyeler yakında eklenecektir.\n\n📌 Her seviye 18 ders içerir.\n🎁 İlk 5 ders tamamen ücretsizdir, sonrasında 18 derslik seviye için sadece 5$ abonelik gereklidir.",
    },
    "ask_level_selection": {
        "ar": "🎯 يرجى اختيار مستواك:\nيمكنك إجراء اختبار تحديد المستوى أولاً، أو اختيار مستواك مباشرة (أو البدء من A0 لمن لا يعرف الحروف).",
        "en": "🎯 Please choose your level:\nYou can take a placement test first, or select your level directly (or start from A0 if you don't know the letters).",
        "tr": "🎯 Lütfen seviyenizi seçin:\nÖnce seviye belirleme sınavına girebilir veya doğrudan seviyenizi seçebilirsiniz (harfleri bilmiyorsanız A0'dan başlayın).",
    },
    "btn_take_placement_test": {
        "ar": "📝 إجراء اختبار تحديد المستوى",
        "en": "📝 Take Placement Test",
        "tr": "📝 Seviye Tespit Sınavı Yap",
    },
    "placement_test_intro": {
        "ar": "📝 جارٍ إعداد اختبار تحديد المستوى لك...",
        "en": "📝 Preparing your placement test...",
        "tr": "📝 Seviye tespit sınavınız hazırlanıyor...",
    },
    "level_chosen": {
        "ar": "✅ تم اختيار المستوى: {level}. دعنا نحدد وقت درسك اليومي الآن:",
        "en": "✅ Level selected: {level}. Let's set your daily lesson time now:",
        "tr": "✅ Seçilen seviye: {level}. Şimdi günlük ders saatinizi belirleyelim:",
    },
    "paywall_tribute": {
        "ar": "🎉 لقد أتممت بنجاح الدروس المجانية المتاحة!\n\nللاستمرار في رحلة تعلم اللغة العربية وفتح المستوى الكامل (18 درسًا مقابل 5$)، يرجى اختيار خطة الاشتراك المناسبة عبر Tribute.\n\nبعد إتمام الدفع، اضغط على زر (تحقق من الاشتراك) لتفعيل حسابك فوراً.",
        "en": "🎉 You have successfully completed the available free lessons!\n\nTo continue your Arabic learning journey and unlock the full level (18 lessons for $5), please choose the appropriate subscription plan via Tribute.\n\nAfter completing the payment, click the (Verify Subscription) button to activate your account immediately.",
    },
    "ask_time": {
        "ar": "اختر الوقت المناسب لوصول درسك اليومي:",
        "en": "Choose the time you'd like your daily lesson to arrive:",
    },
    "time_confirmed": {
        "ar": "✅ تم! سيصلك الدرس يوميًا (الأحد-الخميس) الساعة {time}.",
        "en": "✅ Done! Your lesson will arrive daily (Sun-Thu) at {time}.",
    },
    "lesson_starting_today": {
        "ar": "سيبدأ درسك الأول اليوم في هذا الوقت 🎉",
        "en": "Your first lesson will start today at this time 🎉",
    },
    "lesson_starting_next_study_day": {
        "ar": "سيبدأ درسك الأول في أقرب يوم دراسي القادم، في هذا الوقت 🎉",
        "en": "Your first lesson will start on the next study day, at this time 🎉",
    },
    "skill_intro": {"ar": "🔹 التمهيد", "en": "🔹 Warm-up"},
    "skill_vocab": {"ar": "🔹 المفردات", "en": "🔹 Vocabulary"},
    "skill_grammar": {"ar": "🔹 القواعد", "en": "🔹 Grammar"},
    "skill_reading": {"ar": "🔹 القراءة", "en": "🔹 Reading"},
    "skill_listening": {"ar": "🔹 الاستماع", "en": "🔹 Listening"},
    "skill_speaking": {"ar": "🔹 المحادثة", "en": "🔹 Speaking"},
    "skill_writing": {"ar": "🔹 الكتابة", "en": "🔹 Writing"},
    "correct_answer": {"ar": "✅ إجابة صحيحة!", "en": "✅ Correct!"},
    "wrong_answer_retry": {"ar": "❌ ليست صحيحة تمامًا. حاول مرة أخرى.", "en": "❌ Not quite. Try again."},
    "speaking_prompt_note": {"ar": "🎙️ أرسل إجابتك كتسجيل صوتي أو رسالة نصية، وسيصحّحها الذكاء الاصطناعي فورًا."},
    "writing_prompt_note": {"ar": "✍️ اكتب إجابتك، وسيصحّحها الذكاء الاصطناعي فورًا."},
    "ai_analyzing": {"ar": "⏳ جارٍ تحليل إجابتك...", "en": "⏳ Analyzing your answer..."},
    "ai_correction_unavailable": {"ar": "⚠️ تعذّر تصحيح إجابتك آليًا الآن، لكن تم حفظها وستُراجَع قريبًا."},
    "lesson_complete": {"ar": "🎉 أحسنت! أتممت هذا الدرس بنجاح."},
    "program_complete": {"ar": "🏆 مبارك! أتممت البرنامج بالكامل. شهادتك قيد التجهيز."},
    "progress_title": {"ar": "📊 تقدّمك", "en": "📊 Your Progress"},
    "progress_body": {"ar": "الدروس المكتملة: {completed}/18\nالدرس الحالي: {current}"},
    "settings_title": {"ar": "⚙️ الإعدادات", "en": "⚙️ Settings"},
    "settings_change_language": {"ar": "🌐 تغيير اللغة", "en": "🌐 Change language"},
    "settings_change_time": {"ar": "⏰ تغيير الوقت", "en": "⏰ Change time"},
    "language_changed": {"ar": "✅ تم تغيير اللغة."},
    "no_active_program": {"ar": "لم تبدأ البرنامج بعد. أرسل /start للبدء."},
    "generic_error": {"ar": "⚠️ حدث خطأ غير متوقع. تم إبلاغ المسؤولين، حاول لاحقًا."},
}


def t(key: str, lang: str = DEFAULT_LANG, **kwargs) -> str:
    entry = TEXTS.get(key)
    if entry is None:
        return key
    text = entry.get(lang) or entry.get(DEFAULT_LANG) or ""
    if kwargs:
        text = text.format(**kwargs)
    return text


def language_keyboard_rows():
    rows = []
    for code, (name, flag) in SUPPORTED_LANGUAGES.items():
        rows.append((f"{flag} {name}", f"lang|{code}"))
    return rows
ةا
