from rest_framework import serializers
from task.models import Task, Images
from task.serializers import CategorySerializer, ImagesSerializer
from user.serializers import CustomUserSerializer


class GetTaskToMapSerialize(serializers.ModelSerializer):
    """
    Task table serializer with one image
    """

    images = serializers.SerializerMethodField(method_name='get_image')
    category = CategorySerializer(many=False)
    executor = CustomUserSerializer(many=False)
    creator = CustomUserSerializer(many=False)
    createDateTime = serializers.SerializerMethodField(method_name='convert_date')
    is_expired = serializers.SerializerMethodField(method_name='get_expired')

    class Meta:
        model = Task

        fields = ['id', 'images', 'category', 'executor', 'creator', 'createDateTime', 'is_done', 'is_expired']

    def get_image(self, instance):
        queryset = instance.images.first()
        serializer = ImagesSerializer(queryset)

        return serializer.data

    def get_expired(self, obj):
        return obj.expired

    def convert_date(self, obj):
        return obj.createDateTime.date()
