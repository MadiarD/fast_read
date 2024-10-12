# Generated by Django 5.1.2 on 2024-10-11 20:19

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('fast_read_app', '0005_rename_test_block_tests'),
    ]

    operations = [
        migrations.CreateModel(
            name='ClientResult',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('speed', models.FloatField(verbose_name='Скорость')),
                ('correct_answers', models.IntegerField(verbose_name='Количество правильных ответов')),
                ('count', models.IntegerField(verbose_name='Количество вопросов')),
                ('percent', models.FloatField(verbose_name='Процент правильных ответов')),
                ('tel_number', models.CharField(max_length=12, verbose_name='Номер телефона')),
                ('send_message', models.BooleanField(default=False, verbose_name='Отправлено сообщение')),
                ('text', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='results', to='fast_read_app.text', verbose_name='Текст')),
            ],
            options={
                'verbose_name': 'Результат',
                'verbose_name_plural': 'Результаты',
            },
        ),
    ]
