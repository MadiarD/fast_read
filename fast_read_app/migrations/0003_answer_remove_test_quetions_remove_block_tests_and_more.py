# Generated by Django 5.1.2 on 2024-10-11 19:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('fast_read_app', '0002_alter_text_blocks'),
    ]

    operations = [
        migrations.CreateModel(
            name='Answer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('answer_text', models.CharField(blank=True, max_length=256, null=True, verbose_name='Вопрос')),
                ('is_valid', models.BooleanField(default=False, verbose_name='Верный ответ')),
            ],
            options={
                'verbose_name': 'Вопрос',
                'verbose_name_plural': 'Вопросы',
            },
        ),
        migrations.RemoveField(
            model_name='test',
            name='quetions',
        ),
        migrations.RemoveField(
            model_name='block',
            name='tests',
        ),
        migrations.CreateModel(
            name='Quetions',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quetion', models.TextField(verbose_name='Вопрос')),
                ('answers', models.ManyToManyField(related_name='tests', to='fast_read_app.answer', verbose_name='Отыеты')),
            ],
            options={
                'verbose_name': 'Тест',
                'verbose_name_plural': 'Тесты',
            },
        ),
        migrations.AddField(
            model_name='block',
            name='test',
            field=models.ManyToManyField(related_name='blocks', to='fast_read_app.quetions', verbose_name='Вопросы'),
        ),
        migrations.DeleteModel(
            name='Quetion',
        ),
        migrations.DeleteModel(
            name='Test',
        ),
    ]
