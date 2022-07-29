from django.urls import path
from . import views

urlpatterns = [
    path('get/geojson', views.GetGeoJson.as_view()),
    path('get/tasktomap', views.GetTaskToMap.as_view()),
]


