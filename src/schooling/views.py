import pytz
import datetime

from django.urls import reverse, reverse_lazy
from django.shortcuts import render, HttpResponseRedirect
from asgiref.sync import sync_to_async
from django.conf import settings

from schooling.forms import ChangeDateTimeLesson
from schooling.models import Teacher, Student, Lesson
from schooling.signals_bot import (
    get_schedule_for_role, get_schedule_week_tasks,
)
from bot.utils import check_user_from_db
from core.utils import send_change_lesson_email, send_cancel_lesson_email


EMAIL_HOST_USER = settings.EMAIL_HOST_USER


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
    elif user_role == 'Student':
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
            lesson = await Lesson.objects.aget(id=lesson_id)
            new_datetime = form.cleaned_data['dt_field']
            user = await check_user_from_db(id, (Student, Teacher))
            moscow_tz = pytz.timezone('Europe/Moscow')
            new_datetime_moscow = new_datetime.astimezone(moscow_tz)
            formatted_datetime = new_datetime_moscow.strftime(
                '%Y-%m-%d %H:%M:%S',
            )
            await send_change_lesson_email(lesson, user, formatted_datetime)
            redirect_url = (
                reverse('schedule:lesson_change_success') +
                f'?new_datetime={formatted_datetime}'
            )
            return HttpResponseRedirect(redirect_url)
    return await sync_to_async(render)(
        request,
        'schedule_change_dt_lesson.html',
        context={'form': form},
    )


async def cancel_lesson(request, id, lesson_id):
    if request.method == 'POST':
        lesson = await Lesson.objects.aget(id=lesson_id)
        user = await check_user_from_db(id, (Student, Teacher))
        await send_cancel_lesson_email(lesson, user)
        return await sync_to_async(HttpResponseRedirect)(
            reverse_lazy('schedule:lesson_cancel_success'),
        )
    return await sync_to_async(render)(
        request,
        'schedule_cancel_lesson.html',
    )


def lesson_change_success(request):
    new_datetime = request.GET.get('new_datetime')
    return render(
        request, 'lesson_change_success.html',
        context={'new_datetime': new_datetime},
    )


def lesson_cancel_success(request):
    return render(request, 'lesson_cancel_success.html')
