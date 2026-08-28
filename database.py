# database.py
import sqlite3
import json
from datetime import datetime
from typing import Optional, Dict, Any, List
import logging

logger = logging.getLogger(__name__)

class Database:
    """قاعدة البيانات الرئيسية للبوت"""
    
    def __init__(self, db_path: str = "noor_bot.db"):
        self.db_path = db_path
        self.init_db()
    
    def get_connection(self):
        """الحصول على اتصال بقاعدة البيانات"""
        return sqlite3.connect(self.db_path)
    
    def init_db(self):
        """تهيئة قاعدة البيانات وإنشاء الجداول"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            
            # جدول المستخدمين
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS users (
                    user_id INTEGER PRIMARY KEY,
                    username TEXT,
                    first_name TEXT,
                    last_name TEXT,
                    language TEXT DEFAULT 'ar',
                    lesson_time TEXT,
                    current_lesson INTEGER DEFAULT 1,
                    completed_lessons INTEGER DEFAULT 0,
                    completed_skills TEXT DEFAULT '{}',
                    subscription_status TEXT DEFAULT 'trial',
                    subscription_date TEXT,
                    certificate_status TEXT DEFAULT 'pending',
                    certificate_id TEXT,
                    certificate_date TEXT,
                    active INTEGER DEFAULT 1,
                    created_at TEXT DEFAULT CURRENT_TIMESTAMP,
                    updated_at TEXT DEFAULT CURRENT_TIMESTAMP
                )
            """)
            
            # جدول تقدم المهارات
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS skill_progress (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id INTEGER,
                    lesson_num INTEGER,
                    skill_name TEXT,
                    completed INTEGER DEFAULT 0,
                    attempts INTEGER DEFAULT 0,
                    last_attempt TEXT,
                    FOREIGN KEY (user_id) REFERENCES users(user_id),
                    UNIQUE(user_id, lesson_num, skill_name)
                )
            """)
            
            # جدول إجابات الطلاب
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS student_answers (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id INTEGER,
                    lesson_num INTEGER,
                    skill_name TEXT,
                    question_index INTEGER,
                    answer TEXT,
                    is_correct INTEGER,
                    attempts INTEGER DEFAULT 1,
                    answer_time TEXT DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (user_id) REFERENCES users(user_id)
                )
            """)
            
            # جدول المحادثات
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS conversations (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id INTEGER,
                    lesson_num INTEGER,
                    message TEXT,
                    response TEXT,
                    evaluation TEXT,
                    created_at TEXT DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (user_id) REFERENCES users(user_id)
                )
            """)
            
            # جدول الكتابات
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS writing_submissions (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id INTEGER,
                    lesson_num INTEGER,
                    text TEXT,
                    correction TEXT,
                    evaluation TEXT,
                    score REAL,
                    created_at TEXT DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (user_id) REFERENCES users(user_id)
                )
            """)
            
            conn.commit()
            logger.info("تم تهيئة قاعدة البيانات بنجاح")
    
    def add_user(self, user_id: int, username: str = None, first_name: str = None, language: str = 'ar'):
        """إضافة مستخدم جديد"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            
            # التحقق من وجود المستخدم
            cursor.execute("SELECT user_id FROM users WHERE user_id = ?", (user_id,))
            if cursor.fetchone():
                return self.update_user(user_id, {'language': language})
            
            cursor.execute("""
                INSERT INTO users (user_id, username, first_name, language, created_at, updated_at)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (user_id, username, first_name, language, datetime.now(), datetime.now()))
            conn.commit()
            logger.info(f"تم إضافة مستخدم جديد: {user_id}")
    
    def get_user(self, user_id: int) -> Optional[Dict[str, Any]]:
        """الحصول على بيانات المستخدم"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM users WHERE user_id = ?", (user_id,))
            row = cursor.fetchone()
            
            if row:
                columns = [description[0] for description in cursor.description]
                user = dict(zip(columns, row))
                
                # تحويل JSON إلى قاموس
                if user.get('completed_skills'):
                    try:
                        user['completed_skills'] = json.loads(user['completed_skills'])
                    except:
                        user['completed_skills'] = {}
                else:
                    user['completed_skills'] = {}
                
                return user
            return None
    
    def update_user(self, user_id: int, data: Dict[str, Any]) -> bool:
        """تحديث بيانات المستخدم"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            
            # معالجة البيانات الخاصة
            if 'completed_skills' in data and isinstance(data['completed_skills'], dict):
                data['completed_skills'] = json.dumps(data['completed_skills'])
            
            # بناء استعلام التحديث
            set_clause = ", ".join([f"{key} = ?" for key in data.keys()])
            values = list(data.values()) + [datetime.now(), user_id]
            
            query = f"UPDATE users SET {set_clause}, updated_at = ? WHERE user_id = ?"
            cursor.execute(query, values)
            conn.commit()
            
            return cursor.rowcount > 0
    
    def get_active_users(self) -> List[Dict[str, Any]]:
        """الحصول على المستخدمين النشطين"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT * FROM users 
                WHERE active = 1 AND lesson_time IS NOT NULL
            """)
            rows = cursor.fetchall()
            
            columns = [description[0] for description in cursor.description]
            users = []
            
            for row in rows:
                user = dict(zip(columns, row))
                if user.get('completed_skills'):
                    try:
                        user['completed_skills'] = json.loads(user['completed_skills'])
                    except:
                        user['completed_skills'] = {}
                else:
                    user['completed_skills'] = {}
                users.append(user)
            
            return users
    
    def save_skill_progress(self, user_id: int, lesson_num: int, skill_name: str, completed: bool = True):
        """حفظ تقدم المهارة"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            
            cursor.execute("""
                INSERT INTO skill_progress (user_id, lesson_num, skill_name, completed, last_attempt)
                VALUES (?, ?, ?, ?, ?)
                ON CONFLICT(user_id, lesson_num, skill_name) DO UPDATE SET
                completed = ?, last_attempt = ?, attempts = attempts + 1
            """, (user_id, lesson_num, skill_name, 1 if completed else 0, datetime.now(),
                  1 if completed else 0, datetime.now()))
            conn.commit()
    
    def save_answer(self, user_id: int, lesson_num: int, skill_name: str, 
                   question_index: int, answer: str, is_correct: bool):
        """حفظ إجابة الطالب"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            
            cursor.execute("""
                INSERT INTO student_answers 
                (user_id, lesson_num, skill_name, question_index, answer, is_correct, answer_time)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (user_id, lesson_num, skill_name, question_index, answer, 1 if is_correct else 0, datetime.now()))
            conn.commit()
    
    def save_conversation(self, user_id: int, lesson_num: int, message: str, 
                         response: str, evaluation: str = None):
        """حفظ المحادثة"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            
            cursor.execute("""
                INSERT INTO conversations (user_id, lesson_num, message, response, evaluation, created_at)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (user_id, lesson_num, message, response, evaluation, datetime.now()))
            conn.commit()
    
    def save_writing(self, user_id: int, lesson_num: int, text: str, 
                    correction: str = None, evaluation: str = None, score: float = None):
        """حفظ الكتابة"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            
            cursor.execute("""
                INSERT INTO writing_submissions 
                (user_id, lesson_num, text, correction, evaluation, score, created_at)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (user_id, lesson_num, text, correction, evaluation, score, datetime.now()))
            conn.commit()
    
    def get_skill_progress(self, user_id: int, lesson_num: int) -> List[str]:
        """الحصول على المهارات المكتملة للدرس"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT skill_name FROM skill_progress
                WHERE user_id = ? AND lesson_num = ? AND completed = 1
            """, (user_id, lesson_num))
            rows = cursor.fetchall()
            return [row[0] for row in rows]
    
    def is_lesson_completed(self, user_id: int, lesson_num: int) -> bool:
        """التحقق من اكتمال الدرس"""
        required_skills = ['introduction', 'vocabulary', 'grammar', 'reading', 'listening', 'conversation', 'writing']
        completed = self.get_skill_progress(user_id, lesson_num)
        return all(skill in completed for skill in required_skills)
    
    def update_subscription(self, user_id: int, status: str, date: str = None):
        """تحديث حالة الاشتراك"""
        data = {'subscription_status': status}
        if date:
            data['subscription_date'] = date
        return self.update_user(user_id, data)
    
    def update_certificate(self, user_id: int, certificate_id: str, status: str = 'issued'):
        """تحديث بيانات الشهادة"""
        data = {
            'certificate_status': status,
            'certificate_id': certificate_id,
            'certificate_date': datetime.now().isoformat()
        }
        return self.update_user(user_id, data)
    
    def get_statistics(self) -> Dict[str, Any]:
        """الحصول على إحصائيات عامة"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            
            stats = {}
            
            # عدد المستخدمين
            cursor.execute("SELECT COUNT(*) FROM users")
            stats['total_users'] = cursor.fetchone()[0]
            
            # المستخدمين النشطين
            cursor.execute("SELECT COUNT(*) FROM users WHERE active = 1")
            stats['active_users'] = cursor.fetchone()[0]
            
            # المستخدمين المكتملين
            cursor.execute("SELECT COUNT(*) FROM users WHERE completed_lessons >= 18")
            stats['completed_program'] = cursor.fetchone()[0]
            
            # متوسط التقدم
            cursor.execute("SELECT AVG(completed_lessons) FROM users")
            avg = cursor.fetchone()[0]
            stats['average_progress'] = round(avg, 2) if avg else 0
            
            # توزيع اللغات
            cursor.execute("""
                SELECT language, COUNT(*) FROM users GROUP BY language
            """)
            stats['language_distribution'] = dict(cursor.fetchall())
            
            return stats
