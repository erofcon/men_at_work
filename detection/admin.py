from django.contrib import admin
from .models import DetectionTable, Images, TrackerData

admin.site.register([DetectionTable, Images, TrackerData])
