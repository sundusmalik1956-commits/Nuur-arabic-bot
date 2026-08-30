# -*- coding: utf-8 -*-
"""
lesson1.py
الدرس الأول: التحيات والتعارف (مستوى A1 - الوحدة الأولى)

media:
    روابط جوجل درايف حُوِّلت لصيغة تحميل مباشر (uc?export=download&id=FILE_ID) من
    الروابط الفردية المُرسَلة. إن لم يُحمّل تيليجرام أحدها، تأكدي أن إعداد المشاركة
    على كل ملف هو "أي شخص لديه الرابط" (وليس مقيّدًا)، ثم أعيدي المحاولة —
    الصيغة نفسها صحيحة، والمشكلة الوحيدة المحتملة هي صلاحيات المشاركة.
"""

LESSON = {
    "id": 1,
    "title": {
        "ar": "الدرس الأول: التحيات والتعارف",
        "en": "Lesson 1: Greetings and Introductions",
        "tr": "1. Ders: Selamlaşma ve Tanışma",
    },
    "steps": [
        # ---------------------------------------------------------------
        # 1) التمهيد
        # ---------------------------------------------------------------
        {
            "skill": "intro",
            "delay_minutes": 1,
            "image": "https://drive.google.com/uc?export=download&id=1Q0bcNBdIibnRZSjG-x5yxNrfW96pgD0p",
            "text": {
                "ar": "أهلاً بك في عالم اللغة العربية 🌙 التواصل يبدأ بتحية طيبة والتعريف بالاسم.",
                "en": "Welcome to the world of Arabic 🌙 Communication begins with a kind greeting and introducing your name.",
                "tr": "Arapça dünyasına hoş geldiniz 🌙 İletişim güzel bir selamlaşma ve isim tanıtımıyla başlar.",
            },
            "motivational_question": {
                "ar": "كيف تحيي شخصاً في الصباح باللغة العربية؟",
                "en": "How do you greet someone in the morning in Arabic?",
                "tr": "Arapçada birine sabah nasıl selam verirsiniz?",
            },
        },

        # ---------------------------------------------------------------
        # 2) المفردات (7 كلمات أساسية)
        # ---------------------------------------------------------------
        {
            "skill": "vocab",
            "delay_minutes": 1,
            "image": "https://drive.google.com/uc?export=download&id=1oo-3ask9iElyiaxKcVxVubXdQdqG1mmf",
            "vocab_table": [
                {"ar": "مرحباً", "transliteration": "marḥaban", "meaning": {"en": "Hello", "tr": "Merhaba"}},
                {"ar": "صباح الخير", "transliteration": "ṣabāḥ al-khayr", "meaning": {"en": "Good morning", "tr": "Günaydın"}},
                {"ar": "اسمي", "transliteration": "ismī", "meaning": {"en": "My name is", "tr": "Benim adım"}},
                {"ar": "كيف حالك", "transliteration": "kayfa ḥāluk", "meaning": {"en": "How are you", "tr": "Nasılsın"}},
                {"ar": "بخير", "transliteration": "bikhayr", "meaning": {"en": "Fine / Well", "tr": "İyiyim"}},
                {"ar": "شكراً", "transliteration": "shukran", "meaning": {"en": "Thank you", "tr": "Teşekkürler"}},
                {"ar": "مع السلامة", "transliteration": "maʿa as-salāma", "meaning": {"en": "Goodbye", "tr": "Hoşça kal"}},
            ],
            "exercises": [
                {
                    "type": "multiple_choice",
                    "key": "v1",
                    "question": {
                        "ar": "ما معنى كلمة 'مرحباً'؟",
                        "en": "What does the word 'مرحباً' mean?",
                        "tr": "'مرحباً' kelimesinin anlamı nedir?",
                    },
                    "options": [
                        {"ar": "شكراً", "en": "Thank you", "tr": "Teşekkürler"},
                        {"ar": "أهلاً وسهلاً", "en": "Welcome / Hello", "tr": "Hoş geldin"},
                        {"ar": "مع السلامة", "en": "Goodbye", "tr": "Hoşça kal"},
                    ],
                    "correct_index": 1,
                },
                {
                    "type": "multiple_choice",
                    "key": "v2",
                    "question": {
                        "ar": "الترجمة الصحيحة لـ 'صباح الخير' هي:",
                        "en": "The correct translation of 'صباح الخير' is:",
                        "tr": "'صباح الخير' ifadesinin doğru çevirisi:",
                    },
                    "options": [
                        {"en": "Good morning", "tr": "Günaydın", "ar": "صباح الخير"},
                        {"en": "Good evening", "tr": "İyi akşamlar", "ar": "مساء الخير"},
                        {"en": "Good night", "tr": "İyi geceler", "ar": "تصبح على خير"},
                    ],
                    "correct_index": 0,
                },
                {
                    "type": "multiple_choice",
                    "key": "v3",
                    "question": {
                        "ar": "الكلمة المناسبة لتعني 'My name is' باللغة العربية هي:",
                        "en": "The Arabic word that means 'My name is':",
                        "tr": "'Benim adım' anlamına gelen Arapça kelime:",
                    },
                    "options": [
                        {"ar": "كيف حالك", "en": "How are you", "tr": "Nasılsın"},
                        {"ar": "اسمي", "en": "My name is", "tr": "Benim adım"},
                        {"ar": "بخير", "en": "Fine", "tr": "İyiyim"},
                    ],
                    "correct_index": 1,
                },
            ],
        },

        # ---------------------------------------------------------------
        # 3) القاعدة النحوية: الضمائر المنفصلة للمتكلم والمخاطب
        # ---------------------------------------------------------------
        {
            "skill": "grammar",
            "delay_minutes": 1,
            "explanation": {
                "ar": "نستعمل 'أنا' للتعبير عن النفس، و'أنتَ' لمخاطبة الذكر، و'أنتِ' لمخاطبة الأنثى.",
                "en": "We use 'أنا' (I) to speak about ourselves, 'أنتَ' to address a male, and 'أنتِ' to address a female.",
                "tr": "'أنا' kendimizden bahsetmek için, 'أنتَ' bir erkeğe hitap etmek için, 'أنتِ' ise bir kadına hitap etmek için kullanılır.",
            },
            "table": [
                {"pronoun": "أنا", "meaning": {"en": "I", "tr": "Ben"}, "example": "أنا أحدثك"},
                {"pronoun": "أنتَ", "meaning": {"en": "You (m.)", "tr": "Sen (erkek)"}, "example": "أنتَ طالب"},
                {"pronoun": "أنتِ", "meaning": {"en": "You (f.)", "tr": "Sen (kadın)"}, "example": "أنتِ طالبة"},
            ],
            "examples": ["أنا أحدثك.", "أنتَ طالب.", "أنتِ طالبة."],
            "exercises": [
                {
                    "type": "multiple_choice",
                    "key": "g1",
                    "question": {
                        "ar": "اختر الضمير المناسب: (...... طالب مجتهد) — مخاطبة مذكر",
                        "en": "Choose the correct pronoun: (...... طالب مجتهد) — addressing a male",
                        "tr": "Doğru zamiri seçin: (...... طالب مجتهد) — erkeğe hitap",
                    },
                    "options": [
                        {"ar": "أنا", "en": "I", "tr": "Ben"},
                        {"ar": "أنتَ", "en": "You (m.)", "tr": "Sen (erkek)"},
                        {"ar": "أنتِ", "en": "You (f.)", "tr": "Sen (kadın)"},
                    ],
                    "correct_index": 1,
                },
                {
                    "type": "multiple_choice",
                    "key": "g2",
                    "question": {
                        "ar": "اختر الضمير المناسب: (...... معلمة ذكية) — مخاطبة مؤنث",
                        "en": "Choose the correct pronoun: (...... معلمة ذكية) — addressing a female",
                        "tr": "Doğru zamiri seçin: (...... معلمة ذكية) — kadına hitap",
                    },
                    "options": [
                        {"ar": "أنتِ", "en": "You (f.)", "tr": "Sen (kadın)"},
                        {"ar": "أنتَ", "en": "You (m.)", "tr": "Sen (erkek)"},
                        {"ar": "أنا", "en": "I", "tr": "Ben"},
                    ],
                    "correct_index": 0,
                },
                {
                    "type": "multiple_choice",
                    "key": "g3",
                    "question": {
                        "ar": "ما هي الجملة الصحيحة للمتكلم؟",
                        "en": "Which sentence correctly uses the speaker's pronoun?",
                        "tr": "Konuşan kişi için doğru cümle hangisi?",
                    },
                    "options": [
                        {"ar": "أنتَ أدرس العربية"},
                        {"ar": "أنا أدرس العربية"},
                        {"ar": "أنتِ أدرس العربية"},
                    ],
                    "correct_index": 1,
                },
            ],
        },

        # ---------------------------------------------------------------
        # 4) القراءة
        # ---------------------------------------------------------------
        {
            "skill": "reading",
            "delay_minutes": 1,
            "image": "https://drive.google.com/uc?export=download&id=19T76L2ePHv17nui1TQSod-nfKECqMJbr",
            "audio": "https://drive.google.com/uc?export=download&id=1m5qH_TmQ5uPAcxKheuwtucpTmnhM0fJz",
            "reading_text": "أنا أحمد، أنا من الأردن، أنا طالب في الجامعة. وأنتَ، ما اسمك؟ ومن أين أنت؟",
            "exercises": [
                {
                    "type": "multiple_choice",
                    "key": "r1",
                    "question": {
                        "ar": "ما اسم الشخصية في النص؟",
                        "en": "What is the character's name in the text?",
                        "tr": "Metindeki kişinin adı nedir?",
                    },
                    "options": ["محمد", "أحمد", "علي"],
                    "correct_index": 1,
                },
                {
                    "type": "multiple_choice",
                    "key": "r2",
                    "question": {
                        "ar": "من أين أحمد؟",
                        "en": "Where is Ahmad from?",
                        "tr": "Ahmed nereli?",
                    },
                    "options": [
                        {"ar": "من مصر", "en": "From Egypt", "tr": "Mısır'dan"},
                        {"ar": "من سوريا", "en": "From Syria", "tr": "Suriye'den"},
                        {"ar": "من الأردن", "en": "From Jordan", "tr": "Ürdün'den"},
                    ],
                    "correct_index": 2,
                },
                {
                    "type": "multiple_choice",
                    "key": "r3",
                    "question": {
                        "ar": "ما هي مهنة أحمد؟",
                        "en": "What is Ahmad's occupation?",
                        "tr": "Ahmed'in mesleği nedir?",
                    },
                    "options": [
                        {"ar": "طالب", "en": "Student", "tr": "Öğrenci"},
                        {"ar": "معلم", "en": "Teacher", "tr": "Öğretmen"},
                        {"ar": "طبيب", "en": "Doctor", "tr": "Doktor"},
                    ],
                    "correct_index": 0,
                },
            ],
        },

        # ---------------------------------------------------------------
        # 5) الاستماع
        # ---------------------------------------------------------------
        {
            "skill": "listening",
            "delay_minutes": 1,
            "image": "https://drive.google.com/uc?export=download&id=1yPYbZJDrEQSeXIJgARLw8QhKCl7MUVBT",
            "audio": "https://drive.google.com/uc?export=download&id=1jUB5ZjvDMhRD-8m9y6Z0PVaWNgpF_Hgp",
            "exercises": [
                {
                    "type": "multiple_choice",
                    "key": "l1",
                    "question": {
                        "ar": "من أين سارة؟",
                        "en": "Where is Sarah from?",
                        "tr": "Sarah nereli?",
                    },
                    "options": [
                        {"ar": "من ألمانيا", "en": "From Germany", "tr": "Almanya'dan"},
                        {"ar": "من تركيا", "en": "From Turkey", "tr": "Türkiye'den"},
                        {"ar": "من الإمارات", "en": "From the UAE", "tr": "BAE'den"},
                    ],
                    "correct_index": 0,
                },
                {
                    "type": "multiple_choice",
                    "key": "l2",
                    "question": {
                        "ar": "كم عمر سارة؟",
                        "en": "How old is Sarah?",
                        "tr": "Sarah kaç yaşında?",
                    },
                    "options": ["18", "20", "25"],
                    "correct_index": 1,
                },
                {
                    "type": "multiple_choice",
                    "key": "l3",
                    "question": {
                        "ar": "ماذا تتمنى سارة؟",
                        "en": "What does Sarah wish for?",
                        "tr": "Sarah'nın dileği nedir?",
                    },
                    "options": [
                        {"ar": "أن تسافر", "en": "To travel", "tr": "Seyahat etmek"},
                        {"ar": "أن تتحدث العربية بطلاقة", "en": "To speak Arabic fluently", "tr": "Arapçayı akıcı konuşmak"},
                        {"ar": "أن تتعلم الإنجليزية", "en": "To learn English", "tr": "İngilizce öğrenmek"},
                    ],
                    "correct_index": 1,
                },
            ],
        },

        # ---------------------------------------------------------------
        # 6) المحادثة (تصحيح AI)
        # ---------------------------------------------------------------
        {
            "skill": "speaking",
            "delay_minutes": 1,
            "questions": [
                {"ar": "ما اسمك؟", "en": "What is your name?", "tr": "Adın ne?"},
                {"ar": "من أين أنت؟", "en": "Where are you from?", "tr": "Nerelisin?"},
                {"ar": "كم عمرك؟", "en": "How old are you?", "tr": "Kaç yaşındasın?"},
            ],
        },

        # ---------------------------------------------------------------
        # 7) الكتابة (تصحيح AI)
        # ---------------------------------------------------------------
        {
            "skill": "writing",
            "delay_minutes": 1,
            "questions": [
                {
                    "ar": "اكتب فقرة قصيرة من 3 إلى 5 جمل تُقدّم فيها نفسك: اذكر اسمك، ومن أين أنت، وعمرك.",
                    "en": "Write a short paragraph of 3-5 sentences introducing yourself: mention your name, where you're from, and your age.",
                    "tr": "Kendinizi tanıtan 3-5 cümlelik kısa bir paragraf yazın: adınızı, nereli olduğunuzu ve yaşınızı belirtin.",
                },
            ],
        },
    ],
}
