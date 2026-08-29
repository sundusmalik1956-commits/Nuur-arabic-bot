# gemini_service.py
import os
import logging
from typing import Optional, Dict, Any

import google.generativeai as genai

logger = logging.getLogger(__name__)

class GeminiService:
    """خدمة الذكاء الاصطناعي باستخدام Gemini"""
    
    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key or os.getenv('GEMINI_API_KEY')
        self.model = None
        self.initialized = False
        
        if self.api_key:
            try:
                genai.configure(api_key=self.api_key)
                self.model = genai.GenerativeModel('gemini-1.5-flash')
                self.initialized = True
                logger.info("تم تهيئة Gemini بنجاح")
            except Exception as e:
                logger.error(f"خطأ في تهيئة Gemini: {e}")
        else:
            logger.warning("GEMINI_API_KEY غير موجود")
    
    async def correct_writing(self, text: str, lang: str = 'ar') -> str:
        """تصحيح النص الكتابي"""
        if not self.initialized:
            return self._fallback_response(text, lang)
        
        try:
            prompt = self._get_writing_prompt(text, lang)
            response = self.model.generate_content(prompt)
            return response.text
        except Exception as e:
            logger.error(f"خطأ في تصحيح الكتابة: {e}")
            return self._fallback_response(text, lang)
    
    async def evaluate_conversation(self, user_message: str, lang: str = 'ar') -> str:
        """تقييم المحادثة"""
        if not self.initialized:
            return self._fallback_conversation_response(user_message, lang)
        
        try:
            prompt = self._get_conversation_prompt(user_message, lang)
            response = self.model.generate_content(prompt)
            return response.text
        except Exception as e:
            logger.error(f"خطأ في تقييم المحادثة: {e}")
            return self._fallback_conversation_response(user_message, lang)
    
    def _get_writing_prompt(self, text: str, lang: str) -> str:
        """الحصول على prompt لتصحيح الكتابة"""
        prompts = {
            'ar': f"""قم بتحليل وتصحيح النص العربي التالي:

النص: "{text}"

قم بتقديم:
1. التصحيح (مع إظهار الأخطاء)
2. شرح الأخطاء
3. اقتراح صياغة أفضل
4. تقييم تقريبي (من 10)

كن واضحاً ومفصلاً في الشرح.""",
            
            'en': f"""Analyze and correct the following Arabic text:

Text: "{text}"

Provide:
1. Correction (showing errors)
2. Error explanations
3. Better formulation suggestions
4. Approximate score (out of 10)

Be clear and detailed in your explanation.""",
            
            'tr': f"""Aşağıdaki Arapça metni analiz edin ve düzeltin:

Metin: "{text}"

Şunları sağlayın:
1. Düzeltme (hataları göstererek)
2. Hata açıklamaları
3. Daha iyi ifade önerileri
4. Yaklaşık puan (10 üzerinden)

Açıklamanızda açık ve ayrıntılı olun."""
        }
        
        return prompts.get(lang, prompts['ar'])
    
    def _get_conversation_prompt(self, message: str, lang: str) -> str:
        """الحصول على prompt لتقييم المحادثة"""
        prompts = {
            'ar': f"""قم بتقييم الجملة العربية التالية من حيث:

الجملة: "{message}"

قم بتقييم:
1. صحة الجملة (نحوية وإملائية)
2. وضوح المعنى
3. المفردات المستخدمة
4. مستوى الطالب

قدم تقييماً مفيداً مع نصائح للتحسين.""",
            
            'en': f"""Evaluate the following Arabic sentence:

Sentence: "{message}"

Evaluate:
1. Grammar and spelling
2. Clarity of meaning
3. Vocabulary used
4. Student's level

Provide useful feedback with improvement tips.""",
            
            'tr': f"""Aşağıdaki Arapça cümleyi değerlendirin:

Cümle: "{message}"

Değerlendirin:
1. Dilbilgisi ve yazım
2. Anlam açıklığı
3. Kullanılan kelimeler
4. Öğrencinin seviyesi

İyileştirme ipuçları ile faydalı geri bildirim sağlayın."""
        }
        
        return prompts.get(lang, prompts['ar'])
    
    def _fallback_response(self, text: str, lang: str) -> str:
        """استجابة احتياطية في حالة فشل Gemini"""
        responses = {
            'ar': f"""📝 تقييم كتابتك:

نصك: "{text}"

🌟 أحسنت على المحاولة! استمر في التدريب على الكتابة العربية.

نصائح:
• حاول استخدام جمل بسيطة في البداية
• راجع المفردات التي تعلمتها
• انتبه إلى علامات الترقيم""",
            
            'en': f"""📝 Evaluation of your writing:

Your text: "{text}"

🌟 Good effort! Keep practicing Arabic writing.

Tips:
• Start with simple sentences
• Review the vocabulary you learned
• Pay attention to punctuation""",
            
            'tr': f"""📝 Yazınızın değerlendirmesi:

Metniniz: "{text}"

🌟 İyi deneme! Arapça yazma pratiğine devam edin.

İpuçları:
• Başlangıçta basit cümleler kullanın
• Öğrendiğiniz kelimeleri gözden geçirin
• Noktalama işaretlerine dikkat edin"""
        }
        
        return responses.get(lang, responses['ar'])
    
    def _fallback_conversation_response(self, message: str, lang: str) -> str:
        """استجابة احتياطية للمحادثة"""
        responses = {
            'ar': f"""💬 تقييم المحادثة:

جملتك: "{message}"

🌟 جيد جداً! استمر في التحدث بالعربية.

تلميح: حاول استخدام مفردات جديدة في كل مرة.""",
            
            'en': f"""💬 Conversation Evaluation:

Your sentence: "{message}"

🌟 Very good! Keep speaking Arabic.

Tip: Try to use new vocabulary each time.""",
            
            'tr': f"""💬 Konuşma Değerlendirmesi:

Cümleniz: "{message}"

🌟 Çok iyi! Arapça konuşmaya devam edin.

İpucu: Her seferinde yeni kelimeler kullanmaya çalışın."""
        }
        
        return responses.get(lang, responses['ar'])
    
    async def generate_quiz_question(self, skill: str, level: int, lang: str = 'ar') -> Dict[str, Any]:
        """توليد سؤال اختبار جديد"""
        if not self.initialized:
            return None
        
        try:
            prompt = self._get_quiz_prompt(skill, level, lang)
            response = self.model.generate_content(prompt)
            
            # محاولة تحويل الاستجابة إلى JSON
            import json
            try:
                return json.loads(response.text)
            except:
                return None
        except Exception as e:
            logger.error(f"خطأ في توليد سؤال: {e}")
            return None
    
    def _get_quiz_prompt(self, skill: str, level: int, lang: str) -> str:
        """الحصول على prompt لتوليد سؤال"""
        return f"""قم بإنشاء سؤال اختبار لتعليم اللغة العربية.

المهارة: {skill}
المستوى: {level} (1-5)

قم بإنشاء سؤال اختيار من متعدد مع 4 خيارات وإجابة صحيحة واحدة.

قم بإرجاع النتيجة بصيغة JSON:
{{
    "question": "السؤال بالعربية",
    "options": ["خيار 1", "خيار 2", "خيار 3", "خيار 4"],
    "correct": 0,
    "explanation": "شرح الإجابة"
}}

المحتوى يجب أن يكون مناسباً لمتعلمي اللغة العربية."""
