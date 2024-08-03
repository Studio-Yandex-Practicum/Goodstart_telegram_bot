from django.core.exceptions import ValidationError
from phonenumbers import (NumberParseException, is_possible_number,
                          is_valid_number, parse)
from phonenumbers.phonenumberutil import region_code_for_number


def validate_phone_number(value):
    """Валидация телефонного номера."""
    try:
        phone_number = parse(value, 'RU')
    except NumberParseException:
        raise ValidationError('Номер телефона некорректен или отсутствует.')

    if not is_valid_number(phone_number):
        raise ValidationError('Номер телефона невалиден.')
    if not is_possible_number(phone_number):
        raise ValidationError('Невозможный номер телефона.')
    region_code = region_code_for_number(phone_number)
    if region_code != 'RU':
        raise ValidationError('Номер телефона должен быть из России!')
