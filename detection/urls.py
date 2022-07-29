from django.urls import path
from . import views

urlpatterns = [
    path('get', views.DetectedList.as_view()),
    path('get/<int:pk>', views.GetDetailDetection.as_view()),
    path('delete/detection/<int:pk>', views.DeleteDetection.as_view()),
    path('delete/image/<int:pk>', views.DeleteImage.as_view()),
    path('post/run', views.RunDetection.as_view()),
]
