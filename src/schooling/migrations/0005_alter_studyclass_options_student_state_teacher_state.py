# Generated by Django 5.0.6 on 2024-06-04 14:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('schooling', '0004_alter_student_paid_lessons_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='studyclass',
            options={'verbose_name': 'Учебный класс', 'verbose_name_plural': 'Учебные классы'},
        ),
        migrations.AddField(
            model_name='student',
            name='state',
            field=models.CharField(choices=[('start', 'Start'), ('help', 'Help'), ('schedule', 'Schedule')], default='start', max_length=50, verbose_name='Состояние пользователя'),
        ),
        migrations.AddField(
            model_name='teacher',
            name='state',
            field=models.CharField(choices=[('start', 'Start'), ('help', 'Help'), ('schedule', 'Schedule')], default='start', max_length=50, verbose_name='Состояние пользователя'),
        ),
    ]