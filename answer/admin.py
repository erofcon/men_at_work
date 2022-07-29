from django.contrib import admin
from .models import Answer, AnswerImages


admin.site.register([Answer, AnswerImages])
