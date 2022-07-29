from rest_framework.views import APIView
from rest_framework.generics import DestroyAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from men_at_work.permissions import UserCanCreate
from notification.models import TaskNotificationTable, DetectionNotificationTable
from notification.serializers import DetectionNotificationSerializer

class DeleteTaskNotification(APIView):
    """
    Delete task notification
    """

    permission_classes = [IsAuthenticated]

    def delete(self, request, *args, **kwargs):

        if request.user.is_creator and kwargs['type'] == 'answer':
            TaskNotificationTable.objects.get(id=kwargs['pk']).delete()
            return Response({}, status.HTTP_204_NO_CONTENT)

        if request.user.is_executor and kwargs['type'] == 'new task' or kwargs['type'] == 'close task':
            TaskNotificationTable.objects.get(id=kwargs['pk']).delete()
            return Response({}, status.HTTP_204_NO_CONTENT)

        return Response({'no has access'}, status.HTTP_406_NOT_ACCEPTABLE)


class DeleteDetectionNotification(DestroyAPIView):
    """
    Delete detection notification
    """

    permission_classes = [UserCanCreate]
    queryset = DetectionNotificationTable
    serializer_class = DetectionNotificationSerializer




















