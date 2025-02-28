import asyncio
import datetime

from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponseForbidden
from asgiref.sync import sync_to_async
from django.conf import settings

from schooling.models import (Teacher, Student, Lesson, HomeworkImage,
                              HomeworkFile)
from schooling.forms import HomeworkForm
from schooling.signals_bot import (
    get_schedule_for_role, get_schedule_week_tasks, send_message_to_user,
    get_homework_update_message)
from bot.utils import check_user_from_db


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


def edit_homework(request, id, lesson_id):
    """Редактирование домашнего задания преподавателем."""
    lesson = get_object_or_404(Lesson, id=lesson_id)

    if lesson.teacher_id.telegram_id != id:
        return HttpResponseForbidden('Вы не можете редактировать это занятие!')

    if request.method == 'POST':
        form = HomeworkForm(request.POST, request.FILES, instance=lesson)
        if form.is_valid():
            form.save()

            for image in request.FILES.getlist('images'):
                HomeworkImage.objects.create(lesson=lesson, image=image)

            for file in request.FILES.getlist('files'):
                HomeworkFile.objects.create(lesson=lesson, file=file)

            if lesson.student_id:
                student_tg_id = lesson.student_id.telegram_id
                message = asyncio.run(get_homework_update_message(lesson))
                asyncio.run(send_message_to_user(
                    settings.TELEGRAM_TOKEN, student_tg_id, message))

            return redirect(
                'schedule:details_schedule',
                id=id,
                lesson_id=lesson.id,
            )

    else:
        form = HomeworkForm(instance=lesson)

    context = {
        'form': form,
        'lesson': lesson,
        'user_tg_id': id,
        'homework_images': lesson.homework_images.all(),
        'homework_files': lesson.homework_files.all(),
    }

    return render(request, 'edit_homework.html', context)


def delete_homework_image(request, id, lesson_id, image_id):
    """Удаление изображения домашнего задания только преподавателем."""
    image = get_object_or_404(HomeworkImage, id=image_id, lesson_id=lesson_id)

    if image.lesson.teacher_id.telegram_id != id:
        return HttpResponseForbidden(
            'Вы не можете удалять файлы в этом занятии.')
    image.delete()
    return redirect('schedule:edit_homework', id=id, lesson_id=lesson_id)


def delete_homework_file(request, id, lesson_id, file_id):
    """Удаление файла домашнего задания только преподавателем."""
    file = get_object_or_404(HomeworkFile, id=file_id, lesson_id=lesson_id)

    if file.lesson.teacher_id.telegram_id != id:
        return HttpResponseForbidden(
            'Вы не можете удалять файлы в этом занятии.')

    file.delete()
    return redirect('schedule:edit_homework', id=id, lesson_id=lesson_id)
