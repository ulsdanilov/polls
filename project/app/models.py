from django.contrib.sessions.models import Session
from django.db import models


class Poll(models.Model):
    title = models.CharField(max_length=4096, unique=True, null=False, verbose_name='Название опроса')
    description = models.CharField(max_length=4096, verbose_name='Описание опроса')
    start_date = models.DateTimeField(verbose_name='Дата начала опроса')
    end_date = models.DateTimeField(verbose_name='Дата окончания опроса')

    def __str__(self):
        return self.title


class Question(models.Model):

    class QuestionType:
        CUSTOM = 'CUSTOM'
        SINGLE = 'SINGLE'
        MULTIPLE = 'MULTIPLE'

        choices = (
            (CUSTOM, 'CUSTOM'),
            (SINGLE, 'SINGLE'),
            (MULTIPLE, 'MULTIPLE'),
        )

    poll = models.ForeignKey(Poll, related_name='poll_questions', on_delete=models.CASCADE, verbose_name='Название опроса')
    text = models.CharField(max_length=4096, unique=True, null=False, verbose_name='Текст вопроса')
    question_type = models.CharField(max_length=8, choices=QuestionType.choices, default=QuestionType.SINGLE)

    def __str__(self):
        return self.text


class Choice(models.Model):
    question = models.ForeignKey(Question, related_name='question_choices', on_delete=models.CASCADE, verbose_name='Название вопроса')
    title = models.CharField(max_length=4096, unique=True, null=False, verbose_name='Вариант ответа')

    def __str__(self):
        return self.title


class UserForm(models.Model):
    user = models.ForeignKey(Session, on_delete=models.CASCADE, verbose_name='Идентификатор сессии пользователя')
    poll = models.ForeignKey(Poll, on_delete=models.CASCADE, verbose_name='Название опроса')
    phone_number = models.CharField(max_length=11, null=True, blank=True, verbose_name='Номер телефона пользователя')
    email = models.EmailField(null=True, verbose_name='Электронная почта пользователя')
    create_datetime = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')

    def __str__(self):
        return self.user.pk


class UserAnswer(models.Model):
    user_form = models.ForeignKey(UserForm, related_name='user_answers', on_delete=models.CASCADE, verbose_name='Анкета пользователя')
    question = models.ForeignKey(Question, on_delete=models.CASCADE, verbose_name='Название вопроса')
    choices = models.ManyToManyField(Choice, related_name='user_choices', blank=True, verbose_name='Варианты ответа пользователя')
    custom_answer = models.CharField(max_length=1024, blank=True, null=True, verbose_name='Текстовый ответ пользователя')

    def __str__(self):
        return self.user_form.poll.title
