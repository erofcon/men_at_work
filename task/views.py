from datetime import datetime, timedelta
from django.db.models import QuerySet, Q

from rest_framework.generics import ListAPIView, RetrieveAPIView, CreateAPIView, UpdateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework import pagination
from rest_framework.views import APIView
from rest_framework.response import Response
from men_at_work import permissions
from .serializers import TaskTableSerializer, TaskTableDetailSerializer, CreateTaskSerializer, CategorySerializer, \
    UpdateTaskSerializer
from .models import Task, Images, Category
from notification.models import TaskNotificationTable
import json

class SetPagination(pagination.PageNumberPagination):
    """
    Pagination settings
    """

    page_size = 10
    page_size_query_param = 'page_size'
    ordering = 'created_at'


class GetTaskList(ListAPIView):
    """
    Get tasks

    Params:
        value - The parameter for searching for the necessary tasks.
        Possible values - 'all_current_tasks', 'new_current_tasks', 'expiring_current_tasks',
        'expired_tasks', 'is_done', 'all'

        page - Parameter for getting the page

    """

    permission_classes = [IsAuthenticated]
    queryset = Task.objects.all()
    serializer_class = TaskTableSerializer
    pagination_class = SetPagination

    def get_model_with_condition(self):
        param = self.request.query_params.get('value')

        if param:
            if param == 'all_current_tasks':
                return self.queryset.filter(Q(expired=False) & Q(is_done=False))

            elif param == 'new_current_tasks':
                return self.queryset.filter(
                    Q(expired=False) & Q(createDateTime__gte=datetime.today() - timedelta(days=2))
                    & Q(is_done=False))

            elif param == 'expiring_current_tasks':
                return self.queryset.filter(
                    Q(expired=False) & Q(leadDateTime__lte=datetime.today() - timedelta(days=14)) &
                    Q(is_done=False) & Q(expired=False))

            elif param == 'expired_tasks':
                return self.queryset.filter(Q(expired=True) & Q(is_done=False))

            elif param == 'is_done':
                return self.queryset.filter(is_done=True)

            elif param == 'all':
                return self.queryset.all()

        return self.queryset.all()

    def get_queryset(self):

        assert self.queryset is not None, (
                "'%s' should either include a `queryset` attribute, "
                "or override the `get_queryset()` method."
                % self.__class__.__name__
        )

        if self.request.user.is_superuser:
            queryset = self.get_model_with_condition()

        elif self.request.user.is_creator:
            self.queryset = self.queryset.filter(creator=self.request.user)
            queryset = self.get_model_with_condition()

        elif self.request.user.is_executor:
            self.queryset = self.queryset.filter(executor=self.request.user)
            queryset = self.get_model_with_condition()

        if isinstance(queryset, QuerySet):
            queryset = queryset.all()

        return queryset


class GetDetailedTask(RetrieveAPIView):
    """
    Get one task with more detail and with images
    """

    permission_classes = [permissions.UserHasAccess]
    queryset = Task.objects.all()
    serializer_class = TaskTableDetailSerializer


class CreateTask(CreateAPIView):
    """
    Create task
    """

    permission_classes = [permissions.UserCanCreate]
    queryset = Task
    serializer_class = CreateTaskSerializer

    def perform_create(self, serializer):
        serializer.validated_data['creator'] = self.request.user
        task = serializer.save()

        images = self.request.FILES.getlist('images')

        for image in images:
            Images.objects.create(
                url=image,
                task=task
            )
        print(serializer.validated_data['latitude'])
        notification = TaskNotificationTable(task_id=task, related_user=task.executor, type='new task')
        notification.save()



class GetCountTask(APIView):
    """
    Get statistics on current tasks
    """

    permission_classes = [IsAuthenticated]

    def get(self, request):

        if self.request.user.is_superuser:
            queryset = Task.objects.all()

        else:
            queryset = Task.objects.filter(Q(creator=self.request.user) | Q(executor=self.request.user))

        count_all_tasks = queryset.filter(Q(is_done=False) & Q(expired=False)).count()
        count_is_done_tasks = queryset.filter(Q(is_done=True)).count()
        count_expired_tasks = queryset.filter(Q(is_done=False) & Q(expired=True)).count()

        # count_expiring_tasks = queryset.filter(
        #     Q(leadDateTime__lte=datetime.today() + timedelta(days=2)) & Q(is_done=False) &
        #     Q(expired=False)).count()

        data = {
            'count_current_tasks': count_all_tasks,
            'count_is_done_tasks': count_is_done_tasks,
            'count_expired_tasks': count_expired_tasks,
        }

        return Response(data)


class GetCategory(ListAPIView):
    """
    Get task category
    """

    permission_classes = [IsAuthenticated]
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class CloseTask(UpdateAPIView):
    """
    Close task
    """

    permission_classes = [permissions.UserCanCreate]
    queryset = Task.objects.all()
    serializer_class = UpdateTaskSerializer

    def perform_update(self, serializer):
        serializer.validated_data['is_done'] = True
        task = serializer.save()

        notification = TaskNotificationTable(task_id=task, related_user=task.executor, type='close task')
        notification.save()
