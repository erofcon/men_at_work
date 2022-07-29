from rest_framework import serializers
from .models import TaskNotificationTable
from .models import DetectionNotificationTable


class TaskNotificationSerializer(serializers.ModelSerializer):

    class Meta:
        model = TaskNotificationTable
        fields = '__all__'


class DetectionNotificationSerializer(serializers.ModelSerializer):

    class Meta:
        model = DetectionNotificationTable
        fields = '__all__'
