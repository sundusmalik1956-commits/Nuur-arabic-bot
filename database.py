# -*- coding: utf-8 -*-
"""
database.py
طبقة SQLite الوحيدة لحفظ كل حالة البوت. لا يُعتمد على context.user_data لأي بيانات
يجب أن تبقى بعد إعادة تشغيل البوت — فقط هذا الملف هو مصدر الحقيقة.

الجداول:
    users           بيانات الطالب الأساسية والاشتراك والتقدّم
    lesson_progress سجل تقدّم الطالب داخل كل درس (أي مهارات أتمّها فعليًا)
    answers         كل إجابة اختيار من متعدد أرسلها الطالب (للتتبّع والتحليل)
    completions     سجل كل درس أُتمّ فعليًا (لإعلان الإنجاز وأرشفته)
"""

import sqlite3
import os
import logging
from datetime import datetime
from contextlib import contextmanager

logger = logging.getLogger(__name__)

DB_PATH = os.path.join(os.path.dirname(__file__), "noor_bot.db")

FREE_LESSONS = 5
TOTAL_LESSONS_DEFAULT = 18
TOTAL_LESSONS_A0 = 4

LEVELS = ("A0", "A1", "A2", "B1", "B2")

GROUP_LINKS = {
    "male": "https://t.me/rijalnurakademik",
    "female": "https://t.me/nisanurakademik",
}


def total_lessons_for_level(level: str) -> int:
    return TOTAL_LESSONS_A0 if level == "A0" else TOTAL_LESSONS_DEFAULT


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
                level TEXT,
                gender TEXT,
                group_link TEXT,
                lesson_time TEXT,
                vacation_day_1 INTEGER,
                vacation_day_2 INTEGER,
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
                updated_at TEXT
            )
        """)
        conn.execute("""
            CREATE TABLE IF NOT EXISTS lesson_progress (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER,
                level TEXT,
                lesson_number INTEGER,
                skill TEXT,
                status TEXT DEFAULT 'in_progress',
                started_at TEXT,
                completed_at TEXT,
                UNIQUE(user_id, level, lesson_number, skill)
            )
        """)
        conn.execute("""
            CREATE TABLE IF NOT EXISTS answers (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER,
                level TEXT,
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
                level TEXT,
                lesson_number INTEGER,
                lesson_title TEXT,
                completed_at TEXT
            )
        """)
        conn.commit()
        _migrate_new_columns(conn)
    logger.info("قاعدة البيانات جاهزة.")


def _migrate_new_columns(conn):
    """يضيف أعمدة جديدة لقاعدة بيانات موجودة مسبقًا من نسخة سابقة من البوت (idempotent)."""
    existing_columns = {row["name"] for row in conn.execute("PRAGMA table_info(users)").fetchall()}
    new_columns = {
        "level": "TEXT",
        "gender": "TEXT",
        "group_link": "TEXT",
        "vacation_day_1": "INTEGER",
        "vacation_day_2": "INTEGER",
    }
    for col, col_type in new_columns.items():
        if col not in existing_columns:
            conn.execute(f"ALTER TABLE users ADD COLUMN {col} {col_type}")
            logger.info(f"تمت إضافة عمود جديد لقاعدة البيانات: {col}")

    for table in ("lesson_progress", "answers", "completions"):
        cols = {row["name"] for row in conn.execute(f"PRAGMA table_info({table})").fetchall()}
        if "level" not in cols:
            conn.execute(f"ALTER TABLE {table} ADD COLUMN level TEXT")
            logger.info(f"تمت إضافة عمود level لجدول {table}")
    conn.commit()


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
    """تحديث عام لأي أعمدة في users. مثال: update_user_fields(123, language='en')"""
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


def set_level(user_id: int, level: str):
    update_user_fields(user_id, level=level, current_lesson=1)


def set_gender_and_group(user_id: int, gender: str):
    group_link = GROUP_LINKS.get(gender)
    update_user_fields(user_id, gender=gender, group_link=group_link)


def set_lesson_time(user_id: int, time_str: str):
    update_user_fields(user_id, lesson_time=time_str)


def set_vacation_days(user_id: int, day1: int, day2: int):
    update_user_fields(user_id, vacation_day_1=day1, vacation_day_2=day2)


def is_vacation_day(user: dict, weekday_num: int) -> bool:
    """weekday_num بترقيم Python: الاثنين=0 ... الأحد=6."""
    return weekday_num in (user.get("vacation_day_1"), user.get("vacation_day_2"))


def get_all_users():
    """كل الطلاب المسجَّلين، بكل الأعمدة — تُستخدم فقط لتصدير Excel الإداري."""
    with get_conn() as conn:
        rows = conn.execute("SELECT * FROM users ORDER BY created_at").fetchall()
        return [dict(r) for r in rows]


def get_all_scheduled_users():
    with get_conn() as conn:
        rows = conn.execute(
            """SELECT * FROM users
               WHERE lesson_time IS NOT NULL AND level IS NOT NULL AND active = 1"""
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
    """status: trial | active | expired | cancelled"""
    update_user_fields(user_id, subscription_status=status, subscription_date=_now())


def is_trial_active(user: dict) -> bool:
    if user.get("subscription_status") == "active":
        return True
    return (user.get("completed_lessons") or 0) < FREE_LESSONS


def program_finished(user: dict) -> bool:
    total = total_lessons_for_level(user.get("level") or "A1")
    return (user.get("completed_lessons") or 0) >= total


# ---------------------------------------------------------------------------
# تقدّم المهارات داخل الدرس
# ---------------------------------------------------------------------------

def start_skill(user_id: int, level: str, lesson_number: int, skill: str):
    with get_conn() as conn:
        conn.execute(
            """INSERT OR IGNORE INTO lesson_progress
               (user_id, level, lesson_number, skill, status, started_at)
               VALUES (?, ?, ?, ?, 'in_progress', ?)""",
            (user_id, level, lesson_number, skill, _now()),
        )
        conn.commit()


def complete_skill(user_id: int, level: str, lesson_number: int, skill: str):
    with get_conn() as conn:
        conn.execute(
            """INSERT INTO lesson_progress (user_id, level, lesson_number, skill, status, started_at, completed_at)
               VALUES (?, ?, ?, ?, 'completed', ?, ?)
               ON CONFLICT(user_id, level, lesson_number, skill)
               DO UPDATE SET status='completed', completed_at=excluded.completed_at""",
            (user_id, level, lesson_number, skill, _now(), _now()),
        )
        conn.commit()


def get_completed_skills(user_id: int, level: str, lesson_number: int) -> set:
    with get_conn() as conn:
        rows = conn.execute(
            """SELECT skill FROM lesson_progress
               WHERE user_id = ? AND level = ? AND lesson_number = ? AND status = 'completed'""",
            (user_id, level, lesson_number),
        ).fetchall()
        return {r["skill"] for r in rows}


def reset_lesson_progress(user_id: int, level: str, lesson_number: int):
    """يمسح تقدّم مهارات درس معيّن، يُستخدم عند بدء الدرس من جديد."""
    with get_conn() as conn:
        conn.execute(
            "DELETE FROM lesson_progress WHERE user_id = ? AND level = ? AND lesson_number = ?",
            (user_id, level, lesson_number),
        )
        conn.execute(
            "DELETE FROM answers WHERE user_id = ? AND level = ? AND lesson_number = ?",
            (user_id, level, lesson_number),
        )
        conn.commit()


# ---------------------------------------------------------------------------
# إجابات الاختيار من متعدد
# ---------------------------------------------------------------------------

def record_answer(user_id: int, level: str, lesson_number: int, skill: str, question_key: str,
                   selected_option: str, is_correct: bool):
    with get_conn() as conn:
        existing = conn.execute(
            """SELECT id, attempts FROM answers
               WHERE user_id=? AND level=? AND lesson_number=? AND skill=? AND question_key=?""",
            (user_id, level, lesson_number, skill, question_key),
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
                   (user_id, level, lesson_number, skill, question_key, selected_option, is_correct, attempts, answered_at)
                   VALUES (?, ?, ?, ?, ?, ?, ?, 1, ?)""",
                (user_id, level, lesson_number, skill, question_key, selected_option, int(is_correct), _now()),
            )
        conn.commit()


def is_question_answered_correctly(user_id: int, level: str, lesson_number: int, skill: str, question_key: str) -> bool:
    with get_conn() as conn:
        row = conn.execute(
            """SELECT is_correct FROM answers
               WHERE user_id=? AND level=? AND lesson_number=? AND skill=? AND question_key=?""",
            (user_id, level, lesson_number, skill, question_key),
        ).fetchone()
        return bool(row and row["is_correct"])


def all_questions_answered_correctly(user_id: int, level: str, lesson_number: int, skill: str, question_keys: list) -> bool:
    return all(
        is_question_answered_correctly(user_id, level, lesson_number, skill, qk)
        for qk in question_keys
    )


# ---------------------------------------------------------------------------
# إتمام الدروس
# ---------------------------------------------------------------------------

def log_completion(user_id: int, level: str, lesson_number: int, lesson_title: str):
    with get_conn() as conn:
        conn.execute(
            """INSERT INTO completions (user_id, level, lesson_number, lesson_title, completed_at)
               VALUES (?, ?, ?, ?, ?)""",
            (user_id, level, lesson_number, lesson_title, _now()),
        )
        conn.commit()


def is_completion_logged(user_id: int, level: str, lesson_number: int) -> bool:
    with get_conn() as conn:
        row = conn.execute(
            "SELECT id FROM completions WHERE user_id=? AND level=? AND lesson_number=?",
            (user_id, level, lesson_number),
        ).fetchone()
        return row is not None
