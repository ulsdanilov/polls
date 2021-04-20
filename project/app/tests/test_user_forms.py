from django.contrib.auth.models import User
from django.urls import reverse
from django.utils import timezone
from rest_framework import status
from rest_framework.test import APITransactionTestCase

from project.app.models import (Choice, Poll, Question, Session, UserAnswer,
                                UserForm)
from project.app.serializers import UserFormSerializer


class UserFormCreateViewTests(APITransactionTestCase):
    """
    Проверка прохождения опроса
    """

    def test_create_valid_user_form_from_user(self):
        """
        Прохождение опроса пользователем c валидными данными
        """
        self.poll = Poll.objects.create(
            title='test_poll',
            description='test_description',
            start_date=timezone.now(),
            end_date=timezone.now()
        )
        self.question = Question.objects.create(
            poll=self.poll,
            text='test_text',
            question_type='SINGLE'
        )
        self.choice = Choice.objects.create(
            question=self.question,
            title='test_title'
        )

        response = self.client.post(
            reverse('app:user_form-create'),
            format='json',
            data = {
                'poll': self.poll.pk,
                'phone_number': '89999999999',
                'email': 'test_email@example.com',
                'user_answers': [
                    {
                        'question': self.question.pk,
                        'choices': [self.choice.pk],
                        'custom_answer': ''
                    }
                ]
            }
        )

        user_form_id = response.data['pk']
        user_form = UserForm.objects.get(pk=user_form_id)
        serializer = UserFormSerializer(user_form)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_invalid_single_choice_from_user(self):
        """
        Прохождение опроса пользователем c невалидным одиночным ответом
        """
        self.poll = Poll.objects.create(
            title='test_poll',
            description='test_description',
            start_date=timezone.now(),
            end_date=timezone.now()
        )
        self.question = Question.objects.create(
            poll=self.poll,
            text='test_text',
            question_type='SINGLE'
        )
        self.choice = Choice.objects.create(
            question=self.question,
            title='test_title'
        )

        response = self.client.post(
            reverse('app:user_form-create'),
            format='json',
            data = {
                'poll': self.poll.pk,
                'phone_number': '89999999999',
                'email': 'test_email@example.com',
                'user_answers': [
                    {
                        'question': self.question.pk,
                        'choices': [],
                        'custom_answer': ''
                    }
                ]
            }
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_invalid_multiple_choice_from_user(self):
        """
        Прохождение опроса пользователем c невалидным множественным ответом
        """
        self.poll = Poll.objects.create(
            title='test_poll',
            description='test_description',
            start_date=timezone.now(),
            end_date=timezone.now()
        )
        self.question = Question.objects.create(
            poll=self.poll,
            text='test_text',
            question_type='MULTIPLE'
        )
        self.first_choice = Choice.objects.create(
            question=self.question,
            title='test_first_title'
        )
        self.second_choice = Choice.objects.create(
            question=self.question,
            title='test_second_title'
        )

        response = self.client.post(
            reverse('app:user_form-create'),
            format='json',
            data = {
                'poll': self.poll.pk,
                'phone_number': '89999999999',
                'email': 'test_email@example.com',
                'user_answers': [
                    {
                        'question': self.question.pk,
                        'choices': [],
                        'custom_answer': ''
                    }
                ]
            }
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_invalid_custom_answer_from_user(self):
        """
        Прохождение опроса пользователем c невалидным текстовым ответом
        """
        self.poll = Poll.objects.create(
            title='test_poll',
            description='test_description',
            start_date=timezone.now(),
            end_date=timezone.now()
        )
        self.question = Question.objects.create(
            poll=self.poll,
            text='test_text',
            question_type='CUSTOM'
        )

        response = self.client.post(
            reverse('app:user_form-create'),
            format='json',
            data = {
                'poll': self.poll.pk,
                'phone_number': '89999999999',
                'email': 'test_email@example.com',
                'user_answers': [
                    {
                        'question': self.question.pk,
                        'choices': [],
                        'custom_answer': ''
                    }
                ]
            }
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class UserFormListViewTests(APITransactionTestCase):
    """
    Проверка получения списка пройденных опросов
    """

    def test_get_all_user_forms_from_admin(self):
        """
        Получение списка списка пройденных опросов администратором
        """
        self.superuser = User.objects.create_superuser(
            username='test_superuser',
            email='test@example.com',
            password='test_password',
        )
        self.poll = Poll.objects.create(
            title='test_poll',
            description='test_description',
            start_date=timezone.now(),
            end_date=timezone.now()
        )
        self.question = Question.objects.create(
            poll=self.poll,
            text='test_text',
            question_type='SINGLE'
        )
        self.choice = Choice.objects.create(
            question=self.question,
            title='test_title'
        )
        self.session = Session.objects.get(
            session_key=self.client.session.session_key
        )
        self.user_form = UserForm.objects.create(
            user=self.session,
            poll=self.poll
        )
        self.user_answer = UserAnswer.objects.create(
            user_form=self.user_form,
            question=self.question
        )
        self.user_answer.choices.add(self.choice)

        self.client.force_authenticate(user=self.superuser)

        response = self.client.get(reverse('app:user_form-list'))
        user_forms = UserForm.objects.all()
        serializer = UserFormSerializer(user_forms, many=True)
        self.assertEqual(response.data['results'], serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_all_user_forms_from_user(self):
        """
        Получение списка списка пройденных опросов пользователем
        """
        self.poll = Poll.objects.create(
            title='test_poll',
            description='test_description',
            start_date=timezone.now(),
            end_date=timezone.now()
        )
        self.question = Question.objects.create(
            poll=self.poll,
            text='test_text',
            question_type='SINGLE'
        )
        self.choice = Choice.objects.create(
            question=self.question,
            title='test_title'
        )
        self.session = Session.objects.get(
            session_key=self.client.session.session_key
        )
        self.user_form = UserForm.objects.create(
            user=self.session,
            poll=self.poll
        )
        self.user_answer = UserAnswer.objects.create(
            user_form=self.user_form,
            question=self.question
        )
        self.user_answer.choices.add(self.choice)

        response = self.client.get(reverse('app:user_form-list'))
        user_forms = UserForm.objects.filter(user=self.client.session.session_key)
        serializer = UserFormSerializer(user_forms, many=True)
        self.assertEqual(response.data['results'], serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
