from typing import Sequence
from django.db.models import Model

from potential_user.models import ApplicationForm
from schooling.models import Student


async def check_user_from_db(
    telegram_id: int,
    from_models: Sequence[Model],
) -> Model:
    """
    Check user from database by `telegram_id` field.

    Args:
    ----
        telegram_id (int): The Telegram ID of the user to search for.
        from_models (list[Model]): A list of Django models to search for
        the user in.

    Returns:
    -------
        Model: The user object if found, otherwise `None`.

    """
    for model in from_models:
        try:
            user = await model.objects.aget(telegram_id=telegram_id)
            return user
        except model.DoesNotExist:
            continue
    return None


async def check_user_application_exists(
    telegram_id: int,
) -> bool:
    return await ApplicationForm.objects.filter(
        telegram_id=telegram_id,
    ).aexists()


async def end_paid_message(context):
    """

    Проверяет учащихся, отправляет уведомление
    об окончании оплаченных занятий.
    """
    students = Student.objects.filter(paid_lessons__lte=2)
    async for student in students:
        if student.paid_lessons == 0:
            await context.bot.send_message(
                chat_id=student.telegram_id,
                text='Необходимо внести оплату за обучение!',
            )
        else:
            await context.bot.send_message(
                chat_id=student.telegram_id,
                text=f'Осталось оплаченных занятий: {student.paid_lessons}.',
            )
