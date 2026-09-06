# -*- coding: utf-8 -*-
"""
scheduler.py
جدولة إرسال الدرس اليومي عبر JobQueue بناءً على أيام الإجازة المخصصة لكل طالب.

ترقيم PTB/APScheduler لـ run_daily(days=...) يطابق datetime.weekday():
0=الاثنين, 1=الثلاثاء, 2=الأربعاء, 3=الخميس, 4=الجمعة, 5=السبت, 6=الأحد
"""

from datetime import time as dtime, datetime
import database as db
from lesson_engine import send_lesson

# خريطة تحويل أسماء الأيام المختصرة إلى أرقام الـ weekday في بايثون
DAY_TO_INT = {
    "Mon": 0, "Tue": 1, "Wed": 2, "Thu": 3, "Fri": 4, "Sat": 5, "Sun": 6
}

def _job_name(user_id: int) -> str:
    return f"daily_lesson_{user_id}"

def get_user_study_days(user_id: int) -> tuple:
    """استخراج أيام الدراسة للطالب بناءً على يومي الإجازة اللذين اختارهما."""
    user = db.get_user(user_id)
    rest_days_str = user.get("rest_days") if user else None
    
    # إذا لم يختار الطالب أيام إجازة بعد، نعتبر الافتراضي الجمعة (4) والسبت (5) أو حسب الرغبة (الافتراضي هنا Thu, Fri)
    if not rest_days_str:
        rest_list = ["Thu", "Fri"]
    else:
        rest_list = [d.strip() for d in rest_days_str.split(",") if d.strip()]
        
    rest_ints = {DAY_TO_INT[d] for d in rest_list if d in DAY_TO_INT}
    
    # أيام الدراسة هي كل الأيام ما عدا يومي الإجازة
    all_days = {0, 1, 2, 3, 4, 5, 6}
    study_days = tuple(all_days - rest_ints)
    return study_days

async def _daily_job(context):
    user_id = context.job.data["user_id"]
    user = db.get_user(user_id)
    if not user or not user.get("active", 1):
        return
    if not db.is_trial_active(user):
        from translations import t
        # استخدام مفتاح الدفع المعتمد في الـ Paywall بدلاً من trial_ended غير الموجود في ملف الترجمات
        await context.bot.send_message(chat_id=user_id, text=t("paywall_tribute", user.get("language", "ar")))
        return
    if db.program_finished(user):
        return
    await send_lesson(context.bot, user_id, user.get("language", "ar"), user["current_lesson"], context)


def schedule_daily_lesson(job_queue, user_id: int, hour: int, minute: int):
    remove_daily_lesson(job_queue, user_id)
    
    # جلب أيام الدراسة المخصصة لهذا الطالب
    study_days = get_user_study_days(user_id)
    
    job_queue.run_daily(
        _daily_job,
        time=dtime(hour=hour, minute=minute),
        days=study_days,
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


def next_study_moment_is_today(user_id: int, hour: int, minute: int) -> bool:
    """True إذا كان اليوم يوم دراسة للطالب والوقت المختار لم يمر بعد."""
    now = datetime.now()
    study_days = get_user_study_days(user_id)
    
    if now.weekday() not in study_days:
        return False
        
    # تصحيح الخطأ الإملائي في دالة الوقت (استخدام replace مباشرة بدلاً من index_replace غير الموجودة)
    target = now.replace(hour=hour, minute=minute, second=0, microsecond=0)
    return target > now
