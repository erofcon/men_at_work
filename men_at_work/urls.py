from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from rest_framework_simplejwt.views import TokenRefreshView


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/token/', include('user.urls')),
    path('api/v1/refresh_token/', TokenRefreshView.as_view(), name='refresh_token'),
    path('api/v1/task/', include('task.urls')),
    path('api/v1/answer/', include('answer.urls')),
    path('api/v1/detection/', include('detection.urls')),
    path('api/v1/map/', include('map.urls')),
    path('api/v1/report/', include('report.urls')),
    path('api/v1/notification/', include('notification.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
