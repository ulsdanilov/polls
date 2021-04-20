from django.contrib.auth.models import User
from django.urls import reverse
from django.utils import timezone
from rest_framework import status
from rest_framework.test import APITransactionTestCase

from project.app.models import Poll, Question
from project.app.serializers import QuestionSerializer


class QuestionCreateViewTests(APITransactionTestCase):
    """
    Проверка создания вопроса
    """

    def test_create_question_from_admin(self):
        """
        Создание вопроса администратором
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

        response = self.client.post(
            reverse('app:question-create'),
            data = {
                'poll': self.poll.pk,
                'text': 'test_text',
                'question_type': 'SINGLE'
            }
        )

        question_id = response.data['pk']
        question = Question.objects.get(pk=question_id)
        serializer = QuestionSerializer(question)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_question_from_user(self):
        """
        Создание вопроса пользователем
        """
        self.poll = Poll.objects.create(
            title='test_poll',
            description='test_description',
            start_date=timezone.now(),
            end_date=timezone.now()
        )

        response = self.client.post(
            reverse('app:question-create'),
            data = {
                'poll': self.poll.pk,
                'text': 'test_text',
                'question_type': 'SINGLE'
            }
        )

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class QuestionListViewTests(APITransactionTestCase):
    """
    Проверка получения списка вопросов
    """

    def test_get_all_polls_from_admin(self):
        """
        Получение списка вопросов администратором
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

        response = self.client.get(reverse('app:question-list'))
        questions = Question.objects.all()
        serializer = QuestionSerializer(questions, many=True)
        self.assertEqual(response.data['results'], serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_all_questions_from_user(self):
        """
        Получение списка вопросов пользователем
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

        response = self.client.get(reverse('app:question-list'))
        questions = Question.objects.all()
        serializer = QuestionSerializer(questions, many=True)
        self.assertEqual(response.data['results'], serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class QuestionDetailViewTests(APITransactionTestCase):
    """
    Проверка получения, обновления и удаления вопроса по ID
    """

    def test_get_question_from_admin(self):
        """
        Получение вопроса по ID администратором
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

        response = self.client.get(
            reverse(
                'app:question-detail',
                kwargs={'pk': self.question.pk}
            )
        )

        question = Question.objects.get(id=self.question.pk)
        serializer = QuestionSerializer(question)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_question_from_user(self):
        """
        Получение вопроса по ID пользователем
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

        response = self.client.get(
            reverse(
                'app:question-detail',
                kwargs={'pk': self.question.pk}
            )
        )

        question = Question.objects.get(id=self.question.pk)
        serializer = QuestionSerializer(question)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update_question_from_admin(self):
        """
        Обновление вопроса по ID администратором
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

        response = self.client.patch(
            reverse('app:question-detail', kwargs={'pk': self.question.pk}),
            data={'text': 'updated_test_text'}
        )

        question = Question.objects.get(id=self.question.pk)
        serializer = QuestionSerializer(question)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update_question_from_user(self):
        """
        Обновление вопроса по ID пользователем
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

        response = self.client.patch(
            reverse('app:question-detail', kwargs={'pk': self.question.pk}),
            data={'text': 'updated_test_text'}
        )

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_delete_question_from_admin(self):
        """
        Удаление вопроса по ID администратором
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

        response = self.client.delete(
            reverse(
                'app:question-detail',
                kwargs={'pk': self.question.pk}
            )
        )

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_delete_question_from_user(self):
        """
        Удаление вопроса по ID пользователем
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

        response = self.client.delete(
            reverse(
                'app:question-detail',
                kwargs={'pk': self.question.pk}
            )
        )

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
