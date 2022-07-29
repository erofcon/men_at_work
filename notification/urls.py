from django.urls import path
from . import views

urlpatterns = [
    path('task/delete/<int:pk>/<str:type>', views.DeleteTaskNotification.as_view()),
    path('detection/delete/<int:pk>', views.DeleteDetectionNotification.as_view())
]
