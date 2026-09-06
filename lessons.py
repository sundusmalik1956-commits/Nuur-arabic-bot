import json
import os
from typing import Dict, List, Optional

class LessonsManager:
    def __init__(self, lessons_dir='lessons_data'):
        self.lessons_dir = lessons_dir
        self._ensure_directory()
    
    def _ensure_directory(self):
        if not os.path.exists(self.lessons_dir):
            os.makedirs(self.lessons_dir)
    
    def get_level_lessons(self, level: str) -> List[Dict]:
        """الحصول على دروس المستوى المحدد"""
        file_path = os.path.join(self.lessons_dir, f'level_{level}.json')
        if os.path.exists(file_path):
            with open(file_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        return self._create_default_lessons(level)
    
    def _create_default_lessons(self, level: str) -> List[Dict]:
        """إنشاء دروس افتراضية للمستوى"""
        num_lessons = 4 if level == 'A0' else 18
        lessons = []
        for i in range(1, num_lessons + 1):
            lesson = {
                'id': i,
                'title': f'الدرس {i}',
                'title_en': f'Lesson {i}',
                'description': f'محتوى الدرس {i}',
                'description_en': f'Lesson {i} content',
                'video_url': '',
                'audio_url': '',
                'image_url': '',
                'text_content': f'نص الدرس {i}',
                'vocabulary': [],
                'exercises': [],
                'is_free': i <= 5
            }
            lessons.append(lesson)
        
        # حفظ الدروس الافتراضية
        file_path = os.path.join(self.lessons_dir, f'level_{level}.json')
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(lessons, f, ensure_ascii=False, indent=2)
        
        return lessons
    
    def get_lesson(self, level: str, lesson_id: int) -> Optional[Dict]:
        lessons = self.get_level_lessons(level)
        for lesson in lessons:
            if lesson['id'] == lesson_id:
                return lesson
        return None
    
    def update_lesson(self, level: str, lesson_id: int, data: Dict):
        lessons = self.get_level_lessons(level)
        for i, lesson in enumerate(lessons):
            if lesson['id'] == lesson_id:
                lessons[i].update(data)
                break
        file_path = os.path.join(self.lessons_dir, f'level_{level}.json')
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(lessons, f, ensure_ascii=False, indent=2)
    
    def get_next_lesson(self, level: str, current_lesson: int) -> Optional[Dict]:
        lessons = self.get_level_lessons(level)
        for lesson in lessons:
            if lesson['id'] > current_lesson:
                return lesson
        return None
    
    def get_lesson_content_for_telegram(self, lesson: Dict, language: str = 'ar') -> str:
        """تنسيق محتوى الدرس لإرساله عبر تيليجرام"""
        if language == 'ar':
            title = lesson.get('title', '')
            description = lesson.get('description', '')
            content = lesson.get('text_content', '')
        elif language == 'en':
            title = lesson.get('title_en', lesson.get('title', ''))
            description = lesson.get('description_en', lesson.get('description', ''))
            content = lesson.get('text_content', '')
        else:
            # استخدام العربية كافتراضية
            title = lesson.get('title', '')
            description = lesson.get('description', '')
            content = lesson.get('text_content', '')
        
        message = f"📚 **{title}**\n\n"
        message += f"{description}\n\n"
        message += f"━━━━━━━━━━━━━━━━━━━\n\n"
        message += content
        
        return message

# إنشاء مدير الدروس
lessons_manager = LessonsManager()

# دالة مساعدة لإدارة الدروس من Google Drive
def get_drive_file_embed(drive_url: str) -> str:
    """تحويل رابط Google Drive إلى رابط مضمّن"""
    if not drive_url:
        return ''
    # استخراج معرف الملف من رابط Google Drive
    import re
    patterns = [
        r'/file/d/([^/]+)',
        r'id=([^&]+)',
        r'drive\.google\.com/open\?id=([^&]+)'
    ]
    file_id = None
    for pattern in patterns:
        match = re.search(pattern, drive_url)
        if match:
            file_id = match.group(1)
            break
    
    if file_id:
        return f"https://drive.google.com/uc?export=view&id={file_id}"
    return drive_url
