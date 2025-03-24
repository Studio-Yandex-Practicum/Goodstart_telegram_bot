from django.core.exceptions import ValidationError

def validate_file_size(value):
    max_size_mb = 10
    if value.size > max_size_mb * 1024 * 1024:
        raise ValidationError(
            f'Размер файла не должен превышать {max_size_mb} МБ.',
        )
