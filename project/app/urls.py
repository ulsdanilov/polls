from django.urls import path

from project.app.views.choices_view import (ChoiceCreateView, ChoiceDetailView,
                                            ChoicesListView)
from project.app.views.polls_view import (PollCreateView, PollDetailView,
                                          PollsListView)
from project.app.views.questions_view import (QuestionCreateView,
                                              QuestionDetailView,
                                              QuestionsListView)
from project.app.views.user_forms_view import (UserFormCreateView,
                                               UserFormsListView)

app_name = 'app'

urlpatterns = [
    path('polls/create/', PollCreateView.as_view(), name='poll-create'),
    path('polls/', PollsListView.as_view(), name='poll-list'),
    path('polls/<int:pk>/', PollDetailView.as_view(), name='poll-detail'),
    path('questions/create/', QuestionCreateView.as_view(), name='question-create'),
    path('questions/', QuestionsListView.as_view(), name='question-list'),
    path('questions/<int:pk>/', QuestionDetailView.as_view(), name='question-detail'),
    path('choices/create/', ChoiceCreateView.as_view(), name='choice-create'),
    path('choices/', ChoicesListView.as_view(), name='choice-list'),
    path('choices/<int:pk>/', ChoiceDetailView.as_view(), name='choice-detail'),
    path('user_forms/create/', UserFormCreateView.as_view(), name='user_form-create'),
    path('user_forms/', UserFormsListView.as_view(), name='user_form-list'),
]
