import datetime

from django.urls import reverse_lazy
from django.shortcuts import render, HttpResponseRedirect
from asgiref.sync import sync_to_async

from schooling.forms import ChangeDateTimeLesson
from schooling.models import Teacher, Student, Lesson
from schooling.utils import (
    get_schedule_for_role, get_schedule_week_tasks,
)
from bot.utils import check_user_from_db


async def schedule_page(request, id):
    """Обрабатывает запрос на получение расписания занятий."""
    week_offset = int(request.GET.get('week', 0))

    today = datetime.date.today()
    start_week = (
    today + datetime.timedelta(weeks=week_offset, days=-today.weekday())
    )
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
        'user_tg_id': user.telegram_id,
        'week_offset': week_offset,
    }

    return await sync_to_async(render)(
        request, 'schedule.html', context,
    )

async def details_schedule_page(request, id, lesson_id):
    context = {}
    user = await check_user_from_db(id, (Teacher, Student))
    user_role = user.__class__.__name__
    lesson = await Lesson.objects.select_related(
        'subject', 'teacher_id', 'student_id',
    ).aget(id=lesson_id)

    if user_role == 'Teacher':
        context['user_full_name'] = (
            f'{lesson.student_id}'
        )
    else:
        context['user_full_name'] = (
            f'{lesson.teacher_id}'
        )

    context['user_tg_id'] = user.telegram_id
    context['user_role'] = user_role
    context['lesson'] = lesson

    return await sync_to_async(render)(
        request, 'schedule_details_card.html', context,
    )


async def change_datetime_lesson(request, id, lesson_id):
    form = ChangeDateTimeLesson()

    if request.method == 'POST':
        form = ChangeDateTimeLesson(request.POST)
        if form.is_valid():
            # Обработка успешной отправки формы
            return HttpResponseRedirect(
                reverse_lazy('schedule:lesson_change_success'),
                )

            # TODO: обработать сценарий отправки заявки администратору.

    return render(
        request,
        'schedule_change_dt_lesson.html',
        context={'form': form},
    )


async def cancel_lesson(request, id, lesson_id):
    if request.method == 'POST':
         return HttpResponseRedirect(
            reverse_lazy('schedule:lesson_cancel_success'),
            )

    return render(
        request,
        'schedule_cancel_lesson.html',
    )

def lesson_change_success(request):
    return render(request, 'lesson_change_success.html')

def lesson_cancel_success(request):
    return render(request, 'lesson_cancel_success.html')
