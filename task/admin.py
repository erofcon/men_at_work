from django.contrib import admin
from .models import Task, Category, Images


admin.site.register([Task, Category, Images])
