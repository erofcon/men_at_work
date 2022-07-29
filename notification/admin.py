from django.contrib import admin
from .models import TaskNotificationTable, DetectionNotificationTable

admin.site.register([TaskNotificationTable, DetectionNotificationTable])
