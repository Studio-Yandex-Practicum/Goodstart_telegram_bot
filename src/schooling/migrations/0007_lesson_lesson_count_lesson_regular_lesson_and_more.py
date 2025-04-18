# Generated by Django 5.0.4 on 2025-02-18 16:52

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('schooling', '0006_alter_student_phone_number_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='lesson',
            name='lesson_count',
            field=models.PositiveIntegerField(default=1, help_text='Сколько занятий создать', verbose_name='Количество создаваемых занятий'),
        ),
        migrations.AddField(
            model_name='lesson',
            name='regular_lesson',
            field=models.BooleanField(default=False, verbose_name='Регулярное занятие'),
        ),
        migrations.CreateModel(
            name='LessonGroup',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')),
                ('student', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='lesson_groups', to='schooling.student', verbose_name='Студент')),
            ],
            options={
                'verbose_name': 'группа занятий',
                'verbose_name_plural': 'Группы занятий',
            },
        ),
        migrations.AddField(
            model_name='lesson',
            name='group',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='lessons', to='schooling.lessongroup', verbose_name='Группа занятий'),
        ),
    ]
