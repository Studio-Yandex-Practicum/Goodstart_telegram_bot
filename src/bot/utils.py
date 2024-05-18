from typing import Sequence

from django.db.models import Model


async def check_user_from_db(
    telegram_id: int,
    from_models: Sequence[Model],
) -> Model:
    """Check user from database by `telegram_id` field.

    Args:
        telegram_id (int): The Telegram ID of the user to search for.
        from_models (list[Model]): A list of Django models to search for
        the user in.

    Returns:
        Model: The user object if found, otherwise `None`.
    """
    for model in from_models:
        try:
            user = await model.objects.aget(telegram_id=telegram_id)
            return user
        except model.DoesNotExist:
            continue
    return None
