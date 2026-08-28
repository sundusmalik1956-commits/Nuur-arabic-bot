"""
Noor Bot — البنية الأساسية

هذا الملف مسؤول عن تشغيل البوت وإدارة التدفق العام فقط.
محتوى الدروس يوضع في ملفات مستقلة مثل lesson1.py و lesson2.py.
"""

import asyncio
import importlib
import json
import logging
import os
import sqlite3
import urllib.error
import urllib.request
from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo

from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import (
    Application,
    CallbackQueryHandler,
    CommandHandler,
    ContextTypes,
    JobQueue,
    MessageHandler,
    filters,
)


# ------------------------------
# الإعدادات العامة
# ------------------------------

BASE_DIR = Path(__file__).resolve().parent
DATABASE_PATH = BASE_DIR / "noor_bot.db"
BOT_TOKEN = os.getenv("8629063079:AAHvPGBfbTdCJyHXz2EpHWzPiG8KfgroMMo") or os.getenv("TELEGRAM_BOT_TOKEN")
TIMEZONE = os.getenv("TIMEZONE", "UTC")
ADMIN_GROUP_ID = os.getenv("ADMIN_GROUP_ID") or os.getenv("-1003785748588")
# ضع GEMINI_API_KEY أو AI_API_KEY في إعدادات الاستضافة.
AI_API_KEY = os.getenv("GEMINI_API_KEY") or os.getenv("iXp2hUjxXlJmdVc_xwTT7DEpVb1b1MqUJOSi-lQ")
AI_MODEL = os.getenv("AI_MODEL", "gemini-2.5-flash")
AI_API_URL = os.getenv(
    "AI_API_URL",
    "https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent",
)
FREE_LESSONS = 5
STUDY_DAYS = {6, 0, 1, 2, 3}  # الأحد إلى الخميس في weekday(): الأحد=6

LANGUAGES = {
    "ar": "العربية 🇸🇦",
    "en": "English 🇬🇧",
    "tr": "Türkçe 🇹🇷",
}

TIME_OPTIONS = ["06:00", "08:00", "10:00", "12:00", "14:00", "16:00", "18:00", "20:00", "22:00"]

logging.basicConfig(
    format="%(asctime)s — %(name)s — %(levelname)s — %(message)s",
    level=logging.INFO,
)
logger = logging.getLogger("noor_bot")


# ------------------------------
# قاعدة البيانات المؤقتة الأساسية
# ------------------------------


def get_connection() -> sqlite3.Connection:
    connection = sqlite3.connect(DATABASE_PATH)
    connection.row_factory = sqlite3.Row
    return connection


def init_database() -> None:
    with get_connection() as connection:
        connection.execute(
            """
            CREATE TABLE IF NOT EXISTS students (
                user_id INTEGER PRIMARY KEY,
                username TEXT,
                first_name TEXT,
                language TEXT,
                lesson_time TEXT,
                current_lesson INTEGER NOT NULL DEFAULT 1,
                completed_lessons INTEGER NOT NULL DEFAULT 0,
                active INTEGER NOT NULL DEFAULT 1,
                created_at TEXT NOT NULL,
                updated_at TEXT NOT NULL
            )
            """
        )
        connection.execute(
            """
            CREATE TABLE IF NOT EXISTS lesson_progress (
                user_id INTEGER NOT NULL,
                lesson_number INTEGER NOT NULL,
                skill TEXT NOT NULL,
                completed INTEGER NOT NULL DEFAULT 0,
                attempts INTEGER NOT NULL DEFAULT 0,
                completed_at TEXT,
                PRIMARY KEY (user_id, lesson_number, skill)
            )
            """
        )
        # ترقية قواعد البيانات القديمة دون فقد بيانات الطلاب.
        try:
            connection.execute("ALTER TABLE students ADD COLUMN current_skill TEXT")
        except sqlite3.OperationalError:
            pass
        connection.commit()


def save_student(update: Update, language: str | None = None, lesson_time: str | None = None) -> None:
    user = update.effective_user
    now = datetime.utcnow().isoformat(timespec="seconds")

    with get_connection() as connection:
        connection.execute(
            """
            INSERT INTO students (user_id, username, first_name, language, lesson_time, created_at, updated_at)
            VALUES (?, ?, ?, ?, ?, ?, ?)
            ON CONFLICT(user_id) DO UPDATE SET
                username = excluded.username,
                first_name = excluded.first_name,
                language = COALESCE(excluded.language, students.language),
                lesson_time = COALESCE(excluded.lesson_time, students.lesson_time),
                updated_at = excluded.updated_at
            """ ,
            (user.id, user.username, user.first_name, language, lesson_time, now, now),
        )
        connection.commit()


