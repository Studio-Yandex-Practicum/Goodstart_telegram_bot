# Generated by Django 5.0.6 on 2024-06-29 12:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('schooling', '0006_alter_lesson_duration'),
    ]

    operations = [
        migrations.AlterField(
            model_name='lesson',
            name='test_lesson',
            field=models.BooleanField(default=False, verbose_name='Пробное занятие'),
        ),
    ]
