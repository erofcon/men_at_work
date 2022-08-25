from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import permissions
from task.models import Task
from geojson import MultiPoint
from .serializers import GetTaskToMapSerialize


class GetGeoJson(APIView):
    """
    Get GeoJson data
    """

    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        location = list()

        if request.user.is_superuser:
            queryset = Task.objects.filter(latitude__isnull=False).filter(longitude__isnull=False).filter(
                is_done=False).filter(expired=False).all()

        elif request.user.is_creator:
            queryset = Task.objects.filter(creator=request.user).filter(latitude__isnull=False).filter(
                longitude__isnull=False).filter(is_done=False).filter(expired=False).all()

        elif request.user.is_executor:
            queryset = Task.objects.filter(executor=request.user).filter(latitude__isnull=False).filter(
                longitude__isnull=False).filter(is_done=False).filter(expired=False).all()

        else:
            queryset = []

        for i in queryset:
            location.append([i.latitude, i.longitude])

        gjs = MultiPoint(location, precision=20)

        return Response(gjs)


class GetTaskToMap(APIView):
    """
    Get task
    """

    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        lat = request.query_params['lat']
        lng = request.query_params['lng']
        queryset = Task.objects.filter(latitude=lat, longitude=lng).filter(is_done=False, expired=False).all()

        serializer = GetTaskToMapSerialize(queryset, many=True)

        return Response(serializer.data)