def get_student(user_id: int):
    with get_connection() as connection:
        return connection.execute("SELECT * FROM students WHERE user_id = ?", (user_id,)).fetchone()


def update_student(user_id: int, **values) -> None:
    if not values:
        return
    values["updated_at"] = datetime.utcnow().isoformat(timespec="seconds")
    columns = ", ".join(f"{column} = ?" for column in values)
    with get_connection() as connection:
        connection.execute(f"UPDATE students SET {columns} WHERE user_id = ?", (*values.values(), user_id))
        connection.commit()


def record_progress(user_id: int, lesson_number: int, skill: str, completed: bool = True) -> bool:
    """يحفظ تقدم مهارة ويعيد True إذا اكتملت كل مهارات الدرس."""
    now = datetime.utcnow().isoformat(timespec="seconds")
    with get_connection() as connection:
        connection.execute(
            """
            INSERT INTO lesson_progress (user_id, lesson_number, skill, completed, attempts, completed_at)
            VALUES (?, ?, ?, ?, 1, ?)
            ON CONFLICT(user_id, lesson_number, skill) DO UPDATE SET
                completed = MAX(lesson_progress.completed, excluded.completed),
                attempts = lesson_progress.attempts + 1,
                completed_at = CASE WHEN excluded.completed = 1 THEN excluded.completed_at ELSE lesson_progress.completed_at END
            """,
            (user_id, lesson_number, skill, int(completed), now if completed else None),
        )
        required = {"introduction", "vocabulary", "grammar", "reading", "listening", "conversation", "writing"}
        rows = connection.execute(
            "SELECT skill FROM lesson_progress WHERE user_id = ? AND lesson_number = ? AND completed = 1",
            (user_id, lesson_number),
        ).fetchall()
        finished = required.issubset({row["skill"] for row in rows})
        connection.commit()
    return finished


async def announce_lesson_completion(user_id: int, lesson_number: int, context) -> None:
    """يرسل إشعارًا للقروب مرة واحدة فقط عند إتمام الدرس."""
    if not ADMIN_GROUP_ID:
        logger.warning("ADMIN_GROUP_ID غير مضبوط؛ لن يتم إرسال إشعار القروب.")
        return
    with get_connection() as connection:
        row = connection.execute(
            "SELECT completed_lessons FROM students WHERE user_id = ?", (user_id,)
        ).fetchone()
        if not row:
            return
        already_announced = connection.execute(
            "SELECT 1 FROM lesson_progress WHERE user_id = ? AND lesson_number = ? AND skill = 'announcement_sent' AND completed = 1",
            (user_id, lesson_number),
        ).fetchone()
        if already_announced:
            return
        connection.execute(
            "INSERT OR REPLACE INTO lesson_progress (user_id, lesson_number, skill, completed, attempts, completed_at) VALUES (?, ?, 'announcement_sent', 1, 1, ?)",
            (user_id, lesson_number, 1, datetime.utcnow().isoformat(timespec="seconds")),
        )
        connection.execute(
            "UPDATE students SET completed_lessons = MAX(completed_lessons, ?), current_lesson = MAX(current_lesson, ?), updated_at = ? WHERE user_id = ?",
            (lesson_number, lesson_number + 1, datetime.utcnow().isoformat(timespec="seconds"), user_id),
        )
        connection.commit()
    student = get_student(user_id)
    display_name = student["first_name"] if student else str(user_id)
    await context.bot.send_message(
        chat_id=ADMIN_GROUP_ID,
        text=f"✅ أتم الطالب {display_name} (ID: {user_id}) جميع تدريبات الدرس {lesson_number}.",
    )


# ------------------------------
# طبقة الذكاء الاصطناعي
# ------------------------------


