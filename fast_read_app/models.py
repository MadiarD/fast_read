from django.db import models

class Text(models.Model):
    name = models.CharField(max_length= 256, verbose_name='Название текста')
    class Meta:
        verbose_name = 'Текст'
        verbose_name_plural = 'Тексты'

    def __str__(self):
        return self.name

class Block(models.Model):
    no = models.IntegerField(verbose_name='Номер блока', null=True, blank=True, default=None)
    main_text = models.ForeignKey('Text', on_delete=models.CASCADE, related_name='blocks', verbose_name='Название текста', null=True, blank=True, default=None)  
    text = models.TextField(verbose_name='Текст блока')
    tests = models.ManyToManyField('Quetions', related_name='blocks', verbose_name='Вопросы')
    class Meta:
        verbose_name = 'Блок'
        verbose_name_plural = 'Блоки'
    def __str__(self):
        return self.text

class Quetions(models.Model):
    quetion = models.TextField(verbose_name='Вопрос')
    answers = models.ManyToManyField('Answer', related_name='tests', verbose_name='Ответы')
    class Meta:
        verbose_name = 'Тест'
        verbose_name_plural = 'Тесты'
    def __str__(self):
        return self.quetion

class Answer(models.Model):
    answer_text = models.CharField(max_length=256, blank=True, null=True, verbose_name='Ответ')
    is_valid = models.BooleanField(default=False, verbose_name='Верный ответ')
    class Meta:
        verbose_name = 'Вопрос'
        verbose_name_plural = 'Вопросы'
    def __str__(self):
        return self.answer_text 

class ClientResult(models.Model):
    text = models.ForeignKey('Text', on_delete=models.CASCADE, related_name='results', verbose_name='Текст')
    speed = models.FloatField(verbose_name='Скорость')
    correct_answers = models.IntegerField(verbose_name='Количество правильных ответов')
    count = models.IntegerField(verbose_name='Количество вопросов')
    percent = models.FloatField(verbose_name='Процент правильных ответов')
    tel_number = models.CharField(max_length=12, verbose_name='Номер телефона')
    send_message = models.BooleanField(default=False, verbose_name='Отправлено сообщение')
    class Meta:
        verbose_name = 'Результат'
        verbose_name_plural = 'Результаты'
    def __str__(self):
        return self.text.name
    
class WhatsappMessage(models.Model):
    text = models.TextField(verbose_name='Текст сообщения')
    is_default = models.BooleanField(default=False, verbose_name='Стандартное сообщение')
    class Meta:
        verbose_name = 'Сообщение'
        verbose_name_plural = 'Сообщения'
    def __str__(self):
        return self.text