from django.urls import path
from . import views

urlpatterns = [
    path('post/create', views.CreateAnswer.as_view()),
]

