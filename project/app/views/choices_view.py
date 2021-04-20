from drf_yasg.utils import swagger_auto_schema
from rest_framework import generics
from rest_framework.permissions import IsAdminUser

from project.app.models import Choice
from project.app.permissions import IsAdminOrReadOnly
from project.app.serializers import ChoiceSerializer


class ChoiceCreateView(generics.CreateAPIView):
    serializer_class = ChoiceSerializer
    permission_classes = (IsAdminUser, )

    @swagger_auto_schema(
        operation_description=(
            'Добавление нового варианта ответа к вопросу.\n \
            Доступ имеет только Администратор'
        ),
        operation_summary='Добавление нового варианта ответа к вопросу',
    )
    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)


class ChoicesListView(generics.ListAPIView):
    serializer_class = ChoiceSerializer
    queryset = Choice.objects.all()

    @swagger_auto_schema(
        operation_description='Получение списка всех вариантов ответа к вопросу',
        operation_summary='Получение вариантов ответа к вопросу',
    )
    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)


class ChoiceDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = ChoiceSerializer
    queryset = Choice.objects.all()
    permission_classes = (IsAdminOrReadOnly, )

    @swagger_auto_schema(
        operation_description='Получение варианта ответа к вопросу по ID',
        operation_summary='Получение варианта ответа к вопросу по ID',
    )
    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description=(
            'Обновление варианта ответа к вопросу по ID.\n \
            Доступ имеет только Администратор'
        ),
        operation_summary='Обновление варианта ответа к вопросу по ID',
    )
    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)
    
    @swagger_auto_schema(
        operation_description=(
            'Частичное обновление варианта ответа к вопросу по ID.\n \
            Доступ имеет только Администратор'
        ),
        operation_summary='Обновление варианта ответа к вопросу по ID',
    )
    def patch(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description=(
            'Удаление варианта ответа к вопросу по ID.\n \
            Доступ имеет только Администратор'
        ),
        operation_summary='Удаление варианта ответа к вопросу по ID',
    )
    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)
