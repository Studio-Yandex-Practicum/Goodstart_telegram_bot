# Generated by Django 5.0.7 on 2024-08-06 08:09

import phonenumber_field.modelfields
import schooling.validators.phone_validators
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('admin_user', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='administrator',
            name='phone',
            field=phonenumber_field.modelfields.PhoneNumberField(help_text='Формат +7XXXXXXXXXX', max_length=128, region=None, validators=[schooling.validators.phone_validators.validate_phone_number], verbose_name='Номер телефона.'),
        ),
    ]
