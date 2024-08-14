# Generated by Django 5.0.4 on 2024-08-13 10:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('schooling', '0009_alter_student_phone_number_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='lesson',
            name='is_passed_student',
            field=models.BooleanField(default=False, verbose_name='Занятие подтверждено учеником'),
        ),
        migrations.AddField(
            model_name='lesson',
            name='is_passed_teacher',
            field=models.BooleanField(default=False, verbose_name='Занятие подтверждено учителем'),
        ),
    ]
