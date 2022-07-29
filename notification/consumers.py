from django.db.models import QuerySet, Q
from rest_framework import status
from djangochannelsrestframework.generics import GenericAsyncAPIConsumer
from djangochannelsrestframework.observer.generics import ObserverConsumerMixin, action
from djangochannelsrestframework.observer import model_observer
from .models import TaskNotificationTable, DetectionNotificationTable
from .serializers import TaskNotificationSerializer, DetectionNotificationSerializer


class NotificationConsumer(ObserverConsumerMixin, GenericAsyncAPIConsumer):
    queryset = TaskNotificationTable.objects.all()
    serializer_class = TaskNotificationSerializer

    """
    Subscribe to TaskNotification table
    """

    @action()
    async def subscribe_task_notification_activity(self, request_id, **kwargs):
        await self.task_notification_activity.subscribe(request_id=request_id, user=self.scope['user'])

    @model_observer(TaskNotificationTable, serializer_class=TaskNotificationSerializer)
    async def task_notification_activity(self, message, action, subscribing_request_ids=[], **kwargs):
        for request_id in subscribing_request_ids:
            if self.scope['user'].id == message['related_user']:
                await self.reply(data=[message], action=action, request_id=request_id)
            else:
                await self.reply(data=[], action=action, request_id=request_id)
    """"""

    """
    Subscribe to DetectionNotificationTable
    """

    @action()
    async def subscribe_detection_notification_activity(self, request_id, **kwargs):
        await self.detection_notification_activity.subscribe(request_id=request_id)

    @model_observer(DetectionNotificationTable, serializer_class=DetectionNotificationSerializer)
    async def detection_notification_activity(self, message, action, subscribing_request_ids=[], **kwargs):
        for request_id in subscribing_request_ids:
            if self.scope['user'].id == message['recipient']:
                await self.reply(data=[message], action=action, request_id=request_id)
            else:
                await self.reply(data=[], action=action, request_id=request_id)

    """"""

    """
    Get TaskNotification list
    """

    @action()
    def get_task_notification_list(self, **kwargs):

        if self.scope['user'].is_creator:
            queryset = TaskNotificationTable.objects.filter(related_user=self.scope['user']).filter(type='answer').\
                filter(task_id__creator=self.scope['user']).all()

        elif self.scope['user'].is_executor:
            queryset = TaskNotificationTable.objects.filter(related_user=self.scope['user']).filter(Q(type='close task') | Q(type='new task'))
        else:
            return [], status.HTTP_200_OK

        serializer = TaskNotificationSerializer(queryset, many=True)

        return serializer.data, status.HTTP_200_OK

    """"""

    """
    Get DetectionNotification list
    """

    @action()
    def get_detection_notification_list(self, **kwargs):

        if self.scope['user'].is_creator:
            queryset = DetectionNotificationTable.objects.filter(recipient=self.scope['user']).all()
        else:
            return [], status.HTTP_200_OK

        serializer = DetectionNotificationSerializer(queryset, many=True)

        return serializer.data, status.HTTP_200_OK
