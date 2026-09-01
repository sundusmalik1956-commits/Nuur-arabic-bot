# -*- coding: utf-8 -*-
"""
database.py
طبقة SQLite الوحيدة لحفظ كل حالة البوت. لا يُعتمد على context.user_data لأي بيانات
يجب أن تبقى بعد إعادة تشغيل البوت — فقط هذا الملف هو مصدر الحقيقة.
"""

import sqlite3
import os
import logging
from datetime import datetime
from contextlib import contextmanager

logger = logging.getLogger(__name__)

DB_PATH = os.path.join(os.path.dirname(__file__), "noor_bot.db")

TOTAL_LESSONS = 18
FREE_LESSONS = 5
STUDY_WEEKDAYS = (5, 6, 0, 1, 2)   # السبت, الأحد, الاثنين, الثلاثاء, الأربعاء
OFF_WEEKDAYS = (3, 4)              # الخميس, الجمعة


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
                language TEXT,
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


# ---------------------------------------------------------------------------
# المستخدمون
# ---------------------------------------------------------------------------

def get_user(user_id: int):
    with get_conn() as conn:
        row = conn.execute("SELECT * FROM users WHERE user_id = ?", (user_id,)).fetchone()
        return dict(row) if row else None


def create_user_if_missing(user_id: int, username: str = None, first_name: str = None):
    with get_conn() as conn:
        conn.execute(
            """INSERT OR IGNORE INTO users (user_id, username, first_name, created_at, updated_at)
               VALUES (?, ?, ?, ?, ?)""",
            (user_id, username, first_name, _now(), _now()),
        )
        conn.commit()


def update_user_fields(user_id: int, **fields):
    if not fields:
        return
    fields["updated_at"] = _now()
    columns = ", ".join(f"{k} = ?" for k in fields)
    values = list(fields.values()) + [user_id]
    with get_conn() as conn:
        conn.execute(f"UPDATE users SET {columns} WHERE user_id = ?", values)
        conn.commit()


def set_language(user_id: int, language: str):
    update_user_fields(user_id, language=language)


def set_lesson_time(user_id: int, time_str: str):
    update_user_fields(user_id, lesson_time=time_str)


def get_all_scheduled_users():
    with get_conn() as conn:
        rows = conn.execute(
            "SELECT * FROM users WHERE lesson_time IS NOT NULL AND active = 1"
        ).fetchall()
        return [dict(r) for r in rows]


def mark_lesson_started_today(user_id: int):
    update_user_fields(user_id, last_lesson_date=_now())


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


def set_subscription_status(user_id: int, status: str):
    update_user_fields(user_id, subscription_status=status, subscription_date=_now())


def is_trial_active(user: dict) -> bool:
    if user.get("subscription_status") == "active":
        return True
    return (user.get("completed_lessons") or 0) < FREE_LESSONS


def program_finished(user: dict) -> bool:
    return (user.get("completed_lessons") or 0) >= TOTAL_LESSONS


# ---------------------------------------------------------------------------
# إدارة المهارة المعلقة للذكاء الاصطناعي (Pending Skill)
# ---------------------------------------------------------------------------

def set_pending_skill(user_id: int, skill: str | None):
    """حفظ أو مسح حالة المهارة المعلقة للمستخدم في قاعدة البيانات بشكل دائم."""
    update_user_fields(user_id, pending_skill=skill)


def get_pending_skill(user_id: int) -> str | None:
    """استرجاع المهارة المعلقة الحالية الخاصة بالمستخدم."""
    user = get_user(user_id)
    if user and user.get("pending_skill"):
        return user["pending_skill"]
    return None


# ---------------------------------------------------------------------------
# تقدّم المهارات داخل الدرس
# ---------------------------------------------------------------------------

def start_skill(user_id: int, lesson_number: int, skill: str):
    with get_conn() as conn:
        conn.execute(
            """INSERT OR IGNORE INTO lesson_progress
               (user_id, lesson_number, skill, status, started_at)
               VALUES (?, ?, ?, 'in_progress', ?)""",
            (user_id, lesson_number, skill, _now()),
        )
        conn.commit()


def complete_skill(user_id: int, lesson_number: int, skill: str):
    with get_conn() as conn:
        conn.execute(
            """INSERT INTO lesson_progress (user_id, lesson_number, skill, status, started_at, completed_at)
               VALUES (?, ?, ?, 'completed', ?, ?)
               ON CONFLICT(user_id, lesson_number, skill)
               DO UPDATE SET status='completed', completed_at=excluded.completed_at""",
            (user_id, lesson_number, skill, _now(), _now()),
        )
        conn.commit()


def get_completed_skills(user_id: int, lesson_number: int) -> set:
    with get_conn() as conn:
        rows = conn.execute(
            """SELECT skill FROM lesson_progress
               WHERE user_id = ? AND lesson_number = ? AND status = 'completed'""",
            (user_id, lesson_number),
        ).fetchall()
        return {r["skill"] for r in rows}


def reset_lesson_progress(user_id: int, lesson_number: int):
    """يمسح تقدّم مهارات درس معيّن، يُستخدم عند بدء الدرس من جديد."""
    with get_conn() as conn:
        conn.execute(
            "DELETE FROM lesson_progress WHERE user_id = ? AND lesson_number = ?",
            (user_id, lesson_number),
        )
        conn.execute(
            "DELETE FROM answers WHERE user_id = ? AND lesson_number = ?",
            (user_id, lesson_number),
        )
        conn.commit()


# ---------------------------------------------------------------------------
# إجابات الاختيار من متعدد
# ---------------------------------------------------------------------------

def record_answer(user_id: int, lesson_number: int, skill: str, question_key: str,
                   selected_option: str, is_correct: bool):
    with get_conn() as conn:
        existing = conn.execute(
            """SELECT id, attempts FROM answers
               WHERE user_id=? AND lesson_number=? AND skill=? AND question_key=?""",
            (user_id, lesson_number, skill, question_key),
        ).fetchone()
        if existing:
            conn.execute(
                """UPDATE answers SET selected_option=?, is_correct=?, attempts=attempts+1, answered_at=?
                   WHERE id=?""",
                (selected_option, int(is_correct), _now(), existing["id"]),
            )
        else:
            conn.execute(
                """INSERT INTO answers
                   (user_id, lesson_number, skill, question_key, selected_option, is_correct, attempts, answered_at)
                   VALUES (?, ?, ?, ?, ?, ?, 1, ?)""",
                (user_id, lesson_number, skill, question_key, selected_option, int(is_correct), _now()),
            )
        conn.commit()


def is_question_answered_correctly(user_id: int, lesson_number: int, skill: str, question_key: str) -> bool:
    with get_conn() as conn:
        row = conn.execute(
            """SELECT is_correct FROM answers
               WHERE user_id=? AND lesson_number=? AND skill=? AND question_key=?""",
            (user_id, lesson_number, skill, question_key),
        ).fetchone()
        return bool(row and row["is_correct"])


def all_questions_answered_correctly(user_id: int, lesson_number: int, skill: str, question_keys: list) -> bool:
    return all(
        is_question_answered_correctly(user_id, lesson_number, skill, qk)
        for qk in question_keys
    )


# ---------------------------------------------------------------------------
# إتمام الدروس
# ---------------------------------------------------------------------------

def log_completion(user_id: int, lesson_number: int, lesson_title: str):
    with get_conn() as conn:
        conn.execute(
            """INSERT INTO completions (user_id, lesson_number, lesson_title, completed_at)
               VALUES (?, ?, ?, ?)""",
            (user_id, lesson_number, lesson_title, _now()),
        )
        conn.commit()
