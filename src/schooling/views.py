import datetime

from django.shortcuts import render

from schooling.models import Lesson, Teacher, Student
from schooling.utils import check_role_user_from_db


# TODO: 2очереди. Посмотреть и отрефакторить вьюху.
# Возможно в асинхронном представлении
def schedule_page(request, id):
    """Обрабатывает запрос на получение расписания занятий."""
    today = datetime.date.today()
    start_week = today - datetime.timedelta(days=today.weekday())
    end_week = start_week + datetime.timedelta(days=6)
    user = check_role_user_from_db(id, (Teacher, Student))

    if user.__class__.__name__ == 'Teacher':
        schedule = Lesson.objects.filter(teacher_id=user.id)
    else:
        schedule = Lesson.objects.filter(student_id=user.id)

    schedule_mon = schedule.filter(datetime_start__date=start_week)
    schedule_tue = schedule.filter(
        datetime_start__date=start_week + datetime.timedelta(days=1),
    )
    schedule_wed = schedule.filter(
        datetime_start__date=start_week + datetime.timedelta(days=2),
    )
    schedule_thu = schedule.filter(
        datetime_start__date=start_week + datetime.timedelta(days=3),
    )
    schedule_fri = schedule.filter(
        datetime_start__date=start_week + datetime.timedelta(days=4),
    )
    schedule_sat = schedule.filter(
        datetime_start__date=start_week + datetime.timedelta(days=5),
    )
    schedule_sun = schedule.filter(datetime_start__date=end_week)

    context = {
        'start_week': start_week,
        'end_week': end_week,
        'schedule_mon': schedule_mon,
        'schedule_tue': schedule_tue,
        'schedule_wed': schedule_wed,
        'schedule_thu': schedule_thu,
        'schedule_fri': schedule_fri,
        'schedule_sat': schedule_sat,
        'schedule_sun': schedule_sun,
        'role': user.__class__.__name__,
    }

    return render(request, 'schedule/schedule_lessons.html', context)
