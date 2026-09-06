import pandas as pd
from datetime import datetime
import io
from database import Database

class ExcelExporter:
    def __init__(self):
        self.db = Database()
    
    def export_users_to_excel(self) -> bytes:
        """تصدير بيانات المستخدمين إلى ملف Excel"""
        users = self.db.get_all_users()
        
        if not users:
            # إنشاء DataFrame فارغ
            df = pd.DataFrame(columns=['user_id', 'username', 'first_name', 'last_name', 
                                      'language', 'level', 'gender', 'lesson_time', 
                                      'days_off', 'current_lesson', 'is_subscribed', 
                                      'created_at', 'updated_at'])
        else:
            df = pd.DataFrame(users)
        
        # معالجة أيام الإجازة لتكون نصاً
        if 'days_off' in df.columns:
            df['days_off'] = df['days_off'].apply(lambda x: ', '.join(x) if isinstance(x, list) else x)
        
        # تحويل التواريخ إلى نص
        for col in ['created_at', 'updated_at']:
            if col in df.columns:
                df[col] = df[col].apply(lambda x: str(x) if x else '')
        
        # إنشاء ملف Excel في الذاكرة
        output = io.BytesIO()
        with pd.ExcelWriter(output, engine='openpyxl') as writer:
            df.to_excel(writer, sheet_name='Students', index=False)
            
            # تنسيق الأعمدة
            workbook = writer.book
            worksheet = writer.sheets['Students']
            
            # ضبط عرض الأعمدة
            for column in worksheet.columns:
                max_length = 0
                column_letter = column[0].column_letter
                for cell in column:
                    try:
                        if len(str(cell.value)) > max_length:
                            max_length = len(str(cell.value))
                    except:
                        pass
                adjusted_length = min(max_length + 2, 50)
                worksheet.column_dimensions[column_letter].width = adjusted_length
        
        output.seek(0)
        return output.getvalue()
    
    def get_user_stats(self) -> Dict:
        """الحصول على إحصائيات المستخدمين"""
        users = self.db.get_all_users()
        
        stats = {
            'total_users': len(users),
            'subscribed_users': sum(1 for u in users if u.get('is_subscribed', False)),
            'free_users': sum(1 for u in users if not u.get('is_subscribed', False)),
            'levels': {},
            'languages': {},
            'genders': {}
        }
        
        for user in users:
            level = user.get('level', 'Unknown')
            stats['levels'][level] = stats['levels'].get(level, 0) + 1
            
            lang = user.get('language', 'Unknown')
            stats['languages'][lang] = stats['languages'].get(lang, 0) + 1
            
            gender = user.get('gender', 'Unknown')
            stats['genders'][gender] = stats['genders'].get(gender, 0) + 1
        
        return stats

# إنشاء كائن المصدر
excel_exporter = ExcelExporter()
