# Generated by Django 5.0.7 on 2024-08-11 13:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('schooling', '0007_alter_lesson_test_lesson'),
    ]

    operations = [
        migrations.AddField(
            model_name='lesson',
            name='is_passed_student',
            field=models.BooleanField(default=None, verbose_name='Занятие подтверждено учеником'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='lesson',
            name='is_passed_teacher',
            field=models.BooleanField(default=None, verbose_name='Занятие подтверждено учителем'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='student',
            name='state',
            field=models.CharField(choices=[('start', 'Start'), ('help', 'Help'), ('schedule', 'Schedule'), ('feedback', 'Feedback'), ('feedback_subject_msg', 'Feedback Subject'), ('feedback_body_msg', 'Feedback Body'), ('left_lessons', 'Left Lessons')], default='start', max_length=50, verbose_name='Состояние пользователя'),
        ),
        migrations.AlterField(
            model_name='teacher',
            name='state',
            field=models.CharField(choices=[('start', 'Start'), ('help', 'Help'), ('schedule', 'Schedule'), ('feedback', 'Feedback'), ('feedback_subject_msg', 'Feedback Subject'), ('feedback_body_msg', 'Feedback Body'), ('left_lessons', 'Left Lessons')], default='start', max_length=50, verbose_name='Состояние пользователя'),
        ),
    ]
