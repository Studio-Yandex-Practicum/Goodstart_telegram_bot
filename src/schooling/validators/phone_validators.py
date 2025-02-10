from django.core.exceptions import ValidationError
from phonenumbers import (NumberParseException, is_possible_number,
                          is_valid_number, parse)
from phonenumbers.phonenumberutil import region_code_for_number


def validate_phone_number(value):
    """Валидация телефонного номера."""
    try:
        phone_number = parse(value, 'RU')
    except NumberParseException as err:
        raise ValidationError(
            'Номер телефона некорректен или отсутствует.') from err

    try:
        if not is_valid_number(phone_number):
            raise ValidationError('Номер телефона невалиден.')
        if not is_possible_number(phone_number):
            raise ValidationError('Невозможный номер телефона.')
        if region_code_for_number(phone_number) != 'RU':
            raise ValidationError('Номер телефона должен быть из России!')
    except ValidationError as err:
        raise ValidationError('Ошибка валидации номера телефона.') from err
