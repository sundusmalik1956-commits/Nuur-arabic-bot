# -*- coding: utf-8 -*-
"""
database.py
إدارة قاعدة البيانات SQLite الخاصة بـ "نور بوت".
"""

import sqlite3

DB_NAME = "bot_database.db"

def get_db_connection():
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            user_id INTEGER PRIMARY KEY,
            username TEXT,
            first_name TEXT,
            language TEXT DEFAULT 'ar',
            lesson_time TEXT,
            current_lesson INTEGER DEFAULT 1,
            completed_lessons INTEGER DEFAULT 0,
            pending_skill TEXT DEFAULT NULL
        )
    """)
    
    conn.commit()
    conn.close()

def create_user_if_missing(user_id: int, username: str = None, first_name: str = None):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT user_id FROM users WHERE user_id = ?", (user_id,))
    row = cursor.fetchone()
    if not row:
        cursor.execute(
            "INSERT INTO users (user_id, username, first_name) VALUES (?, ?, ?)",
            (user_id, username, first_name)
        )
        conn.commit()
    conn.close()

def get_user(user_id: int):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE user_id = ?", (user_id,))
    row = cursor.fetchone()
    conn.close()
    return dict(row) if row else None

def set_language(user_id: int, language: str):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("UPDATE users SET language = ? WHERE user_id = ?", (language, user_id))
    conn.commit()
    conn.close()

def set_lesson_time(user_id: int, lesson_time: str):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("UPDATE users SET lesson_time = ? WHERE user_id = ?", (lesson_time, user_id))
    conn.commit()
    conn.close()

def update_progress(user_id: int, current_lesson: int, completed_lessons: int):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        "UPDATE users SET current_lesson = ?, completed_lessons = ? WHERE user_id = ?",
        (current_lesson, completed_lessons, user_id)
    )
    conn.commit()
    conn.close()

def get_all_scheduled_users():
    """استرجاع جميع المستخدمين الذين لديهم أوقات دروس مجدولة."""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT user_id, lesson_time FROM users WHERE lesson_time IS NOT NULL")
    rows = cursor.fetchall()
    conn.close()
    return [dict(row) for row in rows]

def set_pending_skill(user_id: int, skill: str | None):
    """حفظ أو مسح حالة المهارة المعلقة للمستخدم في قاعدة البيانات بشكل دائم."""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("UPDATE users SET pending_skill = ? WHERE user_id = ?", (skill, user_id))
    conn.commit()
    conn.close()

def get_pending_skill(user_id: int) -> str | None:
    """استرجاع المهارة المعلقة الحالية الخاصة بالمستخدم."""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT pending_skill FROM users WHERE user_id = ?", (user_id,))
    row = cursor.fetchone()
    conn.close()
    if row and row["pending_skill"]:
        return row["pending_skill"]
    return None
