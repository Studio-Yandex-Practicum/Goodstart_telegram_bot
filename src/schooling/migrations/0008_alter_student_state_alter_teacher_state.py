# Generated by Django 5.0.7 on 2024-08-05 13:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('schooling', '0007_alter_lesson_test_lesson'),
    ]

    operations = [
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
