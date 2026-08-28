# =========================================================
# NOOR BOT
# Arabic Learning Bot
# Scalable architecture for 18 lessons
# =========================================================

import os
import sqlite3
import logging
import importlib
from datetime import datetime, time
from zoneinfo import ZoneInfo

from dotenv import load_dotenv

from telegram import (
    Update,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
)

from telegram.ext import (
    Application,
    CommandHandler,
    CallbackQueryHandler,
    ContextTypes,
    MessageHandler,
    filters,
)

# Gemini
from google import genai


# =========================================================
# ENVIRONMENT
# =========================================================

load_dotenv()

BOT_TOKEN = os.getenv("8629063079:AAHvPGBfbTdCJyHXz2EpHWzPiG8KfgroMMo")
GEMINI_API_KEY = os.getenv("iXp2hUjxXlJmdVc_xwTT7DEpVb1b1MqUJOSi-lQ")

# =========================================================
# GENERAL SETTINGS
# =========================================================

BOT_NAME = "نور بوت"

DB_NAME = "noor_bot.db"

TIMEZONE = ZoneInfo("Asia/Riyadh")

FREE_LESSONS = 5
TOTAL_LESSONS = 18

# Friday = 4
# Saturday = 5
NO_LESSON_DAYS = {4, 5}

# =========================================================
# ACHIEVEMENT GROUP
# =========================================================

ACHIEVEMENT_GROUP_ID = -1003785748588


# =========================================================
# LOGGING
# =========================================================

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)

logger = logging.getLogger(BOT_NAME)


# =========================================================
# GEMINI
# =========================================================

gemini_client = None

if GEMINI_API_KEY:
    try:
        gemini_client = genai.Client(
            api_key=GEMINI_API_KEY
        )

        logger.info("Gemini AI initialized.")

    except Exception as error:
        logger.exception(
            "Could not initialize Gemini: %s",
            error
        )

else:
    logger.warning(
        "GEMINI_API_KEY was not found. "
        "AI correction will be unavailable."
    )


# =========================================================
# DATABASE
# =========================================================

def get_db():
    connection = sqlite3.connect(
        DB_NAME,
        check_same_thread=False
    )

    connection.row_factory = sqlite3.Row

    return connection


def init_database():

    connection = get_db()

    cursor = connection.cursor()

    # -----------------------------------------------------
    # USERS
    # -----------------------------------------------------

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (

            user_id INTEGER PRIMARY KEY,

            username TEXT,

            first_name TEXT,

            language TEXT DEFAULT 'en',

            lesson_time TEXT,

            current_lesson INTEGER DEFAULT 1,

            completed_lessons INTEGER DEFAULT 0,

            active INTEGER DEFAULT 1,

            learning_mode TEXT DEFAULT NULL,

            ai_context TEXT DEFAULT '',

            created_at TEXT,

            updated_at TEXT
        )
    """)

    # -----------------------------------------------------
    # LESSON PROGRESS
    # -----------------------------------------------------

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS lesson_progress (

            id INTEGER PRIMARY KEY AUTOINCREMENT,

            user_id INTEGER,

            lesson_number INTEGER,

            completed INTEGER DEFAULT 0,

            started_at TEXT,

            completed_at TEXT,

            UNIQUE(user_id, lesson_number)
        )
    """)

    connection.commit()

    connection.close()


# =========================================================
# USER FUNCTIONS
# =========================================================

def create_or_update_user(
    user_id,
    username=None,
    first_name=None
):

    connection = get_db()

    now = datetime.now(
        TIMEZONE
    ).isoformat()

    connection.execute("""
        INSERT INTO users (
            user_id,
            username,
            first_name,
            created_at,
            updated_at
        )

        VALUES (?, ?, ?, ?, ?)

        ON CONFLICT(user_id)

        DO UPDATE SET

            username = excluded.username,

            first_name = excluded.first_name,

            updated_at = excluded.updated_at

    """, (
        user_id,
        username,
        first_name,
        now,
        now
    ))

    connection.commit()

    connection.close()


