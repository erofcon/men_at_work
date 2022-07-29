from django.urls import path
from .views import MyTokenObtainPairView, GetRelatedUser

urlpatterns = [
    path('', MyTokenObtainPairView.as_view(), name='token'),
    path('related_user', GetRelatedUser.as_view()),
]

