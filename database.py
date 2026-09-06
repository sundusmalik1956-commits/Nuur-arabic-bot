import sqlite3
import json
from datetime import datetime
from typing import Dict, List, Optional

class Database:
    def __init__(self, db_path='users.db'):
        self.db_path = db_path
        self.init_db()
    
    def init_db(self):
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS users (
                    user_id INTEGER PRIMARY KEY,
                    username TEXT,
                    first_name TEXT,
                    last_name TEXT,
                    language TEXT DEFAULT 'ar',
                    level TEXT,
                    gender TEXT,
                    lesson_time TEXT,
                    days_off TEXT,
                    current_lesson INTEGER DEFAULT 0,
                    is_subscribed BOOLEAN DEFAULT FALSE,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS user_progress (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id INTEGER,
                    lesson_number INTEGER,
                    completed BOOLEAN DEFAULT FALSE,
                    completed_at TIMESTAMP,
                    FOREIGN KEY (user_id) REFERENCES users(user_id)
                )
            ''')
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS user_settings (
                    user_id INTEGER PRIMARY KEY,
                    settings TEXT,
                    FOREIGN KEY (user_id) REFERENCES users(user_id)
                )
            ''')
            conn.commit()
    
    def get_user(self, user_id: int) -> Optional[Dict]:
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM users WHERE user_id = ?', (user_id,))
            row = cursor.fetchone()
            if row:
                columns = [description[0] for description in cursor.description]
                return dict(zip(columns, row))
            return None
    
    def create_user(self, user_id: int, username: str = None, first_name: str = None, last_name: str = None):
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                INSERT OR IGNORE INTO users (user_id, username, first_name, last_name)
                VALUES (?, ?, ?, ?)
            ''', (user_id, username, first_name, last_name))
            conn.commit()
    
    def update_user(self, user_id: int, **kwargs):
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            fields = []
            values = []
            for key, value in kwargs.items():
                if key in ['username', 'first_name', 'last_name', 'language', 'level', 'gender', 'lesson_time', 'days_off', 'current_lesson', 'is_subscribed']:
                    if key == 'days_off' and isinstance(value, list):
                        value = json.dumps(value)
                    fields.append(f"{key} = ?")
                    values.append(value)
            if fields:
                values.append(user_id)
                query = f"UPDATE users SET {', '.join(fields)}, updated_at = CURRENT_TIMESTAMP WHERE user_id = ?"
                cursor.execute(query, values)
                conn.commit()
    
    def get_user_settings(self, user_id: int) -> Dict:
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT settings FROM user_settings WHERE user_id = ?', (user_id,))
            row = cursor.fetchone()
            if row and row[0]:
                return json.loads(row[0])
            return {}
    
    def save_user_settings(self, user_id: int, settings: Dict):
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                INSERT OR REPLACE INTO user_settings (user_id, settings)
                VALUES (?, ?)
            ''', (user_id, json.dumps(settings)))
            conn.commit()
    
    def get_all_users(self) -> List[Dict]:
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM users')
            rows = cursor.fetchall()
            columns = [description[0] for description in cursor.description]
            users = []
            for row in rows:
                user = dict(zip(columns, row))
                if user.get('days_off'):
                    user['days_off'] = json.loads(user['days_off'])
                users.append(user)
            return users
    
    def get_users_by_time(self, hour: int, minute: int) -> List[Dict]:
        time_str = f"{hour:02d}:{minute:02d}"
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM users WHERE lesson_time = ?', (time_str,))
            rows = cursor.fetchall()
            columns = [description[0] for description in cursor.description]
            users = []
            for row in rows:
                user = dict(zip(columns, row))
                if user.get('days_off'):
                    user['days_off'] = json.loads(user['days_off'])
                users.append(user)
            return users
    
    def record_lesson_completion(self, user_id: int, lesson_number: int):
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                INSERT OR REPLACE INTO user_progress (user_id, lesson_number, completed, completed_at)
                VALUES (?, ?, ?, CURRENT_TIMESTAMP)
            ''', (user_id, lesson_number, True))
            conn.commit()
    
    def get_completed_lessons(self, user_id: int) -> List[int]:
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT lesson_number FROM user_progress WHERE user_id = ? AND completed = TRUE', (user_id,))
            rows = cursor.fetchall()
            return [row[0] for row in rows]
