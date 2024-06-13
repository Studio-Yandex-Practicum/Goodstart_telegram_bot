import datetime

from django.shortcuts import render
from asgiref.sync import sync_to_async

from schooling.models import Teacher, Student
from schooling.utils import (
    get_schedule_for_role, get_schedule_week_tasks,
)
from bot.utils import check_user_from_db


async def schedule_page(request, id):
    """Обрабатывает запрос на получение расписания занятий."""
    today = datetime.date.today()
    start_week = today - datetime.timedelta(days=today.weekday())
    end_week = start_week + datetime.timedelta(days=6)

    user = await check_user_from_db(id, (Teacher, Student))

    schedule = await get_schedule_for_role(user)

    (
        schedule_mon, schedule_tue, schedule_wed,
        schedule_thu, schedule_fri, schedule_sat, schedule_sun,
    ) = await get_schedule_week_tasks(schedule, start_week)

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

    return await sync_to_async(render)(
        request, 'schedule/schedule.html', context,
    )