def _call_gemini_api(prompt: str) -> str:
    """استدعاء Gemini بطريقة متوافقة مع بيئة الاستضافة."""
    if not AI_API_KEY:
        raise RuntimeError("لم يتم ضبط GEMINI_API_KEY أو AI_API_KEY")

    url = AI_API_URL.format(model=AI_MODEL)
    if "?" not in url:
        url += "?key=" + AI_API_KEY
    elif "key=" not in url:
        url += "&key=" + AI_API_KEY

    payload = {
        "contents": [{"parts": [{"text": prompt}]}],
        "generationConfig": {
            "temperature": 0.3,
            "maxOutputTokens": 700,
        },
    }
    request = urllib.request.Request(
        url,
        data=json.dumps(payload).encode("utf-8"),
        headers={"Content-Type": "application/json"},
        method="POST",
    )

    try:
        with urllib.request.urlopen(request, timeout=45) as response:
            data = json.loads(response.read().decode("utf-8"))
    except urllib.error.HTTPError as error:
        details = error.read().decode("utf-8", errors="ignore")
        raise RuntimeError(f"AI API error {error.code}: {details[:300]}") from error
    except urllib.error.URLError as error:
        raise RuntimeError(f"تعذر الاتصال بخدمة الذكاء الاصطناعي: {error.reason}") from error

    try:
        return data["candidates"][0]["content"]["parts"][0]["text"].strip()
    except (KeyError, IndexError, TypeError) as error:
        raise RuntimeError("رد الذكاء الاصطناعي غير متوقع") from error


async def evaluate_arabic_answer(answer: str, language: str) -> str:
    """تقييم إجابة الطالب العربية مع إخراج الشرح بلغة الواجهة المختارة."""
    interface_language = {"ar": "العربية", "en": "English", "tr": "Türkçe"}.get(language, "العربية")
    prompt = f"""
أنت مدرس لغة عربية لغير الناطقين بها في Noor Bot.
قيّم إجابة الطالب التالية: {answer}
لغة شرح النتيجة يجب أن تكون: {interface_language}.
المادة التي يتعلمها الطالب تبقى بالعربية.

أعد نتيجة قصيرة ومنظمة بهذا الشكل:
✅ أو ❌ النتيجة:
التصحيح: ...
الشرح: ...
التقييم التقريبي: من 10

إذا كانت الإجابة صحيحة، اذكر ذلك بوضوح ولا تخترع أخطاء.
"""
    return await asyncio.to_thread(_call_gemini_api, prompt)


async def ai_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """يعالج رسائل الطالب النصية ويرسلها إلى الذكاء الاصطناعي."""
    if not update.message or not update.message.text:
        return

    save_student(update)
    student = get_student(update.effective_user.id)
    language = student["language"] if student and student["language"] else "ar"

    if not AI_API_KEY:
        await update.message.reply_text(
            "لم يتم تفعيل الذكاء الاصطناعي بعد. أضف GEMINI_API_KEY في إعدادات الاستضافة."
        )
        return

    waiting_message = await update.message.reply_text("جارٍ تحليل إجابتك...")
    try:
        result = await evaluate_arabic_answer(update.message.text, language)
        await waiting_message.edit_text(result)
        # إجابة المحادثة أو الكتابة تُسجّل بعد إرسال تحليل AI.
        current_skill = student["current_skill"] if student and "current_skill" in student.keys() else None
        if current_skill in {"conversation", "writing"}:
            finished = record_progress(update.effective_user.id, 1, current_skill)
            if finished:
                await announce_lesson_completion(update.effective_user.id, 1, context)
    except Exception:
        logger.exception("AI evaluation failed for user %s", update.effective_user.id)
        await waiting_message.edit_text("تعذر تحليل الإجابة الآن. حاول مرة أخرى لاحقًا.")


# ------------------------------
# الواجهة الأساسية
# ------------------------------


def language_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup([
        [InlineKeyboardButton(name, callback_data=f"language:{code}")]
        for code, name in LANGUAGES.items()
    ])


def time_keyboard() -> InlineKeyboardMarkup:
    rows = []
    for index in range(0, len(TIME_OPTIONS), 3):
        rows.append([
            InlineKeyboardButton(value, callback_data=f"time:{value}")
            for value in TIME_OPTIONS[index:index + 3]
        ])
    return InlineKeyboardMarkup(rows)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    save_student(update)
    await update.message.reply_text(
        "مرحبًا بك في نور بوت لتعليم اللغة العربية.\n\nاختر لغة التعليم:",
        reply_markup=language_keyboard(),
    )


