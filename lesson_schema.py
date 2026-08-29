# -*- coding: utf-8 -*-
"""
lesson_schema.py
مرجع توثيقي فقط (لا يُستورد أو يُنفَّذ) يوضّح الشكل الذي يجب أن يتبعه كل ملف
lessonN.py حتى يعمل مع lesson_engine.py تلقائيًا.

كل ملف درس يجب أن يحتوي على متغيّر LESSON بهذا الشكل تمامًا:

LESSON = {
    "id": 1,
    "title": {"ar": "الدرس الأول: التعريف بالنفس", "en": "Lesson 1: Introductions", "tr": "1. Ders: Tanışma"},
    "steps": [
        {
            "skill": "intro",                # intro | vocab | grammar | reading | listening | speaking | writing
            "delay_minutes": 1,                # الدقائق قبل إرسال هذه الخطوة (تُقرأ من الخطوة *التالية* عمليًا)
            "text": {"ar": "...", "en": "...", "tr": "..."},
            "motivational_question": {"ar": "...", "en": "...", "tr": "..."},
            "image": "https://drive.google.com/uc?export=download&id=XXXX",  # رابط مباشر أو Telegram file_id
        },
        {
            "skill": "vocab",
            "delay_minutes": 1,
            "image": None,
            "vocab_table": [
                {"ar": "اسم", "transliteration": "ism", "meaning": {"en": "name", "tr": "isim"}},
            ],
            "exercises": [
                {
                    "type": "multiple_choice",
                    "key": "v1",                       # معرّف فريد للسؤال داخل هذه المهارة (لتتبّع الإجابات)
                    "question": {"ar": "...", "en": "...", "tr": "..."},
                    "options": ["name", "book", "car"],  # تُعرض كما هي (لا تُترجم تلقائيًا؛ اكتبها بلغة الطالب مسبقًا إن أردت تعدد اللغات، أو أنشئ options لكل لغة بمنطق مخصص)
                    "correct_index": 0,
                    "explanation": {"ar": "...", "en": "...", "tr": "..."},  # اختياري: يظهر بعد الإجابة الصحيحة
                }
            ],
        },
        {
            "skill": "grammar",
            "delay_minutes": 1,
            "explanation": {"ar": "...", "en": "...", "tr": "..."},
            "examples": ["هذا بيتٌ.", "هذا كتابٌ."],
            "exercises": [ ... ],  # نفس شكل exercises أعلاه
        },
        {
            "skill": "reading",
            "delay_minutes": 1,
            "reading_text": "نص عربي فقط، لا يُترجم أبدًا",
            "image": None,
            "audio": "https://... أو Telegram file_id",
            "exercises": [ ... ],
        },
        {
            "skill": "listening",
            "delay_minutes": 1,
            "image": None,
            "audio": "https://... أو Telegram file_id",
            "exercises": [ ... ],
        },
        {
            "skill": "speaking",
            "delay_minutes": 1,
            "questions": [{"ar": "عرّف عن نفسك.", "en": "Introduce yourself.", "tr": "Kendinizi tanıtın."}],
            # لا exercises هنا؛ تُصحَّح عبر AI عند وصول رد الطالب (نص أو صوت)
        },
        {
            "skill": "writing",
            "delay_minutes": 1,
            "questions": [{"ar": "اكتب جملتين عن نفسك.", "en": "Write two sentences about yourself.", "tr": "..."}],
        },
    ],
}

قواعد مهمة:
- "options" و"exercises" الخاصة بالاختيار من متعدد تُعرض للطالب كنص عبر أزرار Inline
  (لا يكتب الطالب حرفًا، فقط يضغط زر).
- reading_text يبقى بالعربية دائمًا. التوجيهات والشروحات فقط تُترجم حسب لغة الطالب.
- كل "key" داخل exercises لمهارة واحدة يجب أن يكون فريدًا ضمن تلك المهارة (يُستخدم لتتبع
  إجابة كل سؤال على حدة في قاعدة البيانات وجدول answers).
- لا تحتوي مهارتا speaking وwriting على exercises آلية؛ يُنتظر رد الطالب (نص/صوت) ويُصحَّح
  عبر services/ai_service.py، وعندها فقط تُعتبر المهارة مكتملة.
- الدرس بالكامل لا يُعتبر "مكتملًا" (لا يُسجَّل في completions ولا يُعلَن في القروب) إلا
  بعد اكتمال جميع مهاراته المذكورة في steps فعليًا — هذا يُدار تلقائيًا في lesson_engine.py.
"""
