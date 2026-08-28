# =========================================================
# Noor Bot - Lesson 1
# الدرس الأول: التعريف بالنفس
# =========================================================

import os
import logging
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes

logger = logging.getLogger(__name__)


# =========================================================
# إعدادات الدرس
# =========================================================

LESSON_NUMBER = 1

LESSON_TITLE = {
    "ar": "📝 الدرس الأول: التعريف بالنفس",
    "en": "📝 Lesson 1: Introducing Yourself",
    "tr": "📝 Ders 1: Kendini Tanıtma",
}


# =========================================================
# الروابط
# =========================================================

MEDIA = {
    "intro_image":
        "https://drive.google.com/uc?export=download&id=1fDorqrKC-QvoElNesKW6T_Eb6ezHc10R",

    "vocabulary_image":
        "https://drive.google.com/uc?export=download&id=16ilPf6aByU4RsuVGYHwoSc-fGrt-KNep",

    "reading_image":
        "https://drive.google.com/uc?export=download&id=1B_dVPhx23mVpU9rX0v1op-aSdjxREevF",

    "reading_audio":
        "https://drive.google.com/uc?export=download&id=1iKsBknxnPN23W6YQn8k7n7B7DeiWKrZM",

    "listening_image":
        "https://drive.google.com/uc?export=download&id=1lZ22At0hJHFUdG6frxZh54TpiEyeOWb7",

    "listening_audio":
        "https://drive.google.com/uc?export=download&id=1xdl-V241ySJetMjdCmYY7qwuPLwot8Xs",
}


# =========================================================
# الأسئلة
# =========================================================

