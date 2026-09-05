# -*- coding: utf-8 -*-
"""
translations.py
كل نصوص واجهة البوت (التعليمات، الأزرار، أسماء الأيام، والرسائل) مترجمة لـ 11 لغة مع دعم المستويات (A0-B2).
"""

from telegram import InlineKeyboardButton

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

# أسماء الأيام مترجمة للـ 11 لغة (الترتيب: الأحد إلى السبت)
DAYS_OF_WEEK = {
    "ar": ["الأحد", "الإثنين", "الثلاثاء", "الأربعاء", "الخميس", "الجمعة", "السبت"],
    "en": ["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"],
    "tr": ["Pazar", "Pazartesi", "Salı", "Çarşamba", "Perşembe", "Cuma", "Cumartesi"],
    "fr": ["Dimanche", "Lundi", "Mardi", "Mercredi", "Jeudi", "Vendredi", "Samedi"],
    "es": ["Domingo", "Lunes", "Martes", "Miércoles", "Jueves", "Viernes", "Sábado"],
    "de": ["Sonntag", "Montag", "Dienstag", "Mittwoch", "Donnerstag", "Freitag", "Samstag"],
    "ru": ["Воскресенье", "Понедельник", "Вторник", "Среда", "Четверг", "Пятница", "Суббота"],
    "id": ["Minggu", "Senin", "Selasa", "Rabu", "Kamis", "Jumat", "Sabtu"],
    "ur": ["اتوار", "پیر", "منگل", "بدھ", "جمعرات", "جمعہ", "ہفتہ"],
    "bn": ["রবিবার", "সোমবার", "মঙ্গলবার", "বুধবারে", "বৃহস্পতিবার", "শুক্রবার", "শনিবার"],
    "fa": ["یکشنبه", "دوشنبه", "سه‌شنبه", "چهارشنبه", "پنجشنبه", "جمعه", "شنبه"],
}

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
        "ar": "📚 يتوفر لدينا محتوى من مستوى الحروف (A0) وحتى المستويات (A1 إلى B2).\n\n📌 مستوى الحروف (A0) يحتوي على 4 دروس.\n📌 باقي المستويات (A1-B2) يحتوي كل منها على 18 درسًا.\n🎁 أول 5 دروس مجانية تمامًا، وبعدها يتطلب اشتراك بقيمة 5 دولار فقط للمستوى الكامل.",
        "en": "📚 We offer content from letter level (A0) to levels (A1 to B2).\n\n📌 Level A0 contains 4 lessons.\n📌 Other levels (A1-B2) contain 18 lessons each.\n🎁 The first 5 lessons are completely free, after which a $5 subscription is required for the full level.",
        "tr": "📚 Harf seviyesinden (A0) B2'ye kadar içerik sunuyoruz.\n\n📌 A0 seviyesi 4 ders içerir.\n📌 Diğer seviyeler (A1-B2) 18 ders içerir.\n🎁 İlk 5 ders tamamen ücretsizdir, sonrasında 5$ abonelik gereklidir.",
        "fr": "📚 Nous proposons du niveau A0 à B2.\n\n📌 Le niveau A0 contient 4 leçons.\n📌 Les autres niveaux contiennent 18 leçons.\n🎁 Les 5 premières leçons sont gratuites.",
        "es": "📚 Ofrecemos contenido desde el nivel A0 hasta B2.\n\n📌 El nivel A0 tiene 4 lecciones.\n📌 Los demás niveles tienen 18 lecciones.\n🎁 Las primeras 5 lecciones son gratis.",
        "de": "📚 Wir bieten Inhalte von Stufe A0 bis B2.\n\n📌 Stufe A0 enthält 4 Lektionen.\n📌 Andere Stufen enthalten 18 Lektionen.\n🎁 Die ersten 5 Lektionen sind kostenlos.",
        "ru": "📚 Доступны уровни от A0 до B2.\n\n📌 Уровень A0 содержит 4 урока.\n📌 Остальные уровни содержат по 18 уроков.\n🎁 Первые 5 уроков бесплатны.",
        "id": "📚 Kami menyediakan konten dari level A0 hingga B2.\n\n📌 Level A0 berisi 4 pelajaran.\n📌 Level lainnya berisi 18 pelajaran.\n🎁 5 pelajaran pertama gratis.",
        "ur": "📚 ہمارے پاس A0 سے B2 تک مواد دستیاب ہے۔\n\n📌 سطح A0 میں 4 اسباق ہیں۔\n📌 باقی سطحوں میں 18 اسباق ہیں۔\n🎁 پہلے 5 اسباق مفت ہیں۔",
        "bn": "📚 আমাদের কাছে A0 থেকে B2 স্তরের বিষয়বস্তু রয়েছে।\n\n📌 A0 স্তরে ৪টি পাঠ রয়েছে।\n📌 অন্যান্য স্তরে ১৮টি পাঠ রয়েছে।\n🎁 প্রথম ৫টি পাঠ বিনামূল্যে।",
        "fa": "📚 محتوای سطح A0 تا B2 موجود است.\n\n📌 سطح A0 شامل ۴ درس است.\n📌 سایر سطوح شامل ۱۸ درس هستند.\n🎁 ۵ درس اول رایگان است.",
    },
    "ask_level_selection": {
        "ar": "🎯 يرجى اختيار مستواك:\nيمكنك إجراء اختبار تحديد المستوى أولاً، أو اختيار مستواك مباشرة (أو البدء من A0 لمن لا يعرف الحروف).",
        "en": "🎯 Please choose your level:\nYou can take a placement test first, or select your level directly (or start from A0 if you don't know the letters).",
        "tr": "🎯 Lütfen seviyenizi seçin:\nÖnce seviye tespit sınavına girebilir veya doğrudan seviyenizi seçebilirsiniz (harfleri bilmiyorsanız A0'dan başlayın).",
        "fr": "🎯 Veuillez choisir votre niveau :\nVous pouvez passer un test de placement ou choisir directement votre niveau (ou commencer à A0).",
        "es": "🎯 Por favor elije tu nivel:\nPuedes hacer una prueba de nivel primero o elegir tu nivel directamente (o empezar desde A0).",
        "de": "🎯 Bitte wählen Sie Ihr Niveau:\nMachen Sie einen Einstufungstest oder wählen Sie direkt Ihr Niveau (oder starten Sie bei A0).",
        "ru": "🎯 Пожалуйста, выберите уровень:\nПройдите тест или выберите уровень напрямую (или начните с A0).",
        "id": "🎯 Silakan pilih level Anda:\nIkuti tes penempatan terlebih dahulu atau pilih langsung (atau mulai dari A0).",
        "ur": "🎯 براہ کرم اپنی سطح منتخب کریں:\nآپ پہلے ٹیسٹ دے سکتے ہیں یا براہ راست سطح منتخب کر سکتے ہیں۔",
        "bn": "🎯 আপনার স্তর নির্বাচন করুন:\nআপনি প্রথমে টেস্ট দিতে পারেন অথবা সরাসরি স্তর বেছে নিতে পারেন।",
        "fa": "🎯 لطفا سطح خود را انتخاب کنید:\nمی‌توانید ابتدا آزمون تعیین سطح بدهید یا مستقیماً انتخاب کنید.",
    },
    "btn_take_placement_test": {
        "ar": "📝 إجراء اختبار تحديد المستوى",
        "en": "📝 Take Placement Test",
        "tr": "📝 Seviye Tespit Sınavı Yap",
        "fr": "📝 Passer le test de niveau",
        "es": "📝 Hacer prueba de nivel",
        "de": "📝 Einstufungstest machen",
        "ru": "📝 Пройти тест уровня",
        "id": "📝 Ikuti Tes Penempatan",
        "ur": "📝 تعینِ سطح کا ٹیسٹ دیں",
        "bn": "📝 প্লেসমেন্ট টেস্ট দিন",
        "fa": "📝 انجام آزمون تعیین سطح",
    },
    "level_chosen": {
        "ar": "✅ تم اختيار المستوى: {level}. دعنا نحدد وقت درسك اليومي الآن:",
        "en": "✅ Level selected: {level}. Let's set your daily lesson time now:",
        "tr": "✅ Seçilen seviye: {level}. Şimdi günlük ders saatinizi belirleyelim:",
        "fr": "✅ Niveau choisi : {level}. Définissons l'heure de votre leçon quotidienne :",
        "es": "✅ Nivel seleccionado: {level}. Establezcamos la hora de tu lección diaria:",
        "de": "✅ Gewähltes Niveau: {level}. Legen wir Ihre tägliche Unterrichtszeit fest:",
        "ru": "✅ Уровень выбран: {level}. Установим время урока:",
        "id": "✅ Level dipilih: {level}. Mari tentukan waktu pelajaran harian Anda:",
        "ur": "✅ سطح منتخب ہو گئی: {level}۔ اب اپنے روزانہ سبق کا وقت طے کریں:",
        "bn": "✅ স্তর নির্বাচিত হয়েছে: {level}। আপনার পাঠের সময় নির্ধারণ করুন:",
        "fa": "✅ سطح انتخاب شد: {level}. زمان درس روزانه را تعیین کنیم:",
    },
    "ask_time": {
        "ar": "اختر الوقت المناسب لوصول درسك اليومي:",
        "en": "Choose the time you'd like your daily lesson to arrive:",
        "tr": "Günlük dersinizin geleceği uygun saati seçin:",
        "fr": "Choisissez l'heure de réception de votre leçon quotidienne :",
        "es": "Elige la hora para recibir tu lección diaria:",
        "de": "Wählen Sie die Uhrzeit für Ihre tägliche Lektion:",
        "ru": "Выберите время для получения ежедневного урока:",
        "id": "Pilih waktu untuk menerima pelajaran harian Anda:",
        "ur": "اپنے روزانہ سبق کے حصول کا مناسب وقت منتخب کریں:",
        "bn": "আপনার দৈনিক পাঠ পাওয়ার উপযুক্ত সময় বেছে নিন:",
        "fa": "زمان مناسب برای دریافت درس روزانه را انتخاب کنید:",
    },
    "time_confirmed": {
        "ar": "✅ تم! تم ضبط وقت الدرس الساعة {time}.",
        "en": "✅ Done! Lesson time set to {time}.",
        "tr": "✅ Tamam! Ders saati {time} olarak ayarlandı.",
        "fr": "✅ Terminé ! Heure de la leçon réglée à {time}.",
        "es": "✅ ¡Hecho! Hora de la lección establecida a las {time}.",
        "de": "✅ Erledigt! Unterrichtszeit auf {time} eingestellt.",
        "ru": "✅ Готово! Время урока установлено на {time}.",
        "id": "✅ Selesai! Waktu pelajaran diatur ke {time}.",
        "ur": "✅ ہو گیا! سبق کا وقت {time} مقرر کر دیا گیا ہے۔",
        "bn": "✅ সম্পন্ন! পাঠের সময় {time} নির্ধারণ করা হয়েছে।",
        "fa": "✅ انجام شد! زمان درس روی {time} تنظیم شد.",
    },
    "ask_rest_days": {
        "ar": "🗓️ اختر أيام الإجازة التي تريدها (يومان في الأسبوع)، حيث لن يُرسل لك فيها دروس:\n(اضغط على اليوم لاختياره أو إلغائه، ثم اضغط حفظ)",
        "en": "🗓️ Choose your 2 rest days per week where no lessons will be sent:\n(Tap a day to select/deselect, then click save)",
        "tr": "🗓️ Ders gönderilmeyecek 2 tatil gününüzü seçin:\n(Seçmek veya kaldırmak için güne dokunun, ardından kaydet'e basın)",
        "fr": "🗓️ Choisissez vos 2 jours de repos par semaine sans leçons :\n(Appuyez sur un jour pour sélectionner/désélectionner, puis cliquez sur enregistrer)",
        "es": "🗓️ Elige tus 2 días de descanso por semana donde no se enviarán lecciones:\n(Toca un día para seleccionar/deseleccionar, luego haz clic en guardar)",
        "de": "🗓️ Wählen Sie Ihre 2 Ruhetage pro Woche, an denen keine Lektionen gesendet werden:\n(Tippen Sie auf einen Tag und klicken Sie auf Speichern)",
        "ru": "🗓️ Выберите 2 дня отдыха в неделю, когда уроки не будут отправляться:\n(Нажмите на день, затем сохраните)",
        "id": "🗓️ Pilih 2 hari istirahat per minggu di mana tidak ada pelajaran yang dikirim:\n(Ketuk hari untuk memilih/membatalkan pilihan, lalu klik simpan)",
        "ur": "🗓️ ہفتے کے اپنے 2 آرام کے دن منتخب کریں جن میں کوئی سبق نہیں بھیجا جائے گا:\n(منتخب کرنے کے لیے دن پر ٹیپ کریں اور پھر محفوظ کریں پر کلک کریں)",
        "bn": "🗓️ সপ্তাহে আপনার ২ দিন ছুটির দিন বেছে নিন যেখানে কোনো পাঠ পাঠানো হবে না:\n(নির্বাচন করতে দিনে ট্যাপ করুন এবং সংরক্ষণ করুন)",
        "fa": "🗓️ ۲ روز استراحت در هفته را که در آن‌ها درسی ارسال نمی‌شود انتخاب کنید:\n(برای انتخاب روی روز ضربه بزنید و سپس ذخیره را بزنید)",
    },
    "btn_save_rest_days": {
        "ar": "💾 حفظ أيام الإجازة",
        "en": "💾 Save Rest Days",
        "tr": "💾 Tatil Günlerini Kaydet",
        "fr": "💾 Enregistrer les jours de repos",
        "es": "💾 Guardar días de descanso",
        "de": "💾 Ruhetage speichern",
        "ru": "💾 Сохранить дни отдыха",
        "id": "💾 Simpan Hari Istirahat",
        "ur": "💾 آرام کے دن محفوظ کریں",
        "bn": "💾 ছুটির দিন সংরক্ষণ করুন",
        "fa": "💾 ذخیره روزهای استراحت",
    },
    "ask_gender": {
        "ar": "👤 يرجى اختيار الجنس (لتوجيهك إلى مجموعة الدردشة المناسبة):",
        "en": "👤 Please select your gender (to direct you to the appropriate chat group):",
        "tr": "👤 Lütfen cinsiyetinizi seçin (sizi uygun sohbet grubuna yönlendirmek için):",
        "fr": "👤 Veuillez sélectionner votre genre (pour vous diriger vers le groupe de discussion approprié) :",
        "es": "👤 Por favor selecciona tu género (para dirigirte al grupo de chat correspondiente):",
        "de": "👤 Bitte wählen Sie Ihr Geschlecht (um Sie zur entsprechenden Chat-Gruppe weiterzuleiten):",
        "ru": "👤 Пожалуйста, выберите ваш пол (чтобы направить вас в соответствующий чат):",
        "id": "👤 Silakan pilih jenis kelamin Anda (untuk mengarahkan Anda ke grup obrolan yang sesuai):",
        "ur": "👤 براہ کرم اپنی صنف منتخب کریں (آپ کو مناسب چیٹ گروپ کی طرف رہنمائی کرنے کے لیے):",
        "bn": "👤 অনুগ্রহ করে আপনার লিঙ্গ নির্বাচন করুন (উপযুক্ত চ্যাট গ্রুপে আপনাকে গাইড করার জন্য):",
        "fa": "👤 لطفاً جنسیت خود را انتخاب کنید (تا شما را به گروه چت مناسب هدایت کنیم):",
    },
    "btn_male": {
        "ar": "👨 رجل",
        "en": "👨 Male",
        "tr": "👨 Erkek",
        "fr": "👨 Homme",
        "es": "👨 Hombre",
        "de": "👨 Männlich",
        "ru": "👨 Мужчина",
        "id": "👨 Pria",
        "ur": "👨 مرد",
        "bn": "👨 পুরুষ",
        "fa": "👨 مرد",
    },
    "btn_female": {
        "ar": "👩 امرأة",
        "en": "👩 Female",
        "tr": "👩 Kadın",
        "fr": "👩 Femme",
        "es": "👩 Mujer",
        "de": "👩 Weiblich",
        "ru": "👩 Женщина",
        "id": "👩 Wanita",
        "ur": "👩 عورت",
        "bn": "👩 নারী",
        "fa": "👩 زن",
    },
    "registration_summary": {
        "ar": "📋 **ملخص بياناتك وتسجيلك:**\n\n👤 الاسم: {name}\n🎯 المستوى: {level}\n⏰ وقت الدرس: {time}\n🗓️ أيام الإجازة: {rest_days}\n👥 مجموعة الدردشة الخاصة بك:\n🔗 {chat_link}\n\n🎉 تم إعداد جدولك بالكامل وانطلقت رحلتك!",
        "en": "📋 **Your Registration Summary:**\n\n👤 Name: {name}\n🎯 Level: {level}\n⏰ Lesson Time: {time}\n🗓️ Rest Days: {rest_days}\n👥 Your Chat Group:\n🔗 {chat_link}\n\n🎉 Your schedule is fully set and your journey has begun!",
        "tr": "📋 **Kayıt Özetiniz:**\n\n👤 İsim: {name}\n🎯 Seviye: {level}\n⏰ Ders Saati: {time}\n🗓️ Tatil Günleri: {rest_days}\n👥 Sohbet Grubunuz:\n🔗 {chat_link}\n\n🎉 Programınız tamamen hazır ve yolculuğunuz başladı!",
        "fr": "📋 **Résumé de votre inscription :**\n\n👤 Nom : {name}\n🎯 Niveau : {level}\n⏰ Heure de leçon : {time}\n🗓️ Jours de repos : {rest_days}\n👥 Votre groupe de discussion :\n🔗 {chat_link}\n\n🎉 Votre programme est prêt et votre voyage commence !",
        "es": "📋 **Resumen de tu registro:**\n\n👤 Nombre: {name}\n🎯 Nivel: {level}\n⏰ Hora de la lección: {time}\n🗓️ Días de descanso: {rest_days}\n👥 Tu grupo de chat:\n🔗 {chat_link}\n\n🎉 ¡Tu horario está listo y tu viaje ha comenzado!",
        "de": "📋 **Ihre Registrierungsübersicht:**\n\n👤 Name: {name}\n🎯 Niveau: {level}\n⏰ Lektionszeit: {time}\n🗓️ Ruhetage: {rest_days}\n👥 Ihre Chat-Gruppe:\n🔗 {chat_link}\n\n🎉 Ihr Zeitplan ist fertig und Ihre Reise beginnt!",
        "ru": "📋 **Сводка вашей регистрации:**\n\n👤 Имя: {name}\n🎯 Уровень: {level}\n⏰ Время урока: {time}\n🗓️ Дни отдыха: {rest_days}\n👥 Ваш чат:\n🔗 {chat_link}\n\n🎉 Ваш график составлен, и путешествие началось!",
        "id": "📋 **Ringkasan Pendaftaran Anda:**\n\n👤 Nama: {name}\n🎯 Level: {level}\n⏰ Waktu Pelajaran: {time}\n🗓️ Hari Istirahat: {rest_days}\n👥 Grup Obrolan Anda:\n🔗 {chat_link}\n\n🎉 Jadwal Anda sudah siap dan perjalanan dimulai!",
        "ur": "📋 **آپ کی رجسٹریشن کا خلاصہ:**\n\n👤 نام: {name}\n🎯 سطح: {level}\n⏰ سبق کا وقت: {time}\n🗓️ آرام کے دن: {rest_days}\n👥 آپ کا چیٹ گروپ:\n🔗 {chat_link}\n\n🎉 آپ کا شیڈول مکمل طور پر تیار ہے!",
        "bn": "📋 **আপনার নিবন্ধনের সারসংক্ষেপ:**\n\n👤 নাম: {name}\n🎯 স্তর: {level}\n⏰ পাঠের সময়: {time}\n🗓️ ছুটির দিন: {rest_days}\n👥 আপনার চ্যাট গ্রুপ:\n🔗 {chat_link}\n\n🎉 আপনার সময়সূচী প্রস্তুত!",
        "fa": "📋 **خلاصه ثبت‌نام شما:**\n\n👤 نام: {name}\n🎯 سطح: {level}\n⏰ زمان درس: {time}\n🗓️ روزهای استراحت: {rest_days}\n👥 گروه چت شما:\n🔗 {chat_link}\n\n🎉 برنامه شما با موفقیت تنظیم شد!",
    },
    "paywall_tribute": {
        "ar": "🎉 لقد أتممت بنجاح الدروس المجانية المتاحة!\n\nللاستمرار في رحلة تعلم اللغة العربية وفتح المستوى الكامل، يرجى اختيار خطة الاشتراك المناسبة عبر Tribute.\n\nبعد إتمام الدفع، اضغط على زر (تحقق من الاشتراك) لتفعيل حسابك فوراً.",
        "en": "🎉 You have successfully completed the available free lessons!\n\nTo continue your Arabic learning journey and unlock the full level, please choose the appropriate subscription plan via Tribute.\n\nAfter completing the payment, click the (Verify Subscription) button to activate your account immediately.",
        "tr": "🎉 Mevcut ücretsiz dersleri başarıyla tamamladınız!\n\nArapça öğrenme yolculuğunuza devam etmek ve tam seviyenin kilidini açmak için lütfen Tribute üzerinden abone olun.",
        "fr": "🎉 Vous avez terminé les leçons gratuites !\n\nPour continuer, veuillez vous abonner via Tribute.",
        "es": "🎉 ¡Has completado las lecciones gratuitas!\n\nPara continuar, suscríbete a través de Tribute.",
        "de": "🎉 Sie haben die kostenlosen Lektionen abgeschlossen!\n\nUm fortzufahren, abonnieren Sie über Tribute.",
        "ru": "🎉 Вы завершили бесплатные уроки!\n\nДля продолжения оформите подписку через Tribute.",
        "id": "🎉 Anda telah menyelesaikan pelajaran gratis!\n\nUntuk melanjutkan, berlanggananlah melalui Tribute.",
        "ur": "🎉 آپ نے مفت اسباق مکمل کر لیے ہیں!\n\nTribute کے ذریعے سبسکرائب کریں۔",
        "bn": "🎉 আপনি বিনামূল্যে পাঠগুলি সম্পন্ন করেছেন!\n\nTribute এর মাধ্যমে সাবস্ক্রাইব করুন।",
        "fa": "🎉 شما دروس رایگان را به پایان رساندید!\n\nبرای ادامه از طریق Tribute اشتراک تهیه کنید.",
    },
    "skill_intro": {"ar": "🔹 التمهيد", "en": "🔹 Warm-up", "tr": "🔹 Giriş", "fr": "🔹 Échauffement", "es": "🔹 Introducción", "de": "🔹 Aufwärmen", "ru": "🔹 Введение", "id": "🔹 Pemanasan", "ur": "🔹 تعارف", "bn": "🔹 ভূমিকা", "fa": "🔹 مقدمه"},
    "skill_vocab": {"ar": "🔹 المفردات", "en": "🔹 Vocabulary", "tr": "🔹 Kelimeler", "fr": "🔹 Vocabulaire", "es": "🔹 Vocabulario", "de": "🔹 Vokabeln", "ru": "🔹 Словарь", "id": "🔹 Kosakata", "ur": "🔹 الفاظ", "bn": "🔹 শব্দভান্ডার", "fa": "🔹 واژگان"},
    "skill_grammar": {"ar": "🔹 القواعد", "en": "🔹 Grammar", "tr": "🔹 Dilbilgisi", "fr": "🔹 Grammaire", "es": "🔹 Gramática", "de": "🔹 Grammatik", "ru": "🔹 Грамматика", "id": "🔹 Tata Bahasa", "ur": "🔹 قواعد", "bn": "🔹 ব্যাকরণ", "fa": "🔹 دستور زبان"},
    "skill_reading": {"ar": "🔹 القراءة", "en": "🔹 Reading", "tr": "🔹 Okuma", "fr": "🔹 Lecture", "es": "🔹 Lectura", "de": "🔹 Lesen", "ru": "🔹 Чтение", "id": "🔹 Membaca", "ur": "🔹 پڑھنا", "bn": "🔹 পঠন", "fa": "🔹 خواندن"},
    "skill_listening": {"ar": "🔹 الاستماع", "en": "🔹 Listening", "tr": "🔹 Dinleme", "fr": "🔹 Écoute", "es": "🔹 Escucha", "de": "🔹 Hören", "ru": "🔹 Аудирование", "id": "🔹 Mendengarkan", "ur": "🔹 سننا", "bn": "🔹 শ্রবণ", "fa": "🔹 شنیدن"},
    "skill_speaking": {"ar": "🔹 المحادثة", "en": "🔹 Speaking", "tr": "🔹 Konuşma", "fr": "🔹 Expression orale", "es": "🔹 Hablar", "de": "🔹 Sprechen", "ru": "🔹 Разговор", "id": "🔹 Berbicara", "ur": "🔹 بولنا", "bn": "🔹 কথা বলা", "fa": "🔹 مکالمه"},
    "skill_writing": {"ar": "🔹 الكتابة", "en": "🔹 Writing", "tr": "🔹 Yazma", "fr": "🔹 Écriture", "es": "🔹 Escritura", "de": "🔹 Schreiben", "ru": "🔹 Письмо", "id": "🔹 Menulis", "ur": "🔹 لکھنا", "bn": "🔹 লেখা", "fa": "🔹 نوشتن"},
    "correct_answer": {"ar": "✅ إجابة صحيحة!", "en": "✅ Correct!", "tr": "✅ Doğru cevap!", "fr": "✅ Correct !", "es": "✅ ¡Correcto!", "de": "✅ Richtig!", "ru": "✅ Правильно!", "id": "✅ Benar!", "ur": "✅ درست جواب!", "bn": "✅ সঠিক উত্তর!", "fa": "✅ پاسخ درست!"},
    "wrong_answer_retry": {"ar": "❌ ليست صحيحة تمامًا. حاول مرة أخرى.", "en": "❌ Not quite. Try again.", "tr": "❌ Tamamen doğru değil. Tekrar deneyin.", "fr": "❌ Pas tout à fait. Réessayez.", "es": "❌ No exactamente. Inténtalo de nuevo.", "de": "❌ Nicht ganz. Versuchen Sie es noch einmal.", "ru": "❌ Не совсем так. Попробуйте еще раз.", "id": "❌ Kurang tepat. Coba lagi.", "ur": "❌ بالکل درست نہیں۔ دوبارہ کوشش کریں۔", "bn": "❌ ঠিক নয়। আবার চেষ্টা করুন።", "fa": "❌ کاملاً درست نیست. دوباره تلاش کنید."},
    "speaking_prompt_note": {"ar": "🎙️ أرسل إجابتك كتسجيل صوتي أو رسالة نصية.", "en": "🎙️ Send your answer as a voice or text message.", "tr": "🎙️ Cevabınızı sesli veya yazılı mesaj olarak gönderin.", "fr": "🎙️ Envoyez votre réponse sous forme de message vocal ou textuel.", "es": "🎙️ Envía tu respuesta como mensaje de voz o texto.", "de": "🎙️ Senden Sie Ihre Antwort als Sprach- oder Textnachricht.", "ru": "🎙️ Отправьте ответ голосом или текстом.", "id": "🎙️ Kirim jawaban Anda sebagai pesan suara atau teks.", "ur": "🎙️ اپنا جواب صوتی یا تحریری پیغام کے طور پر بھیجیں۔", "bn": "🎙️ আপনার উত্তর ভয়েস বা টেক্সট মেসেজ হিসেবে পাঠান।", "fa": "🎙️ پاسخ خود را به صورت پیام صوتی یا متنی ارسال کنید."},
    "writing_prompt_note": {"ar": "✍️ اكتب إجابتك وسيقوم الذكاء الاصطناعي بتصحيحها.", "en": "✍️ Write your answer and AI will correct it.", "tr": "✍️ Cevabınızı yazın, yapay zeka düzeltecektir.", "fr": "✍️ Écrivez votre réponse et l'IA la corrigera.", "es": "✍️ Escribe tu respuesta y la IA la corregirá.", "de": "✍️ Schreiben Sie Ihre Antwort und die KI korrigiert sie.", "ru": "✍️ Напишите ответ, и ИИ исправит его.", "id": "✍️ Tulis jawaban Anda dan AI akan memperbaikinya.", "ur": "✍️ اپنا جواب لکھیں اور AI اسے درست کرے گا۔", "bn": "✍️ আপনার উত্তর লিখুন এবং AI এটি সংশোধন করবে।", "fa": "✍️ پاسخ خود را بنویسید و هوش مصنوعی آن را اصلاح می‌کند."},
    "ai_analyzing": {"ar": "⏳ جارٍ تحليل إجابتك...", "en": "⏳ Analyzing your answer...", "tr": "⏳ Cevabınız analiz ediliyor...", "fr": "⏳ Analyse de votre réponse...", "es": "⏳ Analizando tu respuesta...", "de": "⏳ Analysiere Ihre Antwort...", "ru": "⏳ Анализ вашего ответа...", "id": "⏳ Menganalisis jawaban Anda...", "ur": "⏳ آپ کے جواب کا تجزیہ کیا جا رہا ہے...", "bn": "⏳ আপনার উত্তর বিশ্লেষণ করা হচ্ছে...", "fa": "⏳ در حال تحلیل پاسخ شما..."},
    "lesson_complete": {"ar": "🎉 أحسنت! أتممت هذا الدرس بنجاح.", "en": "🎉 Well done! You completed this lesson.", "tr": "🎉 Aferin! Bu dersi başarıyla tamamladınız.", "fr": "🎉 Bravo ! Vous avez terminé cette leçon.", "es": "🎉 ¡Bien hecho! Has completado esta lección.", "de": "🎉 Gut gemacht! Sie haben diese Lektion abgeschlossen.", "ru": "🎉 Отлично! Вы завершили этот урок.", "id": "🎉 Bagus sekali! Anda telah menyelesaikan pelajaran ini.", "ur": "🎉 شاباش! آپ نے یہ سبق کامیابی سے مکمل کر لیا ہے۔", "bn": "🎉 চমৎকার! আপনি এই পাঠটি সফলভাবে সম্পন্ন করেছেন።",
    "fa": "🎉 آفرین! شما این درس را با موفقیت به پایان رساندید."},
    "progress_title": {"ar": "📊 تقدّمك", "en": "📊 Your Progress", "tr": "📊 İlerlemeniz", "fr": "📊 Votre progression", "es": "📊 Tu progreso", "de": "📊 Ihr Fortschritt", "ru": "📊 Ваш прогресс", "id": "📊 Kemajuan Anda", "ur": "📊 آپ کی پیش رفت", "bn": "📊 আপনার অগ্রগতি", "fa": "📊 پیشرفت شما"},
    "progress_body": {"ar": "المستوى: {level}\nالدروس المكتملة: {completed}/{total}\nالدرس الحالي: {current}", "en": "Level: {level}\nCompleted: {completed}/{total}\nCurrent: {current}", "tr": "Seviye: {level}\nTamamlanan: {completed}/{total}\nMevcut: {current}", "fr": "Niveau : {level}\nComplétées : {completed}/{total}\nActuelle : {current}", "es": "Nivel: {level}\nCompletadas: {completed}/{total}\nActual: {current}", "de": "Niveau: {level}\nAbgeschlossen: {completed}/{total}\nAktuell: {current}", "ru": "Уровень: {level}\nЗавершено: {completed}/{total}\nТекущий: {current}", "id": "Level: {level}\nSelesai: {completed}/{total}\nSaat ini: {current}", "ur": "سطح: {level}\nمکمل شدہ: {completed}/{total}\nموجودہ: {current}", "bn": "স্তর: {level}\nসম্পন্ন: {completed}/{total}\nবর্তমান: {current}", "fa": "سطح: {level}\nتکمیل شده: {completed}/{total}\nفعلی: {current}"},
    "settings_title": {"ar": "⚙️ الإعدادات", "en": "⚙️ Settings", "tr": "⚙️ Ayarlar", "fr": "⚙️ Paramètres", "es": "⚙️ Ajustes", "de": "⚙️ Einstellungen", "ru": "⚙️ Настройки", "id": "⚙️ Pengaturan", "ur": "⚙️ سیٹنگز", "bn": "⚙️ সেটিংস", "fa": "⚙️ تنظیمات"},
    "settings_change_language": {"ar": "🌐 تغيير اللغة", "en": "🌐 Change language", "tr": "🌐 Dili değiştir", "fr": "🌐 Changer de langue", "es": "🌐 Cambiar idioma", "de": "🌐 Sprache ändern", "ru": "🌐 Изменить язык", "id": "🌐 Ubah bahasa", "ur": "🌐 زبان تبدیل کریں", "bn": "🌐 ভাষা পরিবর্তন করুন", "fa": "🌐 تغییر زبان"},
    "settings_change_time": {"ar": "⏰ تغيير الوقت", "en": "⏰ Change time", "tr": "⏰ Saati değiştir", "fr": "⏰ Changer l'heure", "es": "⏰ Cambiar hora", "de": "⏰ Zeit ändern", "ru": "⏰ Изменить время", "id": "⏰ Ubah waktu", "ur": "⏰ وقت تبدیل کریں", "bn": "⏰ সময় পরিবর্তন করুন", "fa": "⏰ تغییر زمان"},
    "language_changed": {"ar": "✅ تم تغيير اللغة.", "en": "✅ Language changed.", "tr": "✅ Dil değiştirildi.", "fr": "✅ Langue modifiée.", "es": "✅ Idioma cambiado.", "de": "✅ Sprache geändert.", "ru": "✅ Язык изменен.", "id": "✅ Bahasa diubah.", "ur": "✅ زبان تبدیل کر دی گئی ہے۔", "bn": "✅ ভাষা পরিবর্তিত হয়েছে.", "fa": "✅ زبان تغییر کرد."},
    "no_active_program": {"ar": "لم تبدأ البرنامج بعد. أرسل /start للبدء.", "en": "No active program. Send /start.", "tr": "Aktif program yok. /start gönderin.", "fr": "Aucun programme actif. Envoyez /start.", "es": "No hay programa activo. Envía /start.", "de": "Kein aktives Programm. Senden Sie /start.", "ru": "Нет активной программы. Отправьте /start.", "id": "Tidak ada program aktif. Kirim /start.", "ur": "کوئی فعال پروگرام نہیں۔ /start بھیجیں۔", "bn": "কোনো সক্রিয় প্রোগ্রাম নেই। /start পাঠান।", "fa": "برنامه فعالی وجود ندارد. /start را بفرستید."},
}


def t(key: str, lang: str = DEFAULT_LANG, **kwargs) -> str:
    entry = TEXTS.get(key)
    if entry is None:
        return key
    text = entry.get(lang) or entry.get(DEFAULT_LANG) or ""
    if kwargs:
        text = text.format(**kwargs)
    return text


def language_codes() -> list:
    """إرجاع قائمة رموز اللغات المدعومة"""
    return list(SUPPORTED_LANGUAGES.keys())


def language_keyboard_rows():
    rows = []
    for code, (name, flag) in SUPPORTED_LANGUAGES.items():
        rows.append([InlineKeyboardButton(f"{flag} {name}", callback_data=f"lang|{code}")])
    return rows


def get_days_list(lang: str = DEFAULT_LANG):
    """إرجاع قائمة الأيام مترجمة حسب اللغة المختارة"""
    return DAYS_OF_WEEK.get(lang) or DAYS_OF_WEEK.get(DEFAULT_LANG)
