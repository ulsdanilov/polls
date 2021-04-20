from drf_yasg.utils import swagger_auto_schema
from rest_framework import generics
from rest_framework.permissions import IsAdminUser

from project.app.models import Question
from project.app.permissions import IsAdminOrReadOnly
from project.app.serializers import QuestionSerializer


class QuestionCreateView(generics.CreateAPIView):
    serializer_class = QuestionSerializer
    permission_classes = (IsAdminUser, )

    @swagger_auto_schema(
        operation_description=(
            'Добавление нового вопроса.\n \
            Доступ имеет только Администратор'
        ),
        operation_summary='Добавление нового вопроса',
    )
    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)


class QuestionsListView(generics.ListAPIView):
    serializer_class = QuestionSerializer
    queryset = Question.objects.all()

    @swagger_auto_schema(
        operation_description=(
            'Получение списка всех вопросов.\n \
            Пользователь может получить список вопросов из активных опросов'
        ),
        operation_summary='Получение списка вопросов',
    )
    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)


class QuestionDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = QuestionSerializer
    queryset = Question.objects.all()
    permission_classes = (IsAdminOrReadOnly, )

    @swagger_auto_schema(
        operation_description='Получение вопроса по ID',
        operation_summary='Получение вопроса по ID',
    )
    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description=(
            'Обновление вопроса по ID.\n \
            Доступ имеет только Администратор'
        ),
        operation_summary='Обновление вопроса по ID',
    )
    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)
    
    @swagger_auto_schema(
        operation_description=(
            'Частичное обновление вопроса по ID.\n \
            Доступ имеет только Администратор'
        ),
        operation_summary='Обновление вопроса по ID',
    )
    def patch(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)
    
    @swagger_auto_schema(
        operation_description=(
            'Удаление вопроса по ID.\n \
            Доступ имеет только Администратор'
        ),
        operation_summary='Удаление вопроса по ID',
    )
    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)