def get_user(user_id):

    connection = get_db()

    cursor = connection.execute("""
        SELECT *
        FROM users
        WHERE user_id = ?
    """, (user_id,))

    user = cursor.fetchone()

    connection.close()

    return user


def set_user_language(
    user_id,
    language
):

    connection = get_db()

    connection.execute("""
        UPDATE users

        SET language = ?,
            updated_at = ?

        WHERE user_id = ?
    """, (
        language,
        datetime.now(
            TIMEZONE
        ).isoformat(),
        user_id
    ))

    connection.commit()

    connection.close()


def set_user_time(
    user_id,
    lesson_time
):

    connection = get_db()

    connection.execute("""
        UPDATE users

        SET lesson_time = ?,
            updated_at = ?

        WHERE user_id = ?
    """, (
        lesson_time,
        datetime.now(
            TIMEZONE
        ).isoformat(),
        user_id
    ))

    connection.commit()

    connection.close()


def set_learning_mode(
    user_id,
    mode
):

    """
    mode examples:

    None
    speaking
    writing
    """

    connection = get_db()

    connection.execute("""
        UPDATE users

        SET learning_mode = ?,
            updated_at = ?

        WHERE user_id = ?
    """, (
        mode,
        datetime.now(
            TIMEZONE
        ).isoformat(),
        user_id
    ))

    connection.commit()

    connection.close()


def get_learning_mode(user_id):

    user = get_user(user_id)

    if not user:
        return None

    return user["learning_mode"]


def set_ai_context(
    user_id,
    context
):

    connection = get_db()

    connection.execute("""
        UPDATE users

        SET ai_context = ?,
            updated_at = ?

        WHERE user_id = ?
    """, (
        context,
        datetime.now(
            TIMEZONE
        ).isoformat(),
        user_id
    ))

    connection.commit()

    connection.close()


def get_ai_context(user_id):

    user = get_user(user_id)

    if not user:
        return ""

    return user["ai_context"] or ""


# =========================================================
# LESSON PROGRESS
# =========================================================

def start_lesson_progress(
    user_id,
    lesson_number
):

    connection = get_db()

    now = datetime.now(
        TIMEZONE
    ).isoformat()

    connection.execute("""
        INSERT INTO lesson_progress (
            user_id,
            lesson_number,
            completed,
            started_at
        )

        VALUES (?, ?, 0, ?)

        ON CONFLICT(user_id, lesson_number)

        DO UPDATE SET

            started_at = excluded.started_at
    """, (
        user_id,
        lesson_number,
        now
    ))

    connection.commit()

    connection.close()


def complete_lesson(
    user_id,
    lesson_number
):

    connection = get_db()

    now = datetime.now(
        TIMEZONE
    ).isoformat()

    # -----------------------------------------------------
    # Check if already completed
    # -----------------------------------------------------

    cursor = connection.execute("""
        SELECT completed
        FROM lesson_progress

        WHERE user_id = ?
        AND lesson_number = ?
    """, (
        user_id,
        lesson_number
    ))

    row = cursor.fetchone()

    if row and row["completed"] == 1:

        connection.close()

        return False

    # -----------------------------------------------------
    # Mark lesson completed
    # -----------------------------------------------------

    connection.execute("""
        INSERT INTO lesson_progress (
            user_id,
            lesson_number,
            completed,
            started_at,
            completed_at
        )

        VALUES (?, ?, 1, ?, ?)

        ON CONFLICT(user_id, lesson_number)

        DO UPDATE SET

            completed = 1,

            completed_at = excluded.completed_at
    """, (
        user_id,
        lesson_number,
        now,
        now
    ))

    # -----------------------------------------------------
    # Count completed lessons
    # -----------------------------------------------------

    cursor = connection.execute("""
        SELECT COUNT(*)
        FROM lesson_progress

        WHERE user_id = ?
        AND completed = 1
    """, (user_id,))

    completed_count = cursor.fetchone()[0]

    # -----------------------------------------------------
    # Update user
    # -----------------------------------------------------

    connection.execute("""
        UPDATE users

        SET completed_lessons = ?,

            current_lesson = ?,

            learning_mode = NULL,

            ai_context = '',

            updated_at = ?

        WHERE user_id = ?
    """, (
        completed_count,
        completed_count + 1,
        now,
        user_id
    ))

    connection.commit()

    connection.close()

    return True


