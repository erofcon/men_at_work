from rest_framework.generics import CreateAPIView
from rest_framework.response import Response
from rest_framework import status

from notification.models import TaskNotificationTable
from .serializers import CreateAnswerSerializer
from task.models import Task
from .models import Answer, AnswerImages
from men_at_work import permissions


class CreateAnswer(CreateAPIView):
    """
    Create answer for task
    """

    permission_classes = [permissions.UserCanAnswer]
    queryset = Answer
    serializer_class = CreateAnswerSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        task = Task.objects.filter(id=self.request.data['task']).first()

        if not task.is_done and task.executor == self.request.user:
            self.perform_create(serializer)
            headers = self.get_success_headers(serializer.data)
            return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

        else:
            return Response('no permission to change', status=status.HTTP_406_NOT_ACCEPTABLE)

    def perform_create(self, serializer):

        answer = serializer.save()
        images = self.request.FILES.getlist('images')

        for image in images:
            AnswerImages.objects.create(
                url=image,
                answer=answer
            )

        notification = TaskNotificationTable(task_id=answer.task, related_user=answer.task.creator, type='answer')
        notification.save()
