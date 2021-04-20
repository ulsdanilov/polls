from django.shortcuts import get_object_or_404
from drf_yasg.utils import swagger_auto_schema
from rest_framework import generics

from project.app.models import Session, UserForm
from project.app.serializers import UserFormSerializer


class UserFormCreateView(generics.CreateAPIView):
    serializer_class = UserFormSerializer

    @swagger_auto_schema(
        operation_description=(
            'Прохождение опроса.\n \
            Пользователь может пройти опрос один раз'
        ),
        operation_summary='Прохождение опроса',
    )
    def post(self, request, *args, **kwargs):
        if hasattr(request, 'session') and not request.session.session_key:
            request.session.save()
            request.session.modified = True

        return self.create(request, *args, **kwargs)

    def perform_create(self, serializer):
        user = get_object_or_404(
            Session,
            session_key=self.request.session.session_key
        )
        serializer.save(user=user)


class UserFormsListView(generics.ListAPIView):
    serializer_class = UserFormSerializer

    def get_queryset(self):
        if self.request.user.is_staff:
            return UserForm.objects.all()

        user = self.request.session.session_key
        return UserForm.objects.filter(user=user)

    @swagger_auto_schema(
        operation_description=(
            'Получение списка пройденных опросов.\n \
            Пользователь может получить список собственных пройденных опросов'
        ),
        operation_summary='Получение списка пройденных опросов',
    )
    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)