# =========================================================
# LANGUAGES
# =========================================================

LANGUAGES = {

    "ar": {
        "name": "العربية 🇸🇦"
    },

    "en": {
        "name": "English 🇬🇧"
    },

    "tr": {
        "name": "Türkçe 🇹🇷"
    },

}


# =========================================================
# BASIC TRANSLATIONS
# =========================================================

TEXTS = {

    "ar": {

        "welcome":
            "مرحبًا بك في نور بوت ✨\n\n"
            "بوت تفاعلي يساعدك على تعلم اللغة العربية "
            "خطوة بخطوة من خلال المفردات والقواعد "
            "والقراءة والاستماع والمحادثة والكتابة.",

        "choose_language":
            "🌍 اختر اللغة التي تريد أن تظهر بها "
            "التوضيحات والتعليمات:",

        "choose_time":
            "⏰ اختر الوقت المناسب لك لإرسال الدرس يوميًا.\n\n"
            "يتم إرسال الدروس من الأحد إلى الخميس، "
            "ولا توجد دروس يوم الجمعة والسبت.",

        "time_selected":
            "تم حفظ وقت التعلم بنجاح ✅\n\n"
            "سيصلك الدرس في الوقت الذي اخترته "
            "من الأحد إلى الخميس.",

        "free_period":
            "🎁 لديك 5 دروس مجانية لتجربة نور بوت.",

        "paid_after":
            "🎓 انتهت الفترة التجريبية المجانية.\n\n"
            "يمكنك الاشتراك في البرنامج الكامل مقابل 5$.\n\n"
            "نظام الدفع سيتم تفعيله لاحقًا.",

        "lesson_started":
            "📚 بدأ درس اليوم.",

        "lesson_not_ready":
            "هذا الدرس لم تتم إضافته إلى البوت بعد ✨",

        "lesson_error":
            "حدث خطأ أثناء تشغيل الدرس. "
            "تم تسجيل المشكلة وسيتم إصلاحها.",

        "lesson_completed":
            "🎉 أحسنت!\n\n"
            "لقد أتممت الدرس بنجاح.",

        "progress":
            "📊 تقدمك:\n\n"
            "الدروس المكتملة: {completed}/18\n"
            "الدرس الحالي: {current}",

        "settings":
            "⚙️ الإعدادات",

        "unknown":
            "اختر أحد الخيارات من الأزرار الموجودة "
            "أسفل الرسالة.",

        "ai_unavailable":
            "🤖 التصحيح بالذكاء الاصطناعي غير متاح حاليًا. "
            "حاول لاحقًا.",

        "ai_error":
            "حدث خطأ أثناء تصحيح إجابتك. حاول مرة أخرى.",

    },


    "en": {

        "welcome":
            "Welcome to Noor Bot ✨\n\n"
            "An interactive Arabic learning bot that "
            "helps you learn step by step through "
            "vocabulary, grammar, reading, listening, "
            "speaking and writing.",

        "choose_language":
            "🌍 Choose the language for explanations "
            "and instructions:",

        "choose_time":
            "⏰ Choose the time for your daily lesson.\n\n"
            "Lessons are sent from Sunday to Thursday. "
            "There are no lessons on Friday or Saturday.",

        "time_selected":
            "Your learning time has been saved successfully ✅\n\n"
            "Your lesson will arrive at the selected time "
            "from Sunday to Thursday.",

        "free_period":
            "🎁 You have 5 free lessons to try Noor Bot.",

        "paid_after":
            "🎓 Your free trial has ended.\n\n"
            "The full program costs $5.\n\n"
            "Payment will be added later.",

        "lesson_started":
            "📚 Today's lesson has started.",

        "lesson_not_ready":
            "This lesson has not been added yet ✨",

        "lesson_error":
            "An error occurred while starting the lesson. "
            "The problem has been logged.",

        "lesson_completed":
            "🎉 Excellent!\n\n"
            "You have successfully completed the lesson.",

        "progress":
            "📊 Your progress:\n\n"
            "Completed lessons: {completed}/18\n"
            "Current lesson: {current}",

        "settings":
            "⚙️ Settings",

        "unknown":
            "Please choose one of the buttons below.",

        "ai_unavailable":
            "🤖 AI correction is currently unavailable. "
            "Please try again later.",

        "ai_error":
            "An error occurred while correcting your answer. "
            "Please try again.",

    },


    "tr": {

        "welcome":
            "Noor Bot'a hoş geldiniz ✨\n\n"
            "Kelime bilgisi, dil bilgisi, okuma, dinleme, "
            "konuşma ve yazma becerileriyle Arapçayı "
            "adım adım öğrenmenize yardımcı olur.",

        "choose_language":
            "🌍 Açıklamalar ve yönergeler için dili seçin:",

        "choose_time":
            "⏰ Günlük dersiniz için uygun zamanı seçin.\n\n"
            "Dersler pazar-perşembe günleri gönderilir. "
            "Cuma ve cumartesi ders yoktur.",

        "time_selected":
            "Öğrenme saatiniz başarıyla kaydedildi ✅\n\n"
            "Dersiniz seçtiğiniz saatte gönderilecektir.",

        "free_period":
            "🎁 Noor Bot'u denemek için 5 ücretsiz dersiniz var.",

        "paid_after":
            "🎓 Ücretsiz deneme süreniz sona erdi.\n\n"
            "Tam programın fiyatı 5$'dır.\n\n"
            "Ödeme sistemi daha sonra eklenecektir.",

        "lesson_started":
            "📚 Bugünkü ders başladı.",

        "lesson_not_ready":
            "Bu ders henüz eklenmedi ✨",

        "lesson_error":
            "Ders başlatılırken bir hata oluştu.",

        "lesson_completed":
            "🎉 Harika!\n\n"
            "Dersi başarıyla tamamladınız.",

        "progress":
            "📊 İlerlemeniz:\n\n"
            "Tamamlanan dersler: {completed}/18\n"
            "Mevcut ders: {current}",

        "settings":
            "⚙️ Ayarlar",

        "unknown":
            "Lütfen aşağıdaki düğmelerden birini seçin.",

        "ai_unavailable":
            "🤖 Yapay zekâ düzeltmesi şu anda kullanılamıyor.",

        "ai_error":
            "Cevabınız düzeltilirken bir hata oluştu.",

    }

}


