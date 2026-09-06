import google.generativeai as genai
from typing import List, Optional
import random
from config import Config

class AITutor:
    def __init__(self):
        self.api_keys = Config.GEMINI_API_KEYS
        self.current_key_index = 0
        self._init_model()
    
    def _init_model(self):
        """تهيئة نموذج Gemini مع مفتاح API الحالي"""
        try:
            genai.configure(api_key=self.api_keys[self.current_key_index])
            self.model = genai.GenerativeModel('gemini-pro')
        except Exception as e:
            print(f"Error initializing Gemini: {e}")
            self._switch_key()
    
    def _switch_key(self):
        """التبديل إلى مفتاح API التالي"""
        self.current_key_index = (self.current_key_index + 1) % len(self.api_keys)
        try:
            genai.configure(api_key=self.api_keys[self.current_key_index])
            self.model = genai.GenerativeModel('gemini-pro')
        except Exception as e:
            print(f"Error switching Gemini key: {e}")
    
    def correct_text(self, text: str, language: str = 'ar') -> str:
        """تصحيح النص باستخدام الذكاء الاصطناعي"""
        try:
            prompt = f"""
            قم بتصحيح النص التالي باللغة العربية:
            النص: {text}
            
            قم بتصحيح الأخطاء الإملائية والنحوية وأعد كتابة النص بشكل صحيح.
            إذا كان النص صحيحاً، أخبر المستخدم بأن النص صحيح.
            """
            
            response = self.model.generate_content(prompt)
            return response.text
        except Exception as e:
            print(f"Error in AI correction: {e}")
            self._switch_key()
            return "⚠️ حدث خطأ في التصحيح. يرجى المحاولة مرة أخرى."
    
    def generate_conversation(self, level: str, topic: str = None, language: str = 'ar') -> str:
        """توليد محادثة تدريبية"""
        try:
            topics = {
                'ar': {
                    'A0': ['التحية', 'الحروف', 'الأرقام', 'الألوان'],
                    'A1': ['العائلة', 'الطعام', 'المنزل', 'المدرسة'],
                    'A2': ['السفر', 'الصحة', 'التسوق', 'الطقس'],
                    'B1': ['العمل', 'الثقافة', 'السياسة', 'البيئة'],
                    'B2': ['التكنولوجيا', 'الفن', 'الأدب', 'العلوم']
                }
            }
            
            if not topic and level in topics.get(language, {}):
                topic = random.choice(topics[language][level])
            
            prompt = f"""
            قم بإنشاء محادثة تدريبية باللغة العربية لمتعلم في المستوى {level}.
            الموضوع: {topic if topic else 'موضوع عام'}
            
            يجب أن تكون المحادثة:
            1. واقعية وطبيعية
            2. مناسبة للمستوى المحدد
            3. تحتوي على عبارات مفيدة
            4. مع ترجمة إنجليزية بسيطة بين قوسين للكلمات الصعبة
            
            قدم المحادثة على شكل حوار بين شخصين.
            """
            
            response = self.model.generate_content(prompt)
            return response.text
        except Exception as e:
            print(f"Error in conversation generation: {e}")
            self._switch_key()
            return "⚠️ حدث خطأ في توليد المحادثة. يرجى المحاولة مرة أخرى."
    
    def generate_writing_prompt(self, level: str, language: str = 'ar') -> str:
        """توليد موضوع كتابة للممارسة"""
        try:
            prompts = {
                'ar': {
                    'A0': ['اكتب عن عائلتك', 'صف منزلك', 'اكتب عن يومك'],
                    'A1': ['اكتب عن هواياتك', 'صف طعامك المفضل', 'اكتب عن مدرستك'],
                    'A2': ['اكتب عن رحلة قمت بها', 'صف مهنتك المفضلة', 'اكتب عن عطلة نهاية الأسبوع'],
                    'B1': ['اكتب عن تجربة تعلم اللغة', 'ناقش مشكلة اجتماعية', 'اكتب عن فيلم أعجبك'],
                    'B2': ['اكتب مقالاً عن التكنولوجيا', 'ناقش قضية بيئية', 'اكتب تحليلاً لموضوع ثقافي']
                }
            }
            
            if level in prompts.get(language, {}):
                return random.choice(prompts[language][level])
            return "اكتب موضوعاً من اختيارك"
        except Exception as e:
            print(f"Error in writing prompt: {e}")
            return "اكتب موضوعاً من اختيارك"
    
    def evaluate_writing(self, text: str, level: str, language: str = 'ar') -> str:
        """تقييم النص الكتابي"""
        try:
            prompt = f"""
            قم بتقييم النص التالي باللغة العربية لمتعلم في المستوى {level}.
            النص: {text}
            
            قم بتقييم:
            1. القواعد النحوية
            2. المفردات المستخدمة
            3. التنظيم والترتيب
            4. الإبداع والأصالة
            
            قدم تقييماً مفصلاً مع ملاحظات تحفيزية ونصائح للتحسين.
            """
            
            response = self.model.generate_content(prompt)
            return response.text
        except Exception as e:
            print(f"Error in writing evaluation: {e}")
            self._switch_key()
            return "⚠️ حدث خطأ في التقييم. يرجى المحاولة مرة أخرى."

# إنشاء كائن المعلم الذكي
ai_tutor = AITutor()