QUESTIONS = {

    # -----------------------------------------------------
    # Vocabulary
    # -----------------------------------------------------

    "vocabulary_q1": {
        "ar": {
            "question": 'ماذا تعني كلمة "اسمي" باللغة الإنجليزية؟',
            "options": [
                ("My name is", True),
                ("Your name", False),
                ("I am", False),
                ("From", False),
            ],
            "correct": "اسمي = My name is",
        },

        "en": {
            "question": 'What does "اسمي" mean in English?',
            "options": [
                ("My name is", True),
                ("Your name", False),
                ("I am", False),
                ("From", False),
            ],
            "correct": "اسمي = My name is",
        },

        "tr": {
            "question": '"اسمي" ne anlama gelir?',
            "options": [
                ("Benim adım", True),
                ("Senin adın", False),
                ("Ben", False),
                ("-den / -dan", False),
            ],
            "correct": "اسمي = Benim adım",
        },
    },


    "vocabulary_q2": {
        "ar": {
            "question": 'كيف تقول "I am from Saudi Arabia" بالعربية؟',
            "options": [
                ("أنا من السعودية", True),
                ("اسمي السعودية", False),
                ("أين السعودية", False),
                ("من أنا", False),
            ],
            "correct": "أنا من السعودية = I am from Saudi Arabia",
        },

        "en": {
            "question": 'How do you say "I am from Saudi Arabia" in Arabic?',
            "options": [
                ("أنا من السعودية", True),
                ("اسمي السعودية", False),
                ("أين السعودية", False),
                ("من أنا", False),
            ],
            "correct": "أنا من السعودية = I am from Saudi Arabia",
        },

        "tr": {
            "question": '"I am from Saudi Arabia" Arapça nasıl söylenir?',
            "options": [
                ("أنا من السعودية", True),
                ("اسمي السعودية", False),
                ("أين السعودية", False),
                ("من أنا", False),
            ],
            "correct": "أنا من السعودية = Suudi Arabistanlıyım.",
        },
    },


    "vocabulary_q3": {
        "ar": {
            "question": 'اختر الترجمة الصحيحة لكلمة "أين".',
            "options": [
                ("Where", True),
                ("What", False),
                ("Who", False),
                ("When", False),
            ],
            "correct": "أين = Where",
        },

        "en": {
            "question": 'Choose the correct translation of "أين".',
            "options": [
                ("Where", True),
                ("What", False),
                ("Who", False),
                ("When", False),
            ],
            "correct": "أين = Where",
        },

        "tr": {
            "question": '"أين" kelimesinin doğru anlamını seçin.',
            "options": [
                ("Nerede", True),
                ("Ne", False),
                ("Kim", False),
                ("Ne zaman", False),
            ],
            "correct": "أين = Nerede",
        },
    },


    # -----------------------------------------------------
    # Grammar
    # -----------------------------------------------------

    "grammar_q1": {
        "ar": {
            "question": 'اختر الجملة الصحيحة التي تعني "I am a student".',
            "options": [
                ("أنا طالب", True),
                ("اسمي طالب", False),
                ("أنا من طالب", False),
                ("عمري طالب", False),
            ],
            "correct":
                "أنا طالب = I am a student. "
                "وللمؤنث: أنا طالبة.",
        },

        "en": {
            "question": 'Choose the sentence that means "I am a student".',
            "options": [
                ("أنا طالب", True),
                ("اسمي طالب", False),
                ("أنا من طالب", False),
                ("عمري طالب", False),
            ],
            "correct":
                "أنا طالب = I am a student. "
                "For a female speaker: أنا طالبة.",
        },

        "tr": {
            "question": '"I am a student" anlamına gelen doğru cümleyi seçin.',
            "options": [
                ("أنا طالب", True),
                ("اسمي طالب", False),
                ("أنا من طالب", False),
                ("عمري طالب", False),
            ],
            "correct":
                "أنا طالب = Ben öğrenciyim. "
                "Kadın konuşmacı için: أنا طالبة.",
        },
    },


    "grammar_q2": {
        "ar": {
            "question": 'كيف تقول "My name is Sarah" بالعربية؟',
            "options": [
                ("اسمي سارة", True),
                ("أنا سارة", False),
                ("من سارة", False),
                ("عمري سارة", False),
            ],
            "correct": "اسمي سارة = My name is Sarah.",
        },

        "en": {
            "question": 'How do you say "My name is Sarah" in Arabic?',
            "options": [
                ("اسمي سارة", True),
                ("أنا سارة", False),
                ("من سارة", False),
                ("عمري سارة", False),
            ],
            "correct": "اسمي سارة = My name is Sarah.",
        },

        "tr": {
            "question": '"My name is Sarah" Arapça nasıl söylenir?',
            "options": [
                ("اسمي سارة", True),
                ("أنا سارة", False),
                ("من سارة", False),
                ("عمري سارة", False),
            ],
            "correct": "اسمي سارة = Benim adım Sarah.",
        },
    },


    "grammar_q3": {
        "ar": {
            "question": "أي من هذه الجمل غير صحيحة نحويًا؟",
            "options": [
                ("أنا من الأردن", False),
                ("اسمي خالد", False),
                ("أنا طالب هو", True),
                ("عمري 25 سنة", False),
            ],
            "correct":
                "أنا طالب هو جملة غير صحيحة؛ "
                'لأن الضمير "هو" لا حاجة له هنا.',
        },

        "en": {
            "question": "Which sentence is grammatically incorrect?",
            "options": [
                ("أنا من الأردن", False),
                ("اسمي خالد", False),
                ("أنا طالب هو", True),
                ("عمري 25 سنة", False),
            ],
            "correct":
                'أنا طالب هو is incorrect because the pronoun "هو" '
                "is unnecessary here.",
        },

        "tr": {
            "question": "Hangi cümle dilbilgisi açısından yanlıştır?",
            "options": [
                ("أنا من الأردن", False),
                ("اسمي خالد", False),
                ("أنا طالب هو", True),
                ("عمري 25 سنة", False),
            ],
            "correct":
                'أنا طالب هو yanlıştır; çünkü "هو" zamirine burada gerek yoktur.',
        },
    },


    # -----------------------------------------------------
    # Reading
    # -----------------------------------------------------

    "reading_q1": {
        "ar": {
            "question": "من أين هو أحمد؟",
            "options": [
                ("مصر", False),
                ("ألمانيا", True),
                ("الأردن", False),
                ("الإمارات", False),
            ],
            "correct": 'النص يقول: "أنا من ألمانيا".',
        },

        "en": {
            "question": "Where is Ahmed from?",
            "options": [
                ("Egypt", False),
                ("Germany", True),
                ("Jordan", False),
                ("UAE", False),
            ],
            "correct": 'The text says: "أنا من ألمانيا".',
        },

        "tr": {
            "question": "Ahmed nereli?",
            "options": [
                ("Mısır", False),
                ("Almanya", True),
                ("Ürdün", False),
                ("BAE", False),
            ],
            "correct": 'Metinde "أنا من ألمانيا" deniyor.',
        },
    },


    "reading_q2": {
        "ar": {
            "question": "كم عمر أحمد؟",
            "options": [
                ("20 سنة", False),
                ("25 سنة", True),
                ("30 سنة", False),
                ("35 سنة", False),
            ],
            "