def t(
    language,
    key,
    **kwargs
):

    if language not in TEXTS:
        language = "en"

    text = TEXTS[language].get(
        key,
        key
    )

    return text.format(**kwargs)


# =========================================================
# LANGUAGE KEYBOARD
# =========================================================

def language_keyboard():

    keyboard = [

        [
            InlineKeyboardButton(
                "العربية 🇸🇦",
                callback_data="lang_ar"
            )
        ],

        [
            InlineKeyboardButton(
                "English 🇬🇧",
                callback_data="lang_en"
            )
        ],

        [
            InlineKeyboardButton(
                "Türkçe 🇹🇷",
                callback_data="lang_tr"
            )
        ],

    ]

    return InlineKeyboardMarkup(
        keyboard
    )


# =========================================================
# TIME KEYBOARD
# =========================================================

def time_keyboard():

    times = [

        ("06:00", "time_06_00"),
        ("08:00", "time_08_00"),
        ("10:00", "time_10_00"),

        ("12:00", "time_12_00"),
        ("14:00", "time_14_00"),
        ("16:00", "time_16_00"),

        ("18:00", "time_18_00"),
        ("20:00", "time_20_00"),
        ("22:00", "time_22_00"),

    ]

    keyboard = []

    for i in range(
        0,
        len(times),
        3
    ):

        row = []

        for name, callback in times[
            i:i + 3
        ]:

            row.append(
                InlineKeyboardButton(
                    name,
                    callback_data=callback
                )
            )

        keyboard.append(row)

    return InlineKeyboardMarkup(
        keyboard
    )


