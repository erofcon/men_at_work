from django.urls import path
from . import views

urlpatterns = [
    path('get', views.GetTaskList.as_view()),
    path('get/<int:pk>', views.GetDetailedTask.as_view()),
    path('get/counttask', views.GetCountTask.as_view()),
    path('get/category', views.GetCategory.as_view()),
    path('post/create', views.CreateTask.as_view()),
    path('put/update/<int:pk>', views.CloseTask.as_view()),
]
