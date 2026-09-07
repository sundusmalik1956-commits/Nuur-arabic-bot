# -*- coding: utf-8 -*-
"""
scheduler.py
جدولة إرسال الدرس اليومي عبر JobQueue (لا asyncio.sleep، لا مهام معلّقة).
كل طالب يختار يومي إجازته الأسبوعية بحرية (وليسا يومين ثابتين لكل الطلاب) —
لذلك نحسب days= المسموح بها لـ run_daily من بيانات ذلك الطالب في قاعدة البيانات
عند كل جدولة، ونعيد الجدولة عند تغييره لأيام إجازته.

ترقيم PTB/APScheduler لـ run_daily(days=...) يطابق datetime.weekday():
0=الاثنين 1=الثلاثاء 2=الأربعاء 3=الخميس 4=الجمعة 5=السبت 6=الأحد
"""

from datetime import time as dtime, datetime
import database as db
from lesson_engine import send_lesson

ALL_WEEKDAYS = (0, 1, 2, 3, 4, 5, 6)


def _job_name(user_id: int) -> str:
    return f"daily_lesson_{user_id}"


def _study_days_for_user(user: dict) -> tuple:
    """أيام الأسبوع المسموح بإرسال الدرس فيها لهذا الطالب تحديدًا (كل الأسبوع ما عدا يومي إجازته)."""
    vacation = {user.get("vacation_day_1"), user.get("vacation_day_2")}
    vacation.discard(None)
    return tuple(d for d in ALL_WEEKDAYS if d not in vacation)


async def _daily_job(context):
    user_id = context.job.data["user_id"]
    user = db.get_user(user_id)
    if not user or not user.get("active", 1):
        return
    if not user.get("level"):
        return  # لم يُكمل التسجيل بعد
    if _already_sent_today(user):
        return  # يمنع إرسالاً مضاعفًا لو تصادف run_once (اليوم) مع أول تشغيل لـ run_daily في نفس اليوم
    if not db.is_trial_active(user):
        from translations import t
        await context.bot.send_message(chat_id=user_id, text=t("trial_ended", user.get("language", "ar")))
        return
    if db.program_finished(user):
        return
    await send_lesson(
        context.bot, user_id, user.get("language", "ar"), user["level"], user["current_lesson"], context,
    )


def _already_sent_today(user: dict) -> bool:
    last = user.get("last_lesson_date")
    if not last:
        return False
    try:
        last_dt = datetime.fromisoformat(last)
    except ValueError:
        return False
    return last_dt.date() == datetime.utcnow().date()


def schedule_daily_lesson(job_queue, user_id: int, hour: int, minute: int):
    """يجدول الإرسال اليومي المتكرر بناءً على أيام إجازة هذا الطالب المحفوظة حاليًا في قاعدة
    البيانات. لا يُرسل شيئًا اليوم بحد ذاته — استخدمي trigger_first_lesson_if_today()
    لإرسال أول درس فورًا إن كان يستحق ذلك اليوم. يجب استدعاؤها أيضًا عند تغيير أيام
    الإجازة أو وقت الدرس لإعادة بناء الجدولة بالقيم الجديدة."""
    remove_daily_lesson(job_queue, user_id)
    user = db.get_user(user_id)
    study_days = _study_days_for_user(user) if user else ALL_WEEKDAYS
    job_queue.run_daily(
        _daily_job,
        time=dtime(hour=hour, minute=minute),
        days=study_days,
        data={"user_id": user_id},
        name=_job_name(user_id),
    )


def trigger_first_lesson_if_today(job_queue, user_id: int, hour: int, minute: int):
    """إن كان اليوم يوم دراسة (ليس أحد يومي إجازة الطالب) والوقت المختار لم يمرّ بعد،
    يُجدوَل إرسال أول درس اليوم فورًا في ذلك الوقت عبر run_once — بشكل صريح ومستقل عن
    التوقيت الأول لـ run_daily، حتى لا يعتمد سلوك 'يبدأ اليوم' على تفاصيل داخلية في
    cron/APScheduler."""
    user = db.get_user(user_id)
    if not user or not next_study_moment_is_today(user, hour, minute):
        return False
    now = datetime.now()
    target = now.replace(hour=hour, minute=minute, second=0, microsecond=0)
    delay_seconds = (target - now).total_seconds()
    job_queue.run_once(
        _daily_job,
        when=delay_seconds,
        data={"user_id": user_id},
        name=f"first_lesson_today_{user_id}",
    )
    return True


def remove_daily_lesson(job_queue, user_id: int):
    for job in job_queue.get_jobs_by_name(_job_name(user_id)):
        job.schedule_removal()


def restore_all_schedules(job_queue):
    """يُستدعى عند إقلاع البوت لإعادة بناء الجدولة من قاعدة البيانات فقط."""
    for user in db.get_all_scheduled_users():
        time_str = user.get("lesson_time")
        if not time_str:
            continue
        try:
            hour, minute = map(int, time_str.split(":"))
        except ValueError:
            continue
        schedule_daily_lesson(job_queue, user["user_id"], hour, minute)


def next_study_moment_is_today(user: dict, hour: int, minute: int) -> bool:
    """True إذا كان اليوم ليس أحد يومي إجازة هذا الطالب، والوقت المختار لم يمر بعد."""
    now = datetime.now()
    if db.is_vacation_day(user, now.weekday()):
        return False
    target = now.replace(hour=hour, minute=minute, second=0, microsecond=0)
    return target > now
