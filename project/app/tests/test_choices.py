from django.contrib.auth.models import User
from django.urls import reverse
from django.utils import timezone
from rest_framework import status
from rest_framework.test import APITransactionTestCase

from project.app.models import Choice, Poll, Question
from project.app.serializers import ChoiceSerializer


class ChoiceCreateViewTests(APITransactionTestCase):
    """
    Проверка создания варианта ответа к вопросу
    """

    def test_create_choice_from_admin(self):
        """
        Создание варианта ответа к вопросу администратором
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

        self.client.force_authenticate(user=self.superuser)

        response = self.client.post(
            reverse('app:choice-create'),
            data = {
                'question': self.question.pk,
                'title': 'test_choice'
            }
        )

        choice_id = response.data['pk']
        choice = Choice.objects.get(pk=choice_id)
        serializer = ChoiceSerializer(choice)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_choice_from_user(self):
        """
        Создание варианта ответа к вопросу пользователем
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

        response = self.client.post(
            reverse('app:choice-create'),
            data = {
                'question': self.question.pk,
                'title': 'test_choice'
            }
        )

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class ChoiceListViewTests(APITransactionTestCase):
    """
    Проверка получения списка вариантов ответа к вопросу
    """

    def test_get_all_choices_from_admin(self):
        """
        Получение списка вариантов ответа к вопросу администратором
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

        self.client.force_authenticate(user=self.superuser)

        response = self.client.get(reverse('app:choice-list'))
        choices = Choice.objects.all()
        serializer = ChoiceSerializer(choices, many=True)
        self.assertEqual(response.data['results'], serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_all_choices_from_user(self):
        """
        Получение списка вариантов ответа к вопросу пользователем
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

        response = self.client.get(reverse('app:choice-list'))
        choices = Choice.objects.all()
        serializer = ChoiceSerializer(choices, many=True)
        self.assertEqual(response.data['results'], serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class ChoiceDetailViewTests(APITransactionTestCase):
    """
    Проверка получения, обновления и удаления варианта ответа к вопросу по ID
    """

    def test_get_choice_from_admin(self):
        """
        Получение варианта ответа к вопросу по ID администратором
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

        self.client.force_authenticate(user=self.superuser)

        response = self.client.get(
            reverse(
                'app:choice-detail',
                kwargs={'pk': self.choice.pk}
            )
        )

        choice = Choice.objects.get(id=self.choice.pk)
        serializer = ChoiceSerializer(choice)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_choice_from_user(self):
        """
        Получение варианта ответа к вопросу по ID пользователем
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

        response = self.client.get(
            reverse(
                'app:choice-detail',
                kwargs={'pk': self.choice.pk}
            )
        )

        choice = Choice.objects.get(id=self.choice.pk)
        serializer = ChoiceSerializer(choice)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update_choice_from_admin(self):
        """
        Обновление варианта ответа к вопросу по ID администратором
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

        self.client.force_authenticate(user=self.superuser)

        response = self.client.patch(
            reverse('app:choice-detail', kwargs={'pk': self.choice.pk}),
            data={'title': 'updated_test_title'}
        )

        chioce = Choice.objects.get(id=self.choice.pk)
        serializer = ChoiceSerializer(chioce)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update_choice_from_user(self):
        """
        Обновление варианта ответа к вопросу по ID пользователем
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

        response = self.client.patch(
            reverse('app:choice-detail', kwargs={'pk': self.choice.pk}),
            data={'title': 'updated_test_title'}
        )

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_delete_choice_from_admin(self):
        """
        Удаление варианта ответа к вопросу по ID администратором
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

        self.client.force_authenticate(user=self.superuser)

        response = self.client.delete(
            reverse(
                'app:choice-detail',
                kwargs={'pk': self.choice.pk}
            )
        )

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_delete_choice_from_user(self):
        """
        Удаление варианта ответа к вопросу по ID пользователем
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

        response = self.client.delete(
            reverse(
                'app:choice-detail',
                kwargs={'pk': self.choice.pk}
            )
        )

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
