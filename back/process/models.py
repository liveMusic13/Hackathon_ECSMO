from django.db import models


class Question(models.Model):
    created = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Время создания',
    )
    audio_name_id = models.CharField(
        max_length=255,
        help_text='Имя аудиофайла вопроса пользователя',
        verbose_name='Имя',
    )
    text = models.TextField(
        verbose_name='Текст вопроса',
    )

    class Meta:
        verbose_name = 'Вопрос'
        verbose_name_plural = 'Вопросы'

    def __str__(self) -> str:
        return f'{self.__class__.__name__} - {self.audio_name_id}'


class Answer(models.Model):
    created = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Время создания',
    )
    audio_full_path = models.TextField(
        help_text='Путь до файла аудиозаписи ответа персонажа',
        verbose_name='Аудиофайл',
    )
    topic = models.CharField(
        max_length=128,
        verbose_name='Тема вопроса',
    )
    emotion = models.CharField(
        max_length=64,
        verbose_name='Эмоция ответа',
    )
    text = models.TextField(
        verbose_name='Текст ответа',
    )
    question = models.OneToOneField(
        to=Question,
        on_delete=models.CASCADE,
        related_name='to_question',
        verbose_name='Вопрос'
    )

    class Meta:
        verbose_name = 'Ответ'
        verbose_name_plural = 'Ответы'

    def __str__(self) -> str:
        return f'{self.__class__.__name__} - {self.audio_full_path}'
