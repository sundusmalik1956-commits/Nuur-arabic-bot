# -*- coding: utf-8 -*-
"""
scheduler.py
جدولة إرسال الدرس اليومي عبر JobQueue.
أيام الإجازة: الخميس والجمعة.
أيام الدراسة: السبت، الأحد، الاثنين، الثلاثاء، الأربعاء.

ترقيم PTB/APScheduler لـ run_daily(days=...) يطابق datetime.weekday():
0=الاثنين, 1=الثلاثاء, 2=الأربعاء, 3=الخميس, 4=الجمعة, 5=السبت, 6=الأحد
"""

from datetime import time as dtime, datetime
import database as db
from lesson_engine import send_lesson

STUDY_DAYS = (5, 6, 0, 1, 2)  # السبت (5)، الأحد (6)، الاثنين (0)، الثلاثاء (1)، الأربعاء (2)
OFF_DAYS = (3, 4)             # الخميس (3)، الجمعة (4)


def _job_name(user_id: int) -> str:
    return f"daily_lesson_{user_id}"


async def _daily_job(context):
    user_id = context.job.data["user_id"]
    user = db.get_user(user_id)
    if not user or not user.get("active", 1):
        return
    if not db.is_trial_active(user):
        from translations import t
        await context.bot.send_message(chat_id=user_id, text=t("trial_ended", user.get("language", "ar")))
        return
    if db.program_finished(user):
        return
    await send_lesson(context.bot, user_id, user.get("language", "ar"), user["current_lesson"], context)


def schedule_daily_lesson(job_queue, user_id: int, hour: int, minute: int):
    remove_daily_lesson(job_queue, user_id)
    job_queue.run_daily(
        _daily_job,
        time=dtime(hour=hour, minute=minute),
        days=STUDY_DAYS,
        data={"user_id": user_id},
        name=_job_name(user_id),
    )


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


def next_study_moment_is_today(hour: int, minute: int) -> bool:
    """True إذا كان اليوم يوم دراسة والوقت المختار لم يمر بعد."""
    now = datetime.now()
    if now.weekday() in OFF_DAYS:
        return False
    target = now.replace(hour=hour, minute=minute, second=0, microsecond=0)
    return target > now
