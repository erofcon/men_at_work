from django.urls import path
from . import views

urlpatterns = [
    path('get/counttask', views.GetCountTask.as_view()),
    path('get/createreport', views.CreateReport.as_view())
]
