from datetime import timedelta

from django.contrib.auth.models import User
from django.urls import reverse
from django.utils import timezone
from rest_framework import status
from rest_framework.test import APITransactionTestCase

from project.app.models import Poll
from project.app.serializers import PollSerializer


class PollCreateViewTests(APITransactionTestCase):
    """
    Проверка создания опроса
    """

    def test_create_poll_from_admin(self):
        """
        Создание опроса администратором
        """
        self.superuser = User.objects.create_superuser(
            username='test_superuser',
            email='test@example.com',
            password='test_password',
        )

        self.client.force_authenticate(user=self.superuser)

        response = self.client.post(
            reverse('app:poll-create'),
            data = {
                'title': 'test_poll',
                'description': 'test_description',
                'start_date': timezone.now(),
                'end_date': timezone.now()
            }
        )

        poll_id = response.data['pk']
        poll = Poll.objects.get(pk=poll_id)
        serializer = PollSerializer(poll)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_poll_from_user(self):
        """
        Создание опроса пользователем
        """
        response = self.client.post(
            reverse('app:poll-create'),
            data = {
                'title': 'test_poll',
                'description': 'test_description',
                'start_date': timezone.now(),
                'end_date': timezone.now()
            }
        )

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class PollListViewTests(APITransactionTestCase):
    """
    Проверка получения списка опросов
    """

    def test_get_all_polls_from_admin(self):
        """
        Получение списка опросов администратором
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

        self.client.force_authenticate(user=self.superuser)

        response = self.client.get(reverse('app:poll-list'))
        polls = Poll.objects.all()
        serializer = PollSerializer(polls, many=True)
        self.assertEqual(response.data['results'], serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_all_active_polls_from_user(self):
        """
        Получение списка активных опросов пользователем
        """
        self.poll = Poll.objects.create(
            title='test_poll',
            description='test_description',
            start_date=timezone.now(),
            end_date=timezone.now() + timedelta(days=1)
        )

        response = self.client.get(reverse('app:poll-list'))
        polls = Poll.objects.all()
        serializer = PollSerializer(polls, many=True)
        self.assertEqual(response.data['results'], serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_all_inactive_polls_from_user(self):
        """
        Получение списка неактивных опросов пользователем
        """
        self.poll = Poll.objects.create(
            title='test_poll',
            description='test_description',
            start_date=timezone.now(),
            end_date=timezone.now()
        )

        response = self.client.get(reverse('app:poll-list'))
        self.assertEqual(response.data['results'], [])
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class PollDetailViewTests(APITransactionTestCase):
    """
    Проверка получения, обновления и удаления опроса по ID
    """

    def test_get_poll_from_admin(self):
        """
        Получение опроса по ID администратором
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

        self.client.force_authenticate(user=self.superuser)

        response = self.client.get(
            reverse(
                'app:poll-detail',
                kwargs={'pk': self.poll.pk}
            )
        )

        poll = Poll.objects.get(id=self.poll.pk)
        serializer = PollSerializer(poll)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_poll_from_user(self):
        """
        Получение опроса по ID пользователем
        """
        self.poll = Poll.objects.create(
            title='test_poll',
            description='test_description',
            start_date=timezone.now(),
            end_date=timezone.now()
        )

        response = self.client.get(
            reverse(
                'app:poll-detail',
                kwargs={'pk': self.poll.pk}
            )
        )

        poll = Poll.objects.get(id=self.poll.pk)
        serializer = PollSerializer(poll)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update_poll_from_admin(self):
        """
        Обновление опроса по ID администратором
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

        self.client.force_authenticate(user=self.superuser)

        response = self.client.patch(
            reverse('app:poll-detail', kwargs={'pk': self.poll.pk}),
            data={'title': 'updated_test_poll'}
        )

        poll = Poll.objects.get(id=self.poll.pk)
        serializer = PollSerializer(poll)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update_poll_from_user(self):
        """
        Обновление опроса по ID пользователем
        """
        self.poll = Poll.objects.create(
            title='test_poll',
            description='test_description',
            start_date=timezone.now(),
            end_date=timezone.now()
        )

        response = self.client.patch(
            reverse('app:poll-detail', kwargs={'pk': self.poll.pk}),
            data={'title': 'updated_test_poll'}
        )

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_delete_poll_from_admin(self):
        """
        Удаление опроса по ID администратором
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

        self.client.force_authenticate(user=self.superuser)

        response = self.client.delete(
            reverse(
                'app:poll-detail',
                kwargs={'pk': self.poll.pk}
            )
        )

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_delete_poll_from_user(self):
        """
        Удаление опроса по ID пользователем
        """
        self.poll = Poll.objects.create(
            title='test_poll',
            description='test_description',
            start_date=timezone.now(),
            end_date=timezone.now()
        )

        response = self.client.delete(
            reverse(
                'app:poll-detail',
                kwargs={'pk': self.poll.pk}
            )
        )

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
