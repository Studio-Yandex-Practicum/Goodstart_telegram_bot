# Generated by Django 5.0.7 on 2024-07-31 17:17

import phonenumber_field.modelfields
import schooling.validator
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('schooling', '0008_alter_student_phone_number_alter_student_state_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='student',
            name='phone_number',
            field=phonenumber_field.modelfields.PhoneNumberField(help_text='Формат +7XXXXXXXXXX', max_length=128, region=None, validators=[schooling.validator.validate_phone_number], verbose_name='Номер телефона'),
        ),
        migrations.AlterField(
            model_name='teacher',
            name='phone_number',
            field=phonenumber_field.modelfields.PhoneNumberField(help_text='Формат +7XXXXXXXXXX', max_length=128, region=None, validators=[schooling.validator.validate_phone_number], verbose_name='Номер телефона'),
        ),
    ]
