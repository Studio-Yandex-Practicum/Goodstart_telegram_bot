import datetime

from django.shortcuts import render, redirect
from asgiref.sync import sync_to_async
from django.conf import settings
from django.http import HttpResponseBadRequest
from django.urls import reverse

from schooling.models import Teacher, Student, Lesson
from schooling.signals_bot import (
    get_schedule_for_role, get_schedule_week_tasks,
)
from bot.utils import check_user_from_db

from .forms import PaymentForm

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


def payment_view(request):
    if request.method == 'POST':
        form = PaymentForm(request.POST)
        if form.is_valid():
            try:
                lessons = int(form.cleaned_data['number_of_lessons'])
                return redirect(reverse('payment_summary',
                                        kwargs={'lessons': lessons}))
            except ValueError:
                return HttpResponseBadRequest(
                    'Некорректное значение количества занятий.')
    else:
        form = PaymentForm()

    return render(request, 'payment_page.html', {'form': form})

def payment_summary_view(request, lessons):
    try:
        lessons = int(lessons)
        if lessons < 1 or lessons > 10:
            return HttpResponseBadRequest('Некорректное количество занятий.')

        total_price = lessons * 100
        payment_url = (
            f'https://example.com/pay?amount={total_price}'
            f'&lessons={lessons}'
        )

        return render(request, 'payment_summary.html', {
            'lessons': lessons,
            'total_price': total_price,
            'payment_url': payment_url,
        })

    except ValueError:
        return HttpResponseBadRequest('Ошибка обработки запроса.')
