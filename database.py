# -*- coding: utf-8 -*-
"""
database.py
طبقة SQLite لحفظ حالة البوت ومزامنة ملف Excel لبيانات الطلاب مع دعم اللغة وأيام الإجازة.
"""

import sqlite3
import os
import logging
from datetime import datetime
from contextlib import contextmanager
import pandas as pd

logger = logging.getLogger(__name__)

DB_PATH = os.path.join(os.path.dirname(__file__), "noor_bot.db")
EXCEL_PATH = os.path.join(os.path.dirname(__file__), "students_data.xlsx")

TOTAL_LESSONS = 18
FREE_LESSONS = 5


@contextmanager
def get_conn():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    try:
        yield conn
    finally:
        conn.close()


def init_db():
    with get_conn() as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS users (
                user_id INTEGER PRIMARY KEY,
                username TEXT,
                first_name TEXT,
                language TEXT DEFAULT 'ar',
                rest_days TEXT DEFAULT 'Thu,Fri',
                gender TEXT,
                group_id INTEGER,
                lesson_time TEXT,
                current_lesson INTEGER DEFAULT 1,
                completed_lessons INTEGER DEFAULT 0,
                active INTEGER DEFAULT 1,
                speaking_score REAL,
                writing_score REAL,
                certificate_status TEXT DEFAULT 'none',
                certificate_id TEXT,
                certificate_url TEXT,
                certificate_date TEXT,
                subscription_status TEXT DEFAULT 'trial',
                subscription_date TEXT,
                last_lesson_date TEXT,
                timezone TEXT,
                created_at TEXT,
                updated_at TEXT,
                pending_skill TEXT DEFAULT NULL
            )
        """)
        conn.execute("""
            CREATE TABLE IF NOT EXISTS lesson_progress (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER,
                lesson_number INTEGER,
                skill TEXT,
                status TEXT DEFAULT 'in_progress',
                started_at TEXT,
                completed_at TEXT,
                UNIQUE(user_id, lesson_number, skill)
            )
        """)
        conn.execute("""
            CREATE TABLE IF NOT EXISTS answers (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER,
                lesson_number INTEGER,
                skill TEXT,
                question_key TEXT,
                selected_option TEXT,
                is_correct INTEGER,
                attempts INTEGER DEFAULT 1,
                answered_at TEXT
            )
        """)
        conn.execute("""
            CREATE TABLE IF NOT EXISTS completions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER,
                lesson_number INTEGER,
                lesson_title TEXT,
                completed_at TEXT
            )
        """)
        conn.commit()
    logger.info("قاعدة البيانات جاهزة.")


def _now():
    return datetime.utcnow().isoformat()


def sync_student_to_excel(user_id: int):
    """مزامنة بيانات الطالب وتضمين اللغة وأيام الإجازة والجنس في ملف الإكسل تلقائياً"""
    try:
        user = get_user(user_id)
        if not user:
            return
        
        record = {
            "user_id": str(user.get("user_id")),
            "username": user.get("username", ""),
            "first_name": user.get("first_name", ""),
            "language": user.get("language", "ar"),
            "rest_days": user.get("rest_days", "Thu,Fri"),
            "gender": user.get("gender", ""),
            "lesson_time": user.get("lesson_time", ""),
            "current_lesson": user.get("current_lesson", 1),
            "completed_lessons": user.get("completed_lessons", 0),
            "subscription_status": user.get("subscription_status", "trial"),
            "updated_at": user.get("updated_at", _now())
        }
        
        if os.path.exists(EXCEL_PATH):
            df = pd.read_excel(EXCEL_PATH)
            df["user_id"] = df["user_id"].astype(str)
            if record["user_id"] in df["user_id"].values:
                for k, v in record.items():
                    df.loc[df["user_id"] == record["user_id"], k] = v
            else:
                new_row = pd.DataFrame([record])
                df = pd.concat([df, new_row], ignore_index=True)
        else:
            df = pd.DataFrame([record])
            
        df.to_excel(EXCEL_PATH, index=False)
    except Exception as e:
        logger.error(f"خطأ أثناء مزامنة بيانات الطالب مع الإكسل: {e}")


def get_user(user_id: int):
    with get_conn() as conn:
        row = conn.execute("SELECT * FROM users WHERE user_id = ?", (user_id,)).fetchone()
        return dict(row) if row else None


def get_all_users():
    with get_conn() as conn:
        rows = conn.execute("SELECT * FROM users").fetchall()
        return {row["user_id"]: dict(row) for row in rows}


def get_all_scheduled_users():
    with get_conn() as conn:
        rows = conn.execute("SELECT * FROM users WHERE lesson_time IS NOT NULL AND active = 1").fetchall()
        return [dict(row) for row in rows]


def create_user_if_missing(user_id: int, username: str = None, first_name: str = None):
    with get_conn() as conn:
        conn.execute(
            """INSERT OR IGNORE INTO users (user_id, username, first_name, language, created_at, updated_at)
               VALUES (?, ?, ?, 'ar', ?, ?)""",
            (user_id, username, first_name, _now(), _now()),
        )
        conn.commit()
    sync_student_to_excel(user_id)


def update_user_fields(user_id: int, **fields):
    if not fields:
        return
    fields["updated_at"] = _now()
    columns = ", ".join(f"{k} = ?" for k in fields)
    values = list(fields.values()) + [user_id]
    with get_conn() as conn:
        conn.execute(f"UPDATE users SET {columns} WHERE user_id = ?", values)
        conn.commit()
    sync_student_to_excel(user_id)


def set_language(user_id: int, language: str):
    update_user_fields(user_id, language=language)


def set_lesson_time(user_id: int, time_str: str):
    update_user_fields(user_id, lesson_time=time_str)


def advance_to_next_lesson(user_id: int):
    with get_conn() as conn:
        conn.execute(
            """UPDATE users
               SET current_lesson = current_lesson + 1,
                   completed_lessons = completed_lessons + 1,
                   updated_at = ?
               WHERE user_id = ?""",
            (_now(), user_id),
        )
        conn.commit()
    sync_student_to_excel(user_id)


def set_subscription_status(user_id: int, status: str):
    update_user_fields(user_id, subscription_status=status, subscription_date=_now())


def is_trial_active(user: dict) -> bool:
    if user.get("subscription_status") == "active":
        return True
    return user.get("current_lesson", 1) <= FREE_LESSONS


def program_finished(user: dict) -> bool:
    return user.get("current_lesson", 1) > TOTAL_LESSONS
