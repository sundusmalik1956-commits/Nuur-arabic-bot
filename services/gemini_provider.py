# -*- coding: utf-8 -*-
"""
services/gemini_provider.py
التفاصيل التقنية الفعلية للاتصال بـ Google Gemini وتصحيح النصوص والأصوات.
"""

import os
import re
import json
import logging
from google import genai
from google.genai import types

logger = logging.getLogger(__name__)

GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")
MODEL_NAME = "gemini-3.6-flash"

_client = None

def _get_client():
    global _client
    if _client is None:
        if not GEMINI_API_KEY:
            raise RuntimeError("GEMINI_API_KEY غير معرَّف في متغيرات البيئة.")
        _client = genai.Client(api_key=GEMINI_API_KEY)
    return _client

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
    cleaned = re.sub(r"^```json|```$", "", raw_text.strip(), flags=re.MULTILINE).strip()
    return json.loads(cleaned)

def correct_writing(student_text: str, prompt_context: str, student_lang: str = "ar"):
    from .ai_service import AICorrectionResult

    client = _get_client()
    prompt = _build_prompt(student_text, prompt_context, student_lang)
    response = client.models.generate_content(model=MODEL_NAME, contents=prompt)
    data = _parse_json_response(response.text)
    return AICorrectionResult(
        is_correct=bool(data.get("is_correct")),
        corrected_text=data.get("corrected_text", student_text),
        explanation=data.get("explanation", ""),
        raw_response=response.text,
    )

def correct_speaking_text(student_text: str, prompt_context: str, student_lang: str = "ar"):
    return correct_writing(student_text, prompt_context, student_lang)

def correct_speaking_audio(audio_bytes: bytes, prompt_context: str, student_lang: str = "ar"):
    from .ai_service import AICorrectionResult

    client = _get_client()
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
    try:
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
    except Exception as e:
        logger.exception(f"فشلت معالجة وتصحيح الملف الصوتي عبر Gemini: {e}")
        return None
