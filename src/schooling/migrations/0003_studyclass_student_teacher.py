# Generated by Django 5.0.6 on 2024-05-13 09:16

import django.db.models.deletion
import phonenumber_field.modelfields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('schooling', '0002_add_subject'),
    ]

    operations = [
        migrations.CreateModel(
            name='StudyClass',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
        migrations.CreateModel(
            name='Student',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('telegram_id', models.IntegerField(unique=True, verbose_name='Telegram ID')),
                ('name', models.CharField(max_length=150, verbose_name='Имя')),
                ('surname', models.CharField(max_length=150, verbose_name='Фамилия')),
                ('city', models.CharField(max_length=50, verbose_name='Город')),
                ('phone_number', phonenumber_field.modelfields.PhoneNumberField(max_length=128, region=None, verbose_name='Номер телефона')),
                ('last_login_date', models.DateField(auto_now=True, verbose_name='Последнее посещение')),
                ('registration_date', models.DateField(auto_now_add=True, verbose_name='Дата регистрации')),
                ('paid_lessons', models.PositiveIntegerField(verbose_name='Оплаченые занятия')),
                ('parents_contacts', models.CharField(verbose_name='Контакты представителей')),
                ('subjects', models.ManyToManyField(to='schooling.subject', verbose_name='Предмет')),
                ('study_class_id', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='students', to='schooling.studyclass', verbose_name='ID учебного класса')),
            ],
            options={
                'verbose_name': 'Студент',
                'verbose_name_plural': 'Студенты',
            },
        ),
        migrations.CreateModel(
            name='Teacher',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('telegram_id', models.IntegerField(unique=True, verbose_name='Telegram ID')),
                ('name', models.CharField(max_length=150, verbose_name='Имя')),
                ('surname', models.CharField(max_length=150, verbose_name='Фамилия')),
                ('city', models.CharField(max_length=50, verbose_name='Город')),
                ('phone_number', phonenumber_field.modelfields.PhoneNumberField(max_length=128, region=None, verbose_name='Номер телефона')),
                ('last_login_date', models.DateField(auto_now=True, verbose_name='Последнее посещение')),
                ('registration_date', models.DateField(auto_now_add=True, verbose_name='Дата регистрации')),
                ('competence', models.ManyToManyField(to='schooling.subject', verbose_name='Предмет')),
                ('study_classes', models.ManyToManyField(to='schooling.studyclass', verbose_name='Учебный класс')),
            ],
            options={
                'verbose_name': 'Преподаватель',
                'verbose_name_plural': 'Преподаватели',
            },
        ),
    ]