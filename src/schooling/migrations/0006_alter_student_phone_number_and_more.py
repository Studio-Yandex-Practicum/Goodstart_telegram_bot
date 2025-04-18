# Generated by Django 5.0.4 on 2025-02-16 18:41

import phonenumber_field.modelfields
import schooling.validators.phone_validators
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('schooling', '0005_alter_student_options_alter_teacher_options_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='student',
            name='phone_number',
            field=phonenumber_field.modelfields.PhoneNumberField(help_text='Формат +7XXXXXXXXXX', max_length=128, region='RU', validators=[schooling.validators.phone_validators.validate_phone_number], verbose_name='Номер телефона'),
        ),
        migrations.AlterField(
            model_name='teacher',
            name='phone_number',
            field=phonenumber_field.modelfields.PhoneNumberField(help_text='Формат +7XXXXXXXXXX', max_length=128, region='RU', validators=[schooling.validators.phone_validators.validate_phone_number], verbose_name='Номер телефона'),
        ),
    ]
