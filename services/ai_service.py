# -*- coding: utf-8 -*-
"""
services/ai_service.py
الواجهة العامة للذكاء الاصطناعي. الدروس والبوت يستدعون هذا الملف فقط،
وليس Gemini مباشرة — هذا يسمح بتغيير المزوّد (Gemini/OpenAI/آخر) مستقبلًا
بتعديل services/gemini_provider.py فقط دون لمس أي درس.

مسار الاستدعاء:
    bot.py -> lessonN.py -> services/ai_service.py -> services/gemini_provider.py
"""

import logging
from dataclasses import dataclass
from . import gemini_provider

logger = logging.getLogger(__name__)


@dataclass
class AICorrectionResult:
    is_correct: bool
    corrected_text: str
    explanation: str
    raw_response: str = ""


def correct_writing(student_text: str, prompt_context: str, student_lang: str = "ar") -> AICorrectionResult | None:
    """تصحيح فقرة كتابة. يُعيد None إذا فشل الاتصال بالذكاء الاصطناعي (يُعامَل بلطف من قِبل الطالب)."""
    try:
        return gemini_provider.correct_writing(student_text, prompt_context, student_lang)
    except Exception:
        logger.exception("فشلت طبقة AI في تصحيح الكتابة")
        return None


def correct_speaking_text(student_text: str, prompt_context: str, student_lang: str = "ar") -> AICorrectionResult | None:
    """تصحيح إجابة محادثة مُحوَّلة إلى نص (أو مُرسَلة كنص أصلاً)."""
    try:
        return gemini_provider.correct_speaking_text(student_text, prompt_context, student_lang)
    except Exception:
        logger.exception("فشلت طبقة AI في تصحيح المحادثة النصية")
        return None


def correct_speaking_audio(audio_bytes: bytes, prompt_context: str, student_lang: str = "ar") -> AICorrectionResult | None:
    """تصحيح تسجيل صوتي مباشرة (متعدد الوسائط)."""
    try:
        return gemini_provider.correct_speaking_audio(audio_bytes, prompt_context, student_lang)
    except Exception:
        logger.exception("فشلت طبقة AI في تصحيح المحادثة الصوتية")
        return None
