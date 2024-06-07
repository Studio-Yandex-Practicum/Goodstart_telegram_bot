# Generated by Django 5.0.6 on 2024-06-07 15:15

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('schooling', '0006_merge_20240607_1417'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='lesson',
            options={'verbose_name': 'занятие', 'verbose_name_plural': 'Занятия'},
        ),
        migrations.AlterModelOptions(
            name='student',
            options={'verbose_name': 'студент', 'verbose_name_plural': 'Студенты'},
        ),
        migrations.AlterModelOptions(
            name='studyclass',
            options={'verbose_name': 'учебный класс', 'verbose_name_plural': 'Учебные классы'},
        ),
        migrations.AlterModelOptions(
            name='subject',
            options={'verbose_name': 'название предмета', 'verbose_name_plural': 'Названия предметов'},
        ),
        migrations.AlterModelOptions(
            name='teacher',
            options={'verbose_name': 'преподаватель', 'verbose_name_plural': 'Преподаватели'},
        ),
        migrations.AlterField(
            model_name='lesson',
            name='student_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='lessons', to='schooling.student', verbose_name='Студент'),
        ),
        migrations.AlterField(
            model_name='lesson',
            name='teacher_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='lessons', to='schooling.teacher', verbose_name='Преподаватель'),
        ),
    ]