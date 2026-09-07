# -*- coding: utf-8 -*-
"""
translations.py
كل نصوص واجهة البوت (التعليمات، الأزرار، الرسائل) — وليس محتوى الدرس العربي نفسه.

إضافة لغة جديدة رقم 12 مستقبلاً:
    1. أضف الكود لقائمة SUPPORTED_LANGUAGES أدناه مع اسمها وعلمها.
    2. أضف الترجمة داخل كل مفتاح في TEXTS (أو اتركها تسقط تلقائيًا للعربية إن لم تُترجم بعد).
    لا حاجة لتعديل أي ملف درس أو أي كود آخر.
"""

# كل لغة مدعومة: الكود -> (الاسم المعروض بلغته، العلم)
SUPPORTED_LANGUAGES = {
    "ar": ("العربية", "🇸🇦"),
    "en": ("English", "🇬🇧"),
    "tr": ("Türkçe", "🇹🇷"),
    "es": ("Español", "🇪🇸"),
    "fr": ("Français", "🇫🇷"),
    "ru": ("Русский", "🇷🇺"),
    "zh": ("中文", "🇨🇳"),
    "ur": ("اردو", "🇵🇰"),
    "hi": ("हिन्दी", "🇮🇳"),
    "fa": ("فارسی", "🇮🇷"),
    "id": ("Bahasa Indonesia", "🇮🇩"),
}

DEFAULT_LANG = "ar"

TEXTS = {
    # -----------------------------------------------------------------
    # 1) الترحيب واللغة
    # -----------------------------------------------------------------
    "choose_language": {
        "ar": "أهلاً بك 🌙\nاختر لغتك المفضّلة:",
        "en": "Welcome 🌙\nChoose your preferred language:",
        "tr": "Hoş geldiniz 🌙\nTercih ettiğiniz dili seçin:",
        "es": "Bienvenido 🌙\nElige tu idioma preferido:",
        "fr": "Bienvenue 🌙\nChoisissez votre langue préférée :",
        "ru": "Добро пожаловать 🌙\nВыберите предпочитаемый язык:",
        "zh": "欢迎 🌙\n请选择您的首选语言：",
        "ur": "خوش آمدید 🌙\nاپنی پسندیدہ زبان منتخب کریں:",
        "hi": "स्वागत है 🌙\nअपनी पसंदीदा भाषा चुनें:",
        "fa": "خوش آمدید 🌙\nزبان مورد نظر خود را انتخاب کنید:",
        "id": "Selamat datang 🌙\nPilih bahasa pilihan Anda:",
    },

    # -----------------------------------------------------------------
    # 2) التعريف بالمنهج
    # -----------------------------------------------------------------
    "curriculum_intro": {
        "ar": (
            "🌙 أهلاً بك في نور بوت — رحلتك لتعلّم اللغة العربية\n\n"
            "📚 منهجنا مقسّم إلى مستويات: A0 (للمبتدئين تمامًا الذين لا يعرفون الحروف)، "
            "A1، A2، B1، B2.\n"
            "كل مستوى يحتوي على 18 درسًا (ما عدا A0: 4 دروس تأسيسية).\n\n"
            "🎁 أول 5 دروس مجانية تمامًا.\n"
            "💵 بعدها الاشتراك بسعر 5$ لكل مستوى."
        ),
        "en": (
            "🌙 Welcome to Noor Bot — your journey to learning Arabic\n\n"
            "📚 Our curriculum is divided into levels: A0 (for complete beginners who don't "
            "know the alphabet yet), A1, A2, B1, B2.\n"
            "Each level has 18 lessons (except A0: 4 foundational lessons).\n\n"
            "🎁 The first 5 lessons are completely free.\n"
            "💵 After that, subscription is $5 per level."
        ),
        "tr": (
            "🌙 Nur Bot'a hoş geldiniz — Arapça öğrenme yolculuğunuz\n\n"
            "📚 Müfredatımız seviyelere ayrılmıştır: A0 (alfabeyi henüz bilmeyen tam "
            "başlangıç seviyesi), A1, A2, B1, B2.\n"
            "Her seviyede 18 ders bulunur (A0 hariç: 4 temel ders).\n\n"
            "🎁 İlk 5 ders tamamen ücretsizdir.\n"
            "💵 Sonrasında seviye başına 5$ abonelik ücreti geçerlidir."
        ),
        "es": (
            "🌙 Bienvenido a Noor Bot — tu viaje para aprender árabe\n\n"
            "📚 Nuestro programa se divide en niveles: A0 (para principiantes totales que "
            "aún no conocen el alfabeto), A1, A2, B1, B2.\n"
            "Cada nivel tiene 18 lecciones (excepto A0: 4 lecciones básicas).\n\n"
            "🎁 Las primeras 5 lecciones son completamente gratuitas.\n"
            "💵 Después, la suscripción cuesta $5 por nivel."
        ),
        "fr": (
            "🌙 Bienvenue sur Noor Bot — votre voyage pour apprendre l'arabe\n\n"
            "📚 Notre programme est divisé en niveaux : A0 (pour les débutants complets qui "
            "ne connaissent pas encore l'alphabet), A1, A2, B1, B2.\n"
            "Chaque niveau comporte 18 leçons (sauf A0 : 4 leçons de base).\n\n"
            "🎁 Les 5 premières leçons sont entièrement gratuites.\n"
            "💵 Ensuite, l'abonnement coûte 5$ par niveau."
        ),
        "ru": (
            "🌙 Добро пожаловать в Noor Bot — ваше путешествие в изучении арабского\n\n"
            "📚 Наша программа разделена на уровни: A0 (для начинающих с нуля, не "
            "знающих алфавит), A1, A2, B1, B2.\n"
            "На каждом уровне 18 уроков (кроме A0: 4 базовых урока).\n\n"
            "🎁 Первые 5 уроков совершенно бесплатны.\n"
            "💵 Далее подписка стоит 5$ за уровень."
        ),
        "zh": (
            "🌙 欢迎使用 Noor Bot — 开启您的阿拉伯语学习之旅\n\n"
            "📚 我们的课程分为多个级别：A0（完全零基础，尚不认识字母的学员）、"
            "A1、A2、B1、B2。\n"
            "每个级别包含18节课（A0除外：4节基础课）。\n\n"
            "🎁 前5节课完全免费。\n"
            "💵 之后每个级别订阅费用为5美元。"
        ),
        "ur": (
            "🌙 نور بوٹ میں خوش آمدید — عربی سیکھنے کا آپ کا سفر\n\n"
            "📚 ہمارا نصاب مختلف سطحوں میں تقسیم ہے: A0 (مکمل ابتدائی طلبہ کے لیے جو حروف "
            "تہجی سے واقف نہیں)، A1، A2، B1، B2۔\n"
            "ہر سطح میں 18 اسباق ہیں (سوائے A0 کے: 4 بنیادی اسباق)۔\n\n"
            "🎁 پہلے 5 اسباق مکمل طور پر مفت ہیں۔\n"
            "💵 اس کے بعد رکنیت کی قیمت فی سطح 5$ ہے۔"
        ),
        "hi": (
            "🌙 नूर बॉट में आपका स्वागत है — अरबी सीखने की आपकी यात्रा\n\n"
            "📚 हमारा पाठ्यक्रम स्तरों में विभाजित है: A0 (पूर्ण शुरुआती जो अभी वर्णमाला "
            "नहीं जानते), A1, A2, B1, B2।\n"
            "प्रत्येक स्तर में 18 पाठ हैं (A0 को छोड़कर: 4 आधारभूत पाठ)।\n\n"
            "🎁 पहले 5 पाठ पूरी तरह मुफ्त हैं।\n"
            "💵 उसके बाद सदस्यता शुल्क प्रति स्तर $5 है।"
        ),
        "fa": (
            "🌙 به نور بات خوش آمدید — سفر شما برای یادگیری زبان عربی\n\n"
            "📚 برنامه درسی ما به سطوح مختلف تقسیم شده است: A0 (برای مبتدیان کامل که هنوز "
            "الفبا را نمی‌دانند)، A1، A2، B1، B2.\n"
            "هر سطح شامل ۱۸ درس است (به‌جز A0: ۴ درس پایه).\n\n"
            "🎁 پنج درس اول کاملاً رایگان است.\n"
            "💵 پس از آن، هزینه اشتراک ۵ دلار برای هر سطح است."
        ),
        "id": (
            "🌙 Selamat datang di Noor Bot — perjalanan Anda belajar bahasa Arab\n\n"
            "📚 Kurikulum kami terbagi dalam beberapa level: A0 (untuk pemula total yang "
            "belum mengenal huruf), A1, A2, B1, B2.\n"
            "Setiap level berisi 18 pelajaran (kecuali A0: 4 pelajaran dasar).\n\n"
            "🎁 5 pelajaran pertama sepenuhnya gratis.\n"
            "💵 Setelah itu, langganan seharga $5 per level."
        ),
    },

    # -----------------------------------------------------------------
    # 3) اختيار المستوى
    # -----------------------------------------------------------------
    "choose_level": {
        "ar": "📊 اختر مستواك الحالي:",
        "en": "📊 Choose your current level:",
        "tr": "📊 Mevcut seviyenizi seçin:",
        "es": "📊 Elige tu nivel actual:",
        "fr": "📊 Choisissez votre niveau actuel :",
        "ru": "📊 Выберите свой текущий уровень:",
        "zh": "📊 请选择您当前的级别：",
        "ur": "📊 اپنی موجودہ سطح منتخب کریں:",
        "hi": "📊 अपना वर्तमान स्तर चुनें:",
        "fa": "📊 سطح فعلی خود را انتخاب کنید:",
        "id": "📊 Pilih level Anda saat ini:",
    },
    "level_a0_note": {
        "ar": "ℹ️ مستوى A0 مخصص لمن لا يعرف الحروف العربية تمامًا (4 دروس تأسيسية).",
        "en": "ℹ️ Level A0 is for those who don't know the Arabic alphabet at all yet (4 foundational lessons).",
        "tr": "ℹ️ A0 seviyesi, Arap alfabesini hiç bilmeyenler içindir (4 temel ders).",
        "es": "ℹ️ El nivel A0 es para quienes aún no conocen el alfabeto árabe (4 lecciones básicas).",
        "fr": "ℹ️ Le niveau A0 est destiné à ceux qui ne connaissent pas encore l'alphabet arabe (4 leçons de base).",
        "ru": "ℹ️ Уровень A0 предназначен для тех, кто вообще не знает арабский алфавит (4 базовых урока).",
        "zh": "ℹ️ A0级别适合完全不认识阿拉伯字母的学员（4节基础课）。",
        "ur": "ℹ️ سطح A0 ان کے لیے ہے جو عربی حروف تہجی بالکل نہیں جانتے (4 بنیادی اسباق)۔",
        "hi": "ℹ️ स्तर A0 उनके लिए है जो अरबी वर्णमाला बिल्कुल नहीं जानते (4 आधारभूत पाठ)।",
        "fa": "ℹ️ سطح A0 برای کسانی است که اصلاً الفبای عربی را نمی‌دانند (۴ درس پایه).",
        "id": "ℹ️ Level A0 untuk mereka yang belum mengenal huruf Arab sama sekali (4 pelajaran dasar).",
    },
    "placement_test_offer": {
        "ar": "🎯 غير متأكد من مستواك؟ يمكنك أخذ اختبار تحديد المستوى أولاً:",
        "en": "🎯 Not sure about your level? You can take a placement test first:",
        "tr": "🎯 Seviyenizden emin değil misiniz? Önce bir seviye tespit sınavına girebilirsiniz:",
        "es": "🎯 ¿No estás seguro de tu nivel? Puedes hacer una prueba de nivel primero:",
        "fr": "🎯 Vous n'êtes pas sûr de votre niveau ? Vous pouvez d'abord passer un test de niveau :",
        "ru": "🎯 Не уверены в своём уровне? Сначала можно пройти тест на определение уровня:",
        "zh": "🎯 不确定自己的级别？您可以先参加分级测试：",
        "ur": "🎯 اپنی سطح کے بارے میں یقین نہیں؟ پہلے سطح کا تعین کرنے والا ٹیسٹ لے سکتے ہیں:",
        "hi": "🎯 अपने स्तर के बारे में अनिश्चित हैं? आप पहले एक स्तर निर्धारण परीक्षा दे सकते हैं:",
        "fa": "🎯 از سطح خود مطمئن نیستید؟ می‌توانید ابتدا آزمون تعیین سطح بدهید:",
        "id": "🎯 Tidak yakin dengan level Anda? Anda bisa mengikuti tes penempatan level terlebih dahulu:",
    },
    "placement_test_button": {
        "ar": "🎯 اختبار تحديد المستوى",
        "en": "🎯 Placement Test",
        "tr": "🎯 Seviye Tespit Sınavı",
        "es": "🎯 Prueba de nivel",
        "fr": "🎯 Test de niveau",
        "ru": "🎯 Тест на уровень",
        "zh": "🎯 分级测试",
        "ur": "🎯 سطح کا تعین کرنے والا ٹیسٹ",
        "hi": "🎯 स्तर निर्धारण परीक्षा",
        "fa": "🎯 آزمون تعیین سطح",
        "id": "🎯 Tes Penempatan Level",
    },
    "level_confirmed": {
        "ar": "✅ تم تحديد مستواك: {level}",
        "en": "✅ Your level is set to: {level}",
        "tr": "✅ Seviyeniz belirlendi: {level}",
        "es": "✅ Tu nivel se ha establecido en: {level}",
        "fr": "✅ Votre niveau est défini sur : {level}",
        "ru": "✅ Ваш уровень установлен: {level}",
        "zh": "✅ 您的级别已设置为：{level}",
        "ur": "✅ آپ کی سطح مقرر کر دی گئی: {level}",
        "hi": "✅ आपका स्तर सेट कर दिया गया है: {level}",
        "fa": "✅ سطح شما تنظیم شد: {level}",
        "id": "✅ Level Anda telah ditetapkan: {level}",
    },

    # -----------------------------------------------------------------
    # 4) الجنس والقروب
    # -----------------------------------------------------------------
    "choose_gender": {
        "ar": "👤 لتوجيهك إلى القروب التحفيزي المناسب، اختر:",
        "en": "👤 To direct you to the right motivational group, choose:",
        "tr": "👤 Sizi doğru motivasyon grubuna yönlendirmek için seçin:",
        "es": "👤 Para dirigirte al grupo motivacional adecuado, elige:",
        "fr": "👤 Pour vous orienter vers le bon groupe de motivation, choisissez :",
        "ru": "👤 Чтобы направить вас в подходящую группу поддержки, выберите:",
        "zh": "👤 为了引导您加入合适的激励群组，请选择：",
        "ur": "👤 آپ کو مناسب حوصلہ افزا گروپ کی طرف رہنمائی کرنے کے لیے، منتخب کریں:",
        "hi": "👤 आपको सही प्रेरक समूह की ओर निर्देशित करने के लिए, चुनें:",
        "fa": "👤 برای هدایت شما به گروه انگیزشی مناسب، انتخاب کنید:",
        "id": "👤 Untuk mengarahkan Anda ke grup motivasi yang tepat, pilih:",
    },
    "gender_male": {
        "ar": "👨 رجل", "en": "👨 Male", "tr": "👨 Erkek", "es": "👨 Hombre", "fr": "👨 Homme",
        "ru": "👨 Мужчина", "zh": "👨 男性", "ur": "👨 مرد", "hi": "👨 पुरुष", "fa": "👨 مرد", "id": "👨 Pria",
    },
    "gender_female": {
        "ar": "👩 امرأة", "en": "👩 Female", "tr": "👩 Kadın", "es": "👩 Mujer", "fr": "👩 Femme",
        "ru": "👩 Женщина", "zh": "👩 女性", "ur": "👩 عورت", "hi": "👩 महिला", "fa": "👩 زن", "id": "👩 Wanita",
    },
    "group_invite": {
        "ar": "🎉 انضم إلى قروب الدعم والتحفيز الخاص بك:\n{link}",
        "en": "🎉 Join your dedicated support & motivation group:\n{link}",
        "tr": "🎉 Size özel destek ve motivasyon grubuna katılın:\n{link}",
        "es": "🎉 Únete a tu grupo de apoyo y motivación:\n{link}",
        "fr": "🎉 Rejoignez votre groupe de soutien et de motivation :\n{link}",
        "ru": "🎉 Присоединяйтесь к вашей группе поддержки и мотивации:\n{link}",
        "zh": "🎉 加入您的专属支持与激励群组：\n{link}",
        "ur": "🎉 اپنے مخصوص معاون اور حوصلہ افزا گروپ میں شامل ہوں:\n{link}",
        "hi": "🎉 अपने समर्पित समर्थन और प्रेरणा समूह में शामिल हों:\n{link}",
        "fa": "🎉 به گروه حمایتی و انگیزشی اختصاصی خود بپیوندید:\n{link}",
        "id": "🎉 Bergabunglah dengan grup dukungan & motivasi khusus Anda:\n{link}",
    },

    # -----------------------------------------------------------------
    # 5) وقت الدرس
    # -----------------------------------------------------------------
    "ask_time": {
        "ar": "⏰ اختر الوقت المناسب لوصول درسك اليومي:",
        "en": "⏰ Choose the time you'd like your daily lesson to arrive:",
        "tr": "⏰ Günlük dersinizin gelmesini istediğiniz saati seçin:",
        "es": "⏰ Elige la hora a la que quieres recibir tu lección diaria:",
        "fr": "⏰ Choisissez l'heure à laquelle vous souhaitez recevoir votre leçon quotidienne :",
        "ru": "⏰ Выберите удобное время для получения ежедневного урока:",
        "zh": "⏰ 请选择您希望每天收到课程的时间：",
        "ur": "⏰ اپنے روزانہ سبق کی آمد کے لیے مناسب وقت منتخب کریں:",
        "hi": "⏰ अपने दैनिक पाठ के आने का उचित समय चुनें:",
        "fa": "⏰ زمان مناسب برای دریافت درس روزانه خود را انتخاب کنید:",
        "id": "⏰ Pilih waktu yang Anda inginkan untuk menerima pelajaran harian Anda:",
    },
    "time_confirmed": {
        "ar": "✅ تم! سيصلك الدرس يوميًا الساعة {time} (ما عدا أيام إجازتك).",
        "en": "✅ Done! Your lesson will arrive daily at {time} (except your vacation days).",
        "tr": "✅ Tamam! Dersiniz her gün saat {time}'de gelecek (izin günleriniz hariç).",
        "es": "✅ ¡Listo! Tu lección llegará diariamente a las {time} (excepto tus días libres).",
        "fr": "✅ C'est fait ! Votre leçon arrivera chaque jour à {time} (sauf vos jours de congé).",
        "ru": "✅ Готово! Урок будет приходить ежедневно в {time} (кроме ваших выходных).",
        "zh": "✅ 完成！您的课程将于每天 {time} 送达（您的休息日除外）。",
        "ur": "✅ ہو گیا! آپ کا سبق روزانہ {time} بجے پہنچے گا (آپ کی چھٹی کے دنوں کے علاوہ)۔",
        "hi": "✅ हो गया! आपका पाठ प्रतिदिन {time} बजे आएगा (आपकी छुट्टी के दिनों को छोड़कर)।",
        "fa": "✅ انجام شد! درس شما هر روز ساعت {time} می‌رسد (به‌جز روزهای تعطیل شما).",
        "id": "✅ Selesai! Pelajaran Anda akan tiba setiap hari pukul {time} (kecuali hari libur Anda).",
    },
    "lesson_starting_today": {
        "ar": "سيبدأ درسك الأول اليوم في هذا الوقت 🎉",
        "en": "Your first lesson will start today at this time 🎉",
        "tr": "İlk dersiniz bugün bu saatte başlayacak 🎉",
        "es": "Tu primera lección comenzará hoy a esta hora 🎉",
        "fr": "Votre première leçon commencera aujourd'hui à cette heure 🎉",
        "ru": "Ваш первый урок начнётся сегодня в это время 🎉",
        "zh": "您的第一节课将于今天此时开始 🎉",
        "ur": "آپ کا پہلا سبق آج اسی وقت شروع ہو گا 🎉",
        "hi": "आपका पहला पाठ आज इसी समय शुरू होगा 🎉",
        "fa": "اولین درس شما امروز در همین ساعت شروع می‌شود 🎉",
        "id": "Pelajaran pertama Anda akan dimulai hari ini pada waktu ini 🎉",
    },
    "lesson_starting_next_study_day": {
        "ar": "سيبدأ درسك الأول في أقرب يوم دراسي القادم، في هذا الوقت 🎉",
        "en": "Your first lesson will start on the next study day, at this time 🎉",
        "tr": "İlk dersiniz bir sonraki ders gününde bu saatte başlayacak 🎉",
        "es": "Tu primera lección comenzará el próximo día de estudio, a esta hora 🎉",
        "fr": "Votre première leçon commencera le prochain jour d'étude, à cette heure 🎉",
        "ru": "Ваш первый урок начнётся в следующий учебный день, в это время 🎉",
        "zh": "您的第一节课将在下一个学习日的此时开始 🎉",
        "ur": "آپ کا پہلا سبق اگلے تعلیمی دن اسی وقت شروع ہو گا 🎉",
        "hi": "आपका पहला पाठ अगले अध्ययन दिवस पर इसी समय शुरू होगा 🎉",
        "fa": "اولین درس شما در نزدیک‌ترین روز تحصیلی بعدی، در همین ساعت شروع می‌شود 🎉",
        "id": "Pelajaran pertama Anda akan dimulai pada hari belajar berikutnya, pada waktu ini 🎉",
    },

    # -----------------------------------------------------------------
    # 6) أيام الإجازة (اختيار حر، يومان أسبوعيًا)
    # -----------------------------------------------------------------
    "ask_vacation_days": {
        "ar": "📅 اختر يومين للإجازة الأسبوعية (لن يصلك درس فيهما):",
        "en": "📅 Choose two weekly vacation days (no lesson will be sent on these days):",
        "tr": "📅 Haftalık iki izin günü seçin (bu günlerde ders gönderilmeyecek):",
        "es": "📅 Elige dos días de descanso semanal (no se enviará lección esos días):",
        "fr": "📅 Choisissez deux jours de repos hebdomadaires (aucune leçon ne sera envoyée ces jours-là) :",
        "ru": "📅 Выберите два выходных дня в неделю (в эти дни урок не будет отправляться):",
        "zh": "📅 请选择每周两天的休息日（这两天将不会发送课程）：",
        "ur": "📅 ہفتہ وار دو چھٹی کے دن منتخب کریں (ان دنوں سبق نہیں بھیجا جائے گا):",
        "hi": "📅 साप्ताहिक दो छुट्टी के दिन चुनें (इन दिनों पाठ नहीं भेजा जाएगा):",
        "fa": "📅 دو روز تعطیلی هفتگی انتخاب کنید (در این روزها درسی ارسال نمی‌شود):",
        "id": "📅 Pilih dua hari libur mingguan (pelajaran tidak akan dikirim pada hari-hari ini):",
    },
    "vacation_day_selected": {
        "ar": "✅ اخترت يوم: {day}\nاختر اليوم الثاني:",
        "en": "✅ You selected: {day}\nChoose the second day:",
        "tr": "✅ Seçtiğiniz gün: {day}\nİkinci günü seçin:",
        "es": "✅ Seleccionaste: {day}\nElige el segundo día:",
        "fr": "✅ Vous avez choisi : {day}\nChoisissez le deuxième jour :",
        "ru": "✅ Вы выбрали: {day}\nВыберите второй день:",
        "zh": "✅ 您已选择：{day}\n请选择第二天：",
        "ur": "✅ آپ نے منتخب کیا: {day}\nدوسرا دن منتخب کریں:",
        "hi": "✅ आपने चुना: {day}\nदूसरा दिन चुनें:",
        "fa": "✅ شما انتخاب کردید: {day}\nروز دوم را انتخاب کنید:",
        "id": "✅ Anda memilih: {day}\nPilih hari kedua:",
    },
    "vacation_days_confirmed": {
        "ar": "✅ أيام إجازتك الأسبوعية: {day1} و{day2}",
        "en": "✅ Your weekly vacation days: {day1} and {day2}",
        "tr": "✅ Haftalık izin günleriniz: {day1} ve {day2}",
        "es": "✅ Tus días de descanso semanal: {day1} y {day2}",
        "fr": "✅ Vos jours de repos hebdomadaires : {day1} et {day2}",
        "ru": "✅ Ваши еженедельные выходные: {day1} и {day2}",
        "zh": "✅ 您每周的休息日：{day1} 和 {day2}",
        "ur": "✅ آپ کی ہفتہ وار چھٹی کے دن: {day1} اور {day2}",
        "hi": "✅ आपकी साप्ताहिक छुट्टी के दिन: {day1} और {day2}",
        "fa": "✅ روزهای تعطیلی هفتگی شما: {day1} و {day2}",
        "id": "✅ Hari libur mingguan Anda: {day1} dan {day2}",
    },

    # -----------------------------------------------------------------
    # أسماء أيام الأسبوع (تُستخدم في أزرار الإجازة والملخص)
    # -----------------------------------------------------------------
    "day_sat": {"ar": "السبت", "en": "Saturday", "tr": "Cumartesi", "es": "Sábado", "fr": "Samedi",
                "ru": "Суббота", "zh": "星期六", "ur": "ہفتہ", "hi": "शनिवार", "fa": "شنبه", "id": "Sabtu"},
    "day_sun": {"ar": "الأحد", "en": "Sunday", "tr": "Pazar", "es": "Domingo", "fr": "Dimanche",
                "ru": "Воскресенье", "zh": "星期日", "ur": "اتوار", "hi": "रविवार", "fa": "یکشنبه", "id": "Minggu"},
    "day_mon": {"ar": "الاثنين", "en": "Monday", "tr": "Pazartesi", "es": "Lunes", "fr": "Lundi",
                "ru": "Понедельник", "zh": "星期一", "ur": "پیر", "hi": "सोमवार", "fa": "دوشنبه", "id": "Senin"},
    "day_tue": {"ar": "الثلاثاء", "en": "Tuesday", "tr": "Salı", "es": "Martes", "fr": "Mardi",
                "ru": "Вторник", "zh": "星期二", "ur": "منگل", "hi": "मंगलवार", "fa": "سه‌شنبه", "id": "Selasa"},
    "day_wed": {"ar": "الأربعاء", "en": "Wednesday", "tr": "Çarşamba", "es": "Miércoles", "fr": "Mercredi",
                "ru": "Среда", "zh": "星期三", "ur": "بدھ", "hi": "बुधवार", "fa": "چهارشنبه", "id": "Rabu"},
    "day_thu": {"ar": "الخميس", "en": "Thursday", "tr": "Perşembe", "es": "Jueves", "fr": "Jeudi",
                "ru": "Четверг", "zh": "星期四", "ur": "جمعرات", "hi": "गुरुवार", "fa": "پنجشنبه", "id": "Kamis"},
    "day_fri": {"ar": "الجمعة", "en": "Friday", "tr": "Cuma", "es": "Viernes", "fr": "Vendredi",
                "ru": "Пятница", "zh": "星期五", "ur": "جمعہ", "hi": "शुक्रवार", "fa": "جمعه", "id": "Jumat"},

    # -----------------------------------------------------------------
    # 7) الملخص الشامل
    # -----------------------------------------------------------------
    "summary_title": {
        "ar": "📋 ملخص إعداداتك", "en": "📋 Your Setup Summary", "tr": "📋 Kurulum Özetiniz",
        "es": "📋 Resumen de tu configuración", "fr": "📋 Résumé de votre configuration",
        "ru": "📋 Сводка ваших настроек", "zh": "📋 您的设置摘要", "ur": "📋 آپ کی ترتیب کا خلاصہ",
        "hi": "📋 आपकी सेटअप सारांश", "fa": "📋 خلاصه تنظیمات شما", "id": "📋 Ringkasan Pengaturan Anda",
    },
    "summary_body": {
        "ar": "👤 الاسم: {name}\n📊 المستوى: {level}\n⏰ وقت الدرس: {time}\n📅 أيام الإجازة: {vacation}\n👥 قروبك: {group}",
        "en": "👤 Name: {name}\n📊 Level: {level}\n⏰ Lesson time: {time}\n📅 Vacation days: {vacation}\n👥 Your group: {group}",
        "tr": "👤 İsim: {name}\n📊 Seviye: {level}\n⏰ Ders saati: {time}\n📅 İzin günleri: {vacation}\n👥 Grubunuz: {group}",
        "es": "👤 Nombre: {name}\n📊 Nivel: {level}\n⏰ Hora de la lección: {time}\n📅 Días de descanso: {vacation}\n👥 Tu grupo: {group}",
        "fr": "👤 Nom : {name}\n📊 Niveau : {level}\n⏰ Heure de la leçon : {time}\n📅 Jours de repos : {vacation}\n👥 Votre groupe : {group}",
        "ru": "👤 Имя: {name}\n📊 Уровень: {level}\n⏰ Время урока: {time}\n📅 Выходные дни: {vacation}\n👥 Ваша группа: {group}",
        "zh": "👤 姓名：{name}\n📊 级别：{level}\n⏰ 上课时间：{time}\n📅 休息日：{vacation}\n👥 您的群组：{group}",
        "ur": "👤 نام: {name}\n📊 سطح: {level}\n⏰ سبق کا وقت: {time}\n📅 چھٹی کے دن: {vacation}\n👥 آپ کا گروپ: {group}",
        "hi": "👤 नाम: {name}\n📊 स्तर: {level}\n⏰ पाठ का समय: {time}\n📅 छुट्टी के दिन: {vacation}\n👥 आपका समूह: {group}",
        "fa": "👤 نام: {name}\n📊 سطح: {level}\n⏰ زمان درس: {time}\n📅 روزهای تعطیل: {vacation}\n👥 گروه شما: {group}",
        "id": "👤 Nama: {name}\n📊 Level: {level}\n⏰ Waktu pelajaran: {time}\n📅 Hari libur: {vacation}\n👥 Grup Anda: {group}",
    },
    "summary_edit_hint": {
        "ar": "يمكنك تعديل أي من هذه الإعدادات في أي وقت عبر /settings",
        "en": "You can edit any of these settings anytime via /settings",
        "tr": "Bu ayarlardan herhangi birini istediğiniz zaman /settings üzerinden değiştirebilirsiniz",
        "es": "Puedes editar cualquiera de estas configuraciones en cualquier momento con /settings",
        "fr": "Vous pouvez modifier n'importe lequel de ces paramètres à tout moment via /settings",
        "ru": "Вы можете изменить любую из этих настроек в любое время через /settings",
        "zh": "您可以随时通过 /settings 编辑这些设置",
        "ur": "آپ کسی بھی وقت /settings کے ذریعے ان ترتیبات میں سے کسی کو بھی تبدیل کر سکتے ہیں",
        "hi": "आप कभी भी /settings के माध्यम से इनमें से किसी भी सेटिंग को संपादित कर सकते हैं",
        "fa": "می‌توانید هر یک از این تنظیمات را در هر زمان از طریق /settings ویرایش کنید",
        "id": "Anda dapat mengedit pengaturan ini kapan saja melalui /settings",
    },

    # -----------------------------------------------------------------
    # الإعدادات (settings) — تعديل أي عنصر
    # -----------------------------------------------------------------
    "settings_title": {
        "ar": "⚙️ الإعدادات — اختر ما تريد تغييره:", "en": "⚙️ Settings — choose what to change:",
        "tr": "⚙️ Ayarlar — değiştirmek istediğinizi seçin:", "es": "⚙️ Ajustes — elige qué cambiar:",
        "fr": "⚙️ Paramètres — choisissez ce que vous voulez modifier :",
        "ru": "⚙️ Настройки — выберите, что изменить:", "zh": "⚙️ 设置 — 选择要更改的项目：",
        "ur": "⚙️ ترتیبات — منتخب کریں کہ کیا تبدیل کرنا ہے:", "hi": "⚙️ सेटिंग्स — बदलने के लिए चुनें:",
        "fa": "⚙️ تنظیمات — انتخاب کنید چه چیزی را تغییر دهید:", "id": "⚙️ Pengaturan — pilih yang ingin diubah:",
    },
    "settings_change_language": {
        "ar": "🌐 تغيير اللغة", "en": "🌐 Change language", "tr": "🌐 Dili değiştir", "es": "🌐 Cambiar idioma",
        "fr": "🌐 Changer de langue", "ru": "🌐 Изменить язык", "zh": "🌐 更改语言", "ur": "🌐 زبان تبدیل کریں",
        "hi": "🌐 भाषा बदलें", "fa": "🌐 تغییر زبان", "id": "🌐 Ubah bahasa",
    },
    "settings_change_level": {
        "ar": "📊 تغيير المستوى", "en": "📊 Change level", "tr": "📊 Seviyeyi değiştir", "es": "📊 Cambiar nivel",
        "fr": "📊 Changer de niveau", "ru": "📊 Изменить уровень", "zh": "📊 更改级别", "ur": "📊 سطح تبدیل کریں",
        "hi": "📊 स्तर बदलें", "fa": "📊 تغییر سطح", "id": "📊 Ubah level",
    },
    "settings_change_gender": {
        "ar": "👤 تغيير القروب", "en": "👤 Change group", "tr": "👤 Grubu değiştir", "es": "👤 Cambiar grupo",
        "fr": "👤 Changer de groupe", "ru": "👤 Изменить группу", "zh": "👤 更改群组", "ur": "👤 گروپ تبدیل کریں",
        "hi": "👤 समूह बदलें", "fa": "👤 تغییر گروه", "id": "👤 Ubah grup",
    },
    "settings_change_time": {
        "ar": "⏰ تغيير الوقت", "en": "⏰ Change time", "tr": "⏰ Saati değiştir", "es": "⏰ Cambiar hora",
        "fr": "⏰ Changer l'heure", "ru": "⏰ Изменить время", "zh": "⏰ 更改时间", "ur": "⏰ وقت تبدیل کریں",
        "hi": "⏰ समय बदलें", "fa": "⏰ تغییر زمان", "id": "⏰ Ubah waktu",
    },
    "settings_change_vacation": {
        "ar": "📅 تغيير أيام الإجازة", "en": "📅 Change vacation days", "tr": "📅 İzin günlerini değiştir",
        "es": "📅 Cambiar días de descanso", "fr": "📅 Changer les jours de repos",
        "ru": "📅 Изменить выходные дни", "zh": "📅 更改休息日", "ur": "📅 چھٹی کے دن تبدیل کریں",
        "hi": "📅 छुट्टी के दिन बदलें", "fa": "📅 تغییر روزهای تعطیل", "id": "📅 Ubah hari libur",
    },
    "settings_view_summary": {
        "ar": "📋 عرض الملخص الكامل", "en": "📋 View full summary", "tr": "📋 Tam özeti görüntüle",
        "es": "📋 Ver resumen completo", "fr": "📋 Voir le résumé complet", "ru": "📋 Посмотреть полную сводку",
        "zh": "📋 查看完整摘要", "ur": "📋 مکمل خلاصہ دیکھیں", "hi": "📋 पूरा सारांश देखें",
        "fa": "📋 مشاهده خلاصه کامل", "id": "📋 Lihat ringkasan lengkap",
    },
    "language_changed": {
        "ar": "✅ تم تغيير اللغة.", "en": "✅ Language changed.", "tr": "✅ Dil değiştirildi.",
        "es": "✅ Idioma cambiado.", "fr": "✅ Langue modifiée.", "ru": "✅ Язык изменён.",
        "zh": "✅ 语言已更改。", "ur": "✅ زبان تبدیل ہو گئی۔", "hi": "✅ भाषा बदल दी गई।",
        "fa": "✅ زبان تغییر کرد.", "id": "✅ Bahasa telah diubah.",
    },

    # -----------------------------------------------------------------
    # نصوص الدرس والمهارات (كما كانت)
    # -----------------------------------------------------------------
    "skill_intro": {
        "ar": "🔹 التمهيد", "en": "🔹 Warm-up", "tr": "🔹 Giriş", "es": "🔹 Introducción",
        "fr": "🔹 Introduction", "ru": "🔹 Вступление", "zh": "🔹 导入", "ur": "🔹 تمہید",
        "hi": "🔹 परिचय", "fa": "🔹 مقدمه", "id": "🔹 Pembukaan",
    },
    "skill_vocab": {
        "ar": "🔹 المفردات", "en": "🔹 Vocabulary", "tr": "🔹 Kelime Bilgisi", "es": "🔹 Vocabulario",
        "fr": "🔹 Vocabulaire", "ru": "🔹 Лексика", "zh": "🔹 词汇", "ur": "🔹 الفاظ",
        "hi": "🔹 शब्दावली", "fa": "🔹 واژگان", "id": "🔹 Kosakata",
    },
    "skill_grammar": {
        "ar": "🔹 القواعد", "en": "🔹 Grammar", "tr": "🔹 Dil Bilgisi", "es": "🔹 Gramática",
        "fr": "🔹 Grammaire", "ru": "🔹 Грамматика", "zh": "🔹 语法", "ur": "🔹 قواعد",
        "hi": "🔹 व्याकरण", "fa": "🔹 دستور زبان", "id": "🔹 Tata Bahasa",
    },
    "skill_reading": {
        "ar": "🔹 القراءة", "en": "🔹 Reading", "tr": "🔹 Okuma", "es": "🔹 Lectura",
        "fr": "🔹 Lecture", "ru": "🔹 Чтение", "zh": "🔹 阅读", "ur": "🔹 پڑھنا",
        "hi": "🔹 पठन", "fa": "🔹 خواندن", "id": "🔹 Membaca",
    },
    "skill_listening": {
        "ar": "🔹 الاستماع", "en": "🔹 Listening", "tr": "🔹 Dinleme", "es": "🔹 Escucha",
        "fr": "🔹 Écoute", "ru": "🔹 Аудирование", "zh": "🔹 听力", "ur": "🔹 سننا",
        "hi": "🔹 सुनना", "fa": "🔹 شنیدن", "id": "🔹 Mendengarkan",
    },
    "skill_speaking": {
        "ar": "🔹 المحادثة", "en": "🔹 Speaking", "tr": "🔹 Konuşma", "es": "🔹 Conversación",
        "fr": "🔹 Expression orale", "ru": "🔹 Говорение", "zh": "🔹 口语", "ur": "🔹 گفتگو",
        "hi": "🔹 बोलना", "fa": "🔹 مکالمه", "id": "🔹 Berbicara",
    },
    "skill_writing": {
        "ar": "🔹 الكتابة", "en": "🔹 Writing", "tr": "🔹 Yazma", "es": "🔹 Escritura",
        "fr": "🔹 Écriture", "ru": "🔹 Письмо", "zh": "🔹 写作", "ur": "🔹 تحریر",
        "hi": "🔹 लेखन", "fa": "🔹 نوشتن", "id": "🔹 Menulis",
    },
    "correct_answer": {
        "ar": "✅ إجابة صحيحة!", "en": "✅ Correct!", "tr": "✅ Doğru!", "es": "✅ ¡Correcto!",
        "fr": "✅ Correct !", "ru": "✅ Верно!", "zh": "✅ 正确！", "ur": "✅ درست جواب!",
        "hi": "✅ सही उत्तर!", "fa": "✅ پاسخ درست!", "id": "✅ Benar!",
    },
    "wrong_answer_retry": {
        "ar": "❌ ليست صحيحة تمامًا. حاول مرة أخرى.",
        "en": "❌ Not quite. Try again.",
        "tr": "❌ Tam olarak değil. Tekrar deneyin.",
        "es": "❌ No es correcto del todo. Inténtalo de nuevo.",
        "fr": "❌ Pas tout à fait. Réessayez.",
        "ru": "❌ Не совсем верно. Попробуйте снова.",
        "zh": "❌ 不太对，请再试一次。",
        "ur": "❌ بالکل درست نہیں۔ دوبارہ کوشش کریں۔",
        "hi": "❌ बिल्कुल सही नहीं। पुनः प्रयास करें।",
        "fa": "❌ کاملاً درست نیست. دوباره تلاش کنید.",
        "id": "❌ Belum tepat. Coba lagi.",
    },
    "speaking_prompt_note": {
        "ar": "🎙️ أرسل إجابتك كتسجيل صوتي أو رسالة نصية، وسيصحّحها الذكاء الاصطناعي فورًا.",
        "en": "🎙️ Send your answer as a voice message or text, and AI will correct it right away.",
        "tr": "🎙️ Cevabınızı sesli mesaj veya yazı olarak gönderin, yapay zeka hemen düzeltecek.",
        "es": "🎙️ Envía tu respuesta como mensaje de voz o texto, y la IA la corregirá de inmediato.",
        "fr": "🎙️ Envoyez votre réponse sous forme de message vocal ou texte, l'IA la corrigera immédiatement.",
        "ru": "🎙️ Отправьте ответ голосовым или текстовым сообщением, ИИ сразу его проверит.",
        "zh": "🎙️ 请以语音或文字发送您的答案，AI 将立即为您批改。",
        "ur": "🎙️ اپنا جواب صوتی پیغام یا تحریری پیغام کے طور پر بھیجیں، مصنوعی ذہانت فوراً درست کرے گی۔",
        "hi": "🎙️ अपना उत्तर वॉइस मैसेज या टेक्स्ट के रूप में भेजें, AI तुरंत सुधार देगा।",
        "fa": "🎙️ پاسخ خود را به‌صورت پیام صوتی یا متنی ارسال کنید، هوش مصنوعی فوراً آن را تصحیح می‌کند.",
        "id": "🎙️ Kirim jawaban Anda berupa pesan suara atau teks, AI akan langsung mengoreksinya.",
    },
    "writing_prompt_note": {
        "ar": "✍️ اكتب إجابتك، وسيصحّحها الذكاء الاصطناعي فورًا.",
        "en": "✍️ Write your answer, and AI will correct it right away.",
        "tr": "✍️ Cevabınızı yazın, yapay zeka hemen düzeltecek.",
        "es": "✍️ Escribe tu respuesta, y la IA la corregirá de inmediato.",
        "fr": "✍️ Écrivez votre réponse, l'IA la corrigera immédiatement.",
        "ru": "✍️ Напишите ваш ответ, ИИ сразу его проверит.",
        "zh": "✍️ 请写下您的答案，AI 将立即为您批改。",
        "ur": "✍️ اپنا جواب لکھیں، مصنوعی ذہانت فوراً درست کرے گی۔",
        "hi": "✍️ अपना उत्तर लिखें, AI तुरंत सुधार देगा।",
        "fa": "✍️ پاسخ خود را بنویسید، هوش مصنوعی فوراً آن را تصحیح می‌کند.",
        "id": "✍️ Tulis jawaban Anda, AI akan langsung mengoreksinya.",
    },
    "ai_analyzing": {
        "ar": "⏳ جارٍ تحليل إجابتك...", "en": "⏳ Analyzing your answer...", "tr": "⏳ Cevabınız analiz ediliyor...",
        "es": "⏳ Analizando tu respuesta...", "fr": "⏳ Analyse de votre réponse en cours...",
        "ru": "⏳ Анализируем ваш ответ...", "zh": "⏳ 正在分析您的答案...", "ur": "⏳ آپ کے جواب کا تجزیہ ہو رہا ہے...",
        "hi": "⏳ आपके उत्तर का विश्लेषण हो रहा है...", "fa": "⏳ در حال تحلیل پاسخ شما...",
        "id": "⏳ Menganalisis jawaban Anda...",
    },
    "ai_correction_unavailable": {
        "ar": "⚠️ تعذّر تصحيح إجابتك آليًا الآن، لكن تم حفظها وستُراجَع قريبًا.",
        "en": "⚠️ Couldn't auto-correct your answer right now, but it's been saved and will be reviewed soon.",
        "tr": "⚠️ Cevabınız şu anda otomatik düzeltilemedi, ancak kaydedildi ve yakında incelenecek.",
        "es": "⚠️ No se pudo corregir tu respuesta automáticamente ahora, pero se ha guardado y será revisada pronto.",
        "fr": "⚠️ Impossible de corriger automatiquement votre réponse pour le moment, mais elle a été enregistrée et sera examinée bientôt.",
        "ru": "⚠️ Не удалось автоматически проверить ваш ответ сейчас, но он сохранён и будет рассмотрен позже.",
        "zh": "⚠️ 目前无法自动批改您的答案，但已保存，稍后将进行审核。",
        "ur": "⚠️ ابھی آپ کا جواب خودکار طور پر درست نہیں ہو سکا، لیکن محفوظ کر لیا گیا ہے اور جلد جائزہ لیا جائے گا۔",
        "hi": "⚠️ अभी आपका उत्तर स्वतः सुधारा नहीं जा सका, लेकिन इसे सहेज लिया गया है और जल्द ही समीक्षा की जाएगी।",
        "fa": "⚠️ اکنون امکان تصحیح خودکار پاسخ شما نبود، اما ذخیره شد و به‌زودی بررسی می‌شود.",
        "id": "⚠️ Tidak dapat mengoreksi jawaban Anda secara otomatis saat ini, tetapi telah disimpan dan akan ditinjau segera.",
    },
    "lesson_complete": {
        "ar": "🎉 أحسنت! أتممت هذا الدرس بنجاح.", "en": "🎉 Well done! You completed this lesson.",
        "tr": "🎉 Aferin! Bu dersi tamamladınız.", "es": "🎉 ¡Bien hecho! Has completado esta lección.",
        "fr": "🎉 Bravo ! Vous avez terminé cette leçon.", "ru": "🎉 Отлично! Вы завершили этот урок.",
        "zh": "🎉 太棒了！您已完成本课。", "ur": "🎉 شاباش! آپ نے یہ سبق کامیابی سے مکمل کر لیا۔",
        "hi": "🎉 शाबाश! आपने यह पाठ पूरा कर लिया।", "fa": "🎉 آفرین! این درس را با موفقیت به پایان رساندید.",
        "id": "🎉 Kerja bagus! Anda telah menyelesaikan pelajaran ini.",
    },
    "program_complete": {
        "ar": "🏆 مبارك! أتممت المستوى بالكامل. شهادتك قيد التجهيز.",
        "en": "🏆 Congratulations! You completed the full level. Your certificate is being prepared.",
        "tr": "🏆 Tebrikler! Seviyeyi tamamen bitirdiniz. Sertifikanız hazırlanıyor.",
        "es": "🏆 ¡Felicidades! Has completado todo el nivel. Tu certificado se está preparando.",
        "fr": "🏆 Félicitations ! Vous avez terminé tout le niveau. Votre certificat est en préparation.",
        "ru": "🏆 Поздравляем! Вы полностью завершили уровень. Ваш сертификат готовится.",
        "zh": "🏆 恭喜！您已完成整个级别。您的证书正在准备中。",
        "ur": "🏆 مبارک ہو! آپ نے پوری سطح مکمل کر لی۔ آپ کا سرٹیفکیٹ تیار کیا جا رہا ہے۔",
        "hi": "🏆 बधाई हो! आपने पूरा स्तर पूरा कर लिया। आपका प्रमाणपत्र तैयार किया जा रहा है।",
        "fa": "🏆 تبریک! شما کل سطح را به پایان رساندید. گواهی شما در حال آماده‌سازی است.",
        "id": "🏆 Selamat! Anda telah menyelesaikan seluruh level. Sertifikat Anda sedang disiapkan.",
    },
    "trial_ended": {
        "ar": "🎓 انتهت الفترة التجريبية المجانية.\nالمستوى الكامل مدفوع (5$). سيتم تفعيل الاشتراك قريبًا.",
        "en": "🎓 Your free trial has ended.\nThe full level is paid ($5). Subscription activation is coming soon.",
        "tr": "🎓 Ücretsiz deneme süreniz sona erdi.\nTam seviye ücretlidir (5$). Abonelik yakında etkinleştirilecek.",
        "es": "🎓 Tu prueba gratuita ha terminado.\nEl nivel completo es de pago (5$). La activación de la suscripción llegará pronto.",
        "fr": "🎓 Votre essai gratuit est terminé.\nLe niveau complet est payant (5$). L'activation de l'abonnement arrive bientôt.",
        "ru": "🎓 Ваш бесплатный пробный период закончился.\nПолный уровень платный (5$). Активация подписки скоро появится.",
        "zh": "🎓 您的免费试用已结束。\n完整级别为付费内容（5美元）。订阅激活功能即将推出。",
        "ur": "🎓 آپ کی مفت آزمائشی مدت ختم ہو گئی۔\nمکمل سطح ادائیگی کے ساتھ ہے (5$)۔ رکنیت کی فعال کاری جلد آ رہی ہے۔",
        "hi": "🎓 आपकी मुफ्त परीक्षण अवधि समाप्त हो गई है।\nपूर्ण स्तर सशुल्क है (5$)। सदस्यता सक्रियण जल्द आ रहा है।",
        "fa": "🎓 دوره آزمایشی رایگان شما به پایان رسید.\nسطح کامل پولی است (۵ دلار). فعال‌سازی اشتراک به‌زودی ارائه می‌شود.",
        "id": "🎓 Masa percobaan gratis Anda telah berakhir.\nLevel lengkap berbayar ($5). Aktivasi langganan akan segera hadir.",
    },
    "not_a_study_day": {
        "ar": "اليوم يوم إجازتك 🌙", "en": "Today is your vacation day 🌙", "tr": "Bugün izin gününüz 🌙",
        "es": "Hoy es tu día de descanso 🌙", "fr": "Aujourd'hui est votre jour de repos 🌙",
        "ru": "Сегодня ваш выходной день 🌙", "zh": "今天是您的休息日 🌙", "ur": "آج آپ کی چھٹی کا دن ہے 🌙",
        "hi": "आज आपकी छुट्टी का दिन है 🌙", "fa": "امروز روز تعطیلی شماست 🌙", "id": "Hari ini adalah hari libur Anda 🌙",
    },
    "progress_title": {
        "ar": "📊 تقدّمك", "en": "📊 Your Progress", "tr": "📊 İlerlemeniz", "es": "📊 Tu progreso",
        "fr": "📊 Votre progression", "ru": "📊 Ваш прогресс", "zh": "📊 您的进度", "ur": "📊 آپ کی پیش رفت",
        "hi": "📊 आपकी प्रगति", "fa": "📊 پیشرفت شما", "id": "📊 Kemajuan Anda",
    },
    "progress_body": {
        "ar": "المستوى: {level}\nالدروس المكتملة: {completed}/{total}\nالدرس الحالي: {current}",
        "en": "Level: {level}\nCompleted lessons: {completed}/{total}\nCurrent lesson: {current}",
        "tr": "Seviye: {level}\nTamamlanan dersler: {completed}/{total}\nMevcut ders: {current}",
        "es": "Nivel: {level}\nLecciones completadas: {completed}/{total}\nLección actual: {current}",
        "fr": "Niveau : {level}\nLeçons terminées : {completed}/{total}\nLeçon actuelle : {current}",
        "ru": "Уровень: {level}\nЗавершено уроков: {completed}/{total}\nТекущий урок: {current}",
        "zh": "级别：{level}\n已完成课程：{completed}/{total}\n当前课程：{current}",
        "ur": "سطح: {level}\nمکمل شدہ اسباق: {completed}/{total}\nموجودہ سبق: {current}",
        "hi": "स्तर: {level}\nपूर्ण पाठ: {completed}/{total}\nवर्तमान पाठ: {current}",
        "fa": "سطح: {level}\nدرس‌های تکمیل‌شده: {completed}/{total}\nدرس فعلی: {current}",
        "id": "Level: {level}\nPelajaran selesai: {completed}/{total}\nPelajaran saat ini: {current}",
    },
    "no_active_program": {
        "ar": "لم تبدأ البرنامج بعد. أرسل /start للبدء.",
        "en": "You haven't started the program yet. Send /start to begin.",
        "tr": "Programa henüz başlamadınız. Başlamak için /start gönderin.",
        "es": "Aún no has comenzado el programa. Envía /start para comenzar.",
        "fr": "Vous n'avez pas encore commencé le programme. Envoyez /start pour commencer.",
        "ru": "Вы ещё не начали программу. Отправьте /start, чтобы начать.",
        "zh": "您尚未开始课程。请发送 /start 开始。",
        "ur": "آپ نے ابھی پروگرام شروع نہیں کیا۔ شروع کرنے کے لیے /start بھیجیں۔",
        "hi": "आपने अभी तक कार्यक्रम शुरू नहीं किया है। शुरू करने के लिए /start भेजें।",
        "fa": "شما هنوز برنامه را شروع نکرده‌اید. برای شروع /start را ارسال کنید.",
        "id": "Anda belum memulai program. Kirim /start untuk memulai.",
    },
    "generic_error": {
        "ar": "⚠️ حدث خطأ غير متوقع. تم إبلاغ المسؤولين، حاول لاحقًا.",
        "en": "⚠️ An unexpected error occurred. Admins have been notified, please try again later.",
        "tr": "⚠️ Beklenmeyen bir hata oluştu. Yöneticilere bildirildi, lütfen daha sonra tekrar deneyin.",
        "es": "⚠️ Ocurrió un error inesperado. Se ha notificado a los administradores, inténtalo más tarde.",
        "fr": "⚠️ Une erreur inattendue s'est produite. Les administrateurs ont été informés, veuillez réessayer plus tard.",
        "ru": "⚠️ Произошла непредвиденная ошибка. Администраторы уведомлены, попробуйте позже.",
        "zh": "⚠️ 发生意外错误。管理员已收到通知，请稍后重试。",
        "ur": "⚠️ ایک غیر متوقع خرابی پیش آئی۔ منتظمین کو مطلع کر دیا گیا ہے، براہ کرم بعد میں دوبارہ کوشش کریں۔",
        "hi": "⚠️ एक अप्रत्याशित त्रुटि हुई। व्यवस्थापकों को सूचित कर दिया गया है, कृपया बाद में पुनः प्रयास करें।",
        "fa": "⚠️ خطای غیرمنتظره‌ای رخ داد. به مدیران اطلاع داده شد، لطفاً بعداً دوباره امتحان کنید.",
        "id": "⚠️ Terjadi kesalahan tak terduga. Admin telah diberi tahu, silakan coba lagi nanti.",
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


# ترتيب أيام الأسبوع لعرضها كأزرار: Python weekday 0=الاثنين ... 6=الأحد
WEEKDAY_KEYS = [
    (0, "day_mon"), (1, "day_tue"), (2, "day_wed"), (3, "day_thu"),
    (4, "day_fri"), (5, "day_sat"), (6, "day_sun"),
]


def weekday_name(weekday_num: int, lang: str) -> str:
    for num, key in WEEKDAY_KEYS:
        if num == weekday_num:
            return t(key, lang)
    return str(weekday_num)


def vacation_day_keyboard_rows(lang: str, exclude: int = None):
    """يبني صفوف أزرار اختيار يوم إجازة، مع استثناء يوم مُختار مسبقًا (لعدم تكراره)."""
    rows = []
    for num, key in WEEKDAY_KEYS:
        if exclude is not None and num == exclude:
            continue
        rows.append((t(key, lang), f"vacday|{num}"))
    return rows
