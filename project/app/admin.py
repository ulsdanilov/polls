from django.contrib import admin

from .models import Choice, Poll, Question, UserAnswer, UserForm

admin.site.register(Poll)
admin.site.register(Question)
admin.site.register(Choice)
admin.site.register(UserForm)
admin.site.register(UserAnswer)