async def choose_language(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    await query.answer()
    language = query.data.split(":", 1)[1]
    save_student(update, language=language)
    await query.edit_message_text(
        "تم حفظ لغة التعليم.\n\nاختر الوقت المناسب لوصول الدرس اليومي:",
        reply_markup=time_keyboard(),
    )


async def choose_time(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    await query.answer()
    lesson_time = query.data.split(":", 1)[1]
    update_student(query.from_user.id, lesson_time=lesson_time, active=1)
    await query.edit_message_text(
        f"تم حفظ وقت الدرس: {lesson_time}\n\nسأرسل لك الدروس من الأحد إلى الخميس."
    )
    await send_current_lesson(query.from_user.id, context)


async def lesson_callback(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """يوجّه أزرار أسئلة الدروس إلى ملف الدرس المناسب."""
    query = update.callback_query
    lesson_module_name = query.data.split(":", 1)[0]
    try:
        lesson_module = importlib.import_module(lesson_module_name)
        correct = await lesson_module.handle_callback(query, context)
        if correct:
            question_id = query.data.split(":")[1]
            skill = {"v1": "vocabulary", "g1": "grammar", "r1": "reading", "l1": "listening"}.get(question_id)
            if skill:
                finished = record_progress(query.from_user.id, 1, skill)
                if finished:
                    await announce_lesson_completion(query.from_user.id, 1, context)
    except Exception:
        logger.exception("Lesson callback failed: %s", query.data)
        await query.answer("تعذر معالجة الإجابة الآن.", show_alert=True)


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(
        "الأوامر المتاحة:\n/start — بدء أو إعادة إعداد الحساب\n/lesson — فتح الدرس الحالي\n/help — عرض المساعدة\n\nأرسل إجابة بالعربية ليقيّمها الذكاء الاصطناعي."
    )


async def lesson_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    save_student(update)
    await send_current_lesson(update.effective_user.id, context)


# ------------------------------
# تشغيل الدروس والجدولة
# ------------------------------


async def send_current_lesson(user_id: int, context: ContextTypes.DEFAULT_TYPE) -> None:
    student = get_student(user_id)
    if student is None:
        return

    current_lesson = student["current_lesson"]
    if current_lesson > FREE_LESSONS:
        await context.bot.send_message(
            chat_id=user_id,
            text="🎓 انتهت الفترة التجريبية المجانية.\nالبرنامج الكامل مدفوع، وسيتم تفعيل الاشتراك لاحقًا.",
        )
        return

    module_name = f"lesson{current_lesson}"
    try:
        lesson_module = importlib.import_module(module_name)
        send_function = getattr(lesson_module, "send_lesson", None)
        if send_function is None:
            raise AttributeError(f"{module_name}.py must define async send_lesson(user_id, context)")
        await send_function(user_id, context)
    except ModuleNotFoundError:
        await context.bot.send_message(
            chat_id=user_id,
            text=f"الدرس {current_lesson} قيد الإعداد. أرسل ملف lesson{current_lesson}.py لإضافته.",
        )
    except Exception:
        logger.exception("Failed to send lesson %s to user %s", current_lesson, user_id)
        await context.bot.send_message(chat_id=user_id, text="حدث خطأ مؤقت أثناء فتح الدرس. حاول مرة أخرى لاحقًا.")


async def daily_lesson_job(context: ContextTypes.DEFAULT_TYPE) -> None:
    now = datetime.now(ZoneInfo(TIMEZONE))
    if now.weekday() not in STUDY_DAYS:
        return

    with get_connection() as connection:
        students = connection.execute(
            "SELECT user_id, lesson_time FROM students WHERE active = 1 AND lesson_time = ?",
            (now.strftime("%H:%M"),),
        ).fetchall()

    for student in students:
        await send_current_lesson(student["user_id"], context)


# ------------------------------
# نقطة تشغيل البرنامج
# ------------------------------


def build_application() -> Application:
    if not BOT_TOKEN:
        raise RuntimeError("ضع BOT_TOKEN في متغيرات البيئة قبل تشغيل البوت.")

    init_database()
    application = Application.builder().token(BOT_TOKEN).job_queue(JobQueue()).build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler("lesson", lesson_command))
    application.add_handler(CallbackQueryHandler(choose_language, pattern=r"^language:"))
    application.add_handler(CallbackQueryHandler(choose_time, pattern=r"^time:"))
    application.add_handler(CallbackQueryHandler(lesson_callback, pattern=r"^lesson[0-9]+:"))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, ai_message))

    # الفحص كل دقيقة؛ لا نستخدم asyncio.sleep داخل مهمة الجدولة.
    application.job_queue.run_repeating(daily_lesson_job, interval=60, first=10)
    return application


def main() -> None:
    application = build_application()
    logger.info("Noor Bot is starting...")
    application.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()