# =========================================================
# /START
# =========================================================

async def start(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):

    user = update.effective_user

    create_or_update_user(
        user_id=user.id,
        username=user.username,
        first_name=user.first_name
    )

    await update.message.reply_text(
        TEXTS["en"]["choose_language"],
        reply_markup=language_keyboard()
    )


# =========================================================
# LANGUAGE CALLBACK
# =========================================================

async def language_callback(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):

    query = update.callback_query

    await query.answer()

    user_id = query.from_user.id

    language = query.data.replace(
        "lang_",
        ""
    )

    set_user_language(
        user_id,
        language
    )

    await query.edit_message_text(
        t(
            language,
            "welcome"
        )
    )

    await query.message.reply_text(
        t(
            language,
            "free_period"
        )
    )

    await query.message.reply_text(
        t(
            language,
            "choose_time"
        ),
        reply_markup=time_keyboard()
    )


# =========================================================
# TIME CALLBACK
# =========================================================

async def time_callback(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):

    query = update.callback_query

    await query.answer()

    user_id = query.from_user.id

    selected_time = (
        query.data
        .replace("time_", "")
        .replace("_", ":")
    )

    set_user_time(
        user_id,
        selected_time
    )

    user = get_user(user_id)

    if not user:
        return

    language = user["language"]

    await query.edit_message_text(
        t(
            language,
            "time_selected"
        )
    )

    schedule_user_lessons(
        context.application,
        user_id,
        selected_time
    )


# =========================================================
# SCHEDULE ONE USER
# =========================================================

def schedule_user_lessons(
    application,
    user_id,
    lesson_time
):

    try:

        hour, minute = map(
            int,
            lesson_time.split(":")
        )

    except ValueError:

        logger.error(
            "Invalid lesson time for user %s: %s",
            user_id,
            lesson_time
        )

        return

    job_name = (
        f"daily_lesson_{user_id}"
    )

    # -----------------------------------------------------
    # Remove previous schedule
    # -----------------------------------------------------

    existing_jobs = (
        application
        .job_queue
        .get_jobs_by_name(
            job_name
        )
    )

    for job in existing_jobs:

        job.schedule_removal()

    # -----------------------------------------------------
    # Sunday - Thursday
    # -----------------------------------------------------

    application.job_queue.run_daily(

        send_daily_lesson,

        time=time(
            hour=hour,
            minute=minute,
            tzinfo=TIMEZONE
        ),

        days=(
            0,  # Monday
            1,  # Tuesday
            2,  # Wednesday
            3,  # Thursday
            6,  # Sunday
        ),

        data={
            "user_id": user_id
        },

        name=job_name

    )

    logger.info(
        "Scheduled user %s at %s",
        user_id,
        lesson_time
    )


# =========================================================
# RESTORE ALL SCHEDULES
# =========================================================

def restore_all_schedules(
    application
):

    connection = get_db()

    cursor = connection.execute("""
        SELECT
            user_id,
            lesson_time,
            active

        FROM users

        WHERE lesson_time IS NOT NULL
        AND active = 1
    """)

    users = cursor.fetchall()

    connection.close()

    for user in users:

        try:

            schedule_user_lessons(
                application,
                user["user_id"],
                user["lesson_time"]
            )

        except Exception:

            logger.exception(
                "Could not restore schedule for user %s",
                user["user_id"]
            )

    logger.info(
        "Restored schedules for %s users.",
        len(users)
    )


# =========================================================
# DAILY LESSON
# =========================================================

async def send_daily_lesson(
    context: ContextTypes.DEFAULT_TYPE
):

    user_id = context.job.data[
        "user_id"
    ]

    user = get_user(user_id)

    if not user:
        return

    if not user["active"]:
        return

    # -----------------------------------------------------
    # Friday / Saturday protection
    # -----------------------------------------------------

    now = datetime.now(
        TIMEZONE
    )

    if now.weekday()
