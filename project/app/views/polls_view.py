from django.utils import timezone
from drf_yasg.utils import swagger_auto_schema
from rest_framework import generics
from rest_framework.permissions import IsAdminUser

from project.app.models import Poll
from project.app.permissions import IsAdminOrReadOnly
from project.app.serializers import PollSerializer


class PollCreateView(generics.CreateAPIView):
    serializer_class = PollSerializer
    permission_classes = (IsAdminUser, )

    @swagger_auto_schema(
        operation_description=(
            'Добавление нового опроса.\n \
            Доступ имеет только Администратор'
        ),
        operation_summary='Добавление нового опроса',
    )
    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)


class PollsListView(generics.ListAPIView):
    serializer_class = PollSerializer

    def get_queryset(self):
        if self.request.user.is_anonymous:
            return Poll.objects.filter(
                start_date__lte=timezone.now(),
                end_date__gte=timezone.now()
            )
        
        return Poll.objects.all()

    @swagger_auto_schema(
        operation_description=(
            'Получение списка всех опросов.\n \
            Пользователь может получить список активных опросов'
        ),
        operation_summary='Получение списка опросов',
    )
    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)


class PollDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = PollSerializer
    queryset = Poll.objects.all()
    permission_classes = (IsAdminOrReadOnly, )

    @swagger_auto_schema(
        operation_description='Получение опроса по ID',
        operation_summary='Получение опроса по ID',
    )
    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description=(
            'Обновление опроса по ID.\n \
            Доступ имеет только Администратор'
        ),
        operation_summary='Обновление опроса по ID',
    )
    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)
    
    @swagger_auto_schema(
        operation_description=(
            'Частичное обновление опроса по ID.\n \
            Доступ имеет только Администратор'
        ),
        operation_summary='Частичное обновление опроса по ID',
    )
    def patch(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description=(
            'Удаление опроса по ID.\n \
            Доступ имеет только Администратор'
        ),
        operation_summary='Удаление опроса по ID',
    )
    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)
