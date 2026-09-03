# -*- coding: utf-8 -*-
"""
services/gemini_provider.py
التفاصيل التقنية للاتصال بـ Google Gemini مع تدوير وتجربة المفاتيح المتعددة تلقائياً لتجاوز الضغط.
"""

import os
import re
import json
import logging
import random
from google import genai
from google.genai import types

logger = logging.getLogger(__name__)

# قراءة المفاتيح المتعددة من متغير البيئة GEMINI_API_KEYS (مفصولة بفاصلة) أو المفتاح الفردي
_keys_env = os.environ.get("GEMINI_API_KEYS", "") or os.environ.get("GEMINI_API_KEY", "")
API_KEYS = [k.strip() for k in _keys_env.split(",") if k.strip()]

MODEL_NAME = "gemini-3.6-flash"

def _call_gemini_with_rotation(func, *args, **kwargs):
    """
    دالة ذكية لتجربة الطلب باستخدام المفاتيح المتاحة تباعاً.
    إذا فشل المفتاح الأول (بسبب ضغط 503 أو غيره)، تنتقل تلقائياً للمفتاح التالي حتى ينجح الطلب.
    """
    if not API_KEYS:
        raise RuntimeError("لا توجد مفاتيح Gemini معرَّفة في متغيرات البيئة (GEMINI_API_KEYS).")

    # نسخ القائمة وخلطها عشوائياً لتبدأ من مفتاح مختلف لكل طلب تلافياً للضغط
    keys_to_try = list(API_KEYS)
    random.shuffle(keys_to_try)

    last_error = None
    for idx, key in enumerate(keys_to_try):
        try:
            client = genai.Client(api_key=key)
            return func(client, *args, **kwargs)
        except Exception as e:
            last_error = e
            logger.warning(f"فشل استخدام أحد مفاتيح Gemini (المحاولة {idx + 1}/{len(keys_to_try)}): {e}")
            continue

    # إذا فشلت كل المفاتيح
    raise last_error

LANG_NAMES = {"ar": "Arabic", "en": "English", "tr": "Turkish"}

def _build_prompt(student_text: str, prompt_context: str, student_lang: str) -> str:
    lang_name = LANG_NAMES.get(student_lang, "Arabic")
    return f"""You are a friendly, encouraging Arabic teacher correcting a beginner
foreign student's answer. Respond ONLY with valid JSON, no markdown fences, no preamble.

Question/context given to the student: {prompt_context}
Student's answer (in Arabic): {student_text}

Return JSON with exactly these keys:
{{
  "is_correct": true or false (true if the sentence is grammatically correct and answers the question reasonably),
  "corrected_text": "the corrected Arabic sentence (or the original if already correct)",
  "explanation": "a short, encouraging explanation of the main issue (or a short praise if correct), written in {lang_name}"
}}
"""

def _parse_json_response(raw_text: str) -> dict:
    if not raw_text:
        raise ValueError("استجابة الذكاء الاصطناعي فارغة.")
    
    text = raw_text.strip()
    text = re.sub(r"^```(?:json)?\s*", "", text, flags=re.IGNORECASE)
    text = re.sub(r"\s*```$", "", text)
    text = text.strip()
    
    match = re.search(r"\{.*\}", text, re.DOTALL)
    if match:
        text = match.group(0)
        
    return json.loads(text)

def correct_writing(student_text: str, prompt_context: str, student_lang: str = "ar"):
    from .ai_service import AICorrectionResult

    def _task(client):
        prompt = _build_prompt(student_text, prompt_context, student_lang)
        response = client.models.generate_content(model=MODEL_NAME, contents=prompt)
        data = _parse_json_response(response.text)
        return AICorrectionResult(
            is_correct=bool(data.get("is_correct")),
            corrected_text=data.get("corrected_text", student_text),
            explanation=data.get("explanation", ""),
            raw_response=response.text,
        )

    try:
        return _call_gemini_with_rotation(_task)
    except Exception:
        logger.exception("فشلت معالجة وتصحيح الكتابة بعد تجربة كافة المفاتيح المتاحة.")
        return None

def correct_speaking_text(student_text: str, prompt_context: str, student_lang: str = "ar"):
    return correct_writing(student_text, prompt_context, student_lang)

def correct_speaking_audio(audio_bytes: bytes, prompt_context: str, student_lang: str = "ar"):
    from .ai_service import AICorrectionResult

    lang_name = LANG_NAMES.get(student_lang, "Arabic")
    prompt = f"""Listen to this audio recording — a beginner foreign student's spoken
answer in Arabic to the following question: {prompt_context}

Respond ONLY with valid JSON, no markdown fences:
{{
  "is_correct": true or false,
  "corrected_text": "what the student should have said, in Arabic",
  "explanation": "short encouraging feedback on pronunciation/grammar, in {lang_name}"
}}
"""
    def _task(client):
        audio_part = types.Part.from_bytes(
            data=audio_bytes,
            mime_type="audio/ogg",
        )
        response = client.models.generate_content(
            model=MODEL_NAME,
            contents=[audio_part, prompt],
        )
        data = _parse_json_response(response.text)
        return AICorrectionResult(
            is_correct=bool(data.get("is_correct")),
            corrected_text=data.get("corrected_text", ""),
            explanation=data.get("explanation", ""),
            raw_response=response.text,
        )

    try:
        return _call_gemini_with_rotation(_task)
    except Exception as e:
        logger.exception(f"فشلت معالجة وتصحيح الملف الصوتي بعد تجربة كافة المفاتيح: {e}")
        return None
