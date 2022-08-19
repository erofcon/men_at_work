from rest_framework import serializers
from user.serializers import CustomUserSerializer
from .models import Task, Images, Category
from answer.serializers import GetAnswerSerializer


class CategorySerializer(serializers.ModelSerializer):
    """
    Category table serializer
    """

    class Meta:
        model = Category
        fields = '__all__'


class ImagesSerializer(serializers.ModelSerializer):
    """
    Images table serializer
    """

    url = serializers.SerializerMethodField(method_name='get_url')

    class Meta:
        model = Images
        fields = ['id', 'url']

    def get_url(self, instance):
        return instance.get_url()


class TaskTableSerializer(serializers.ModelSerializer):
    """
    Task table serializer without images
    """

    category = CategorySerializer(many=False)
    executor = CustomUserSerializer(many=False)
    creator = CustomUserSerializer(many=False)
    createDateTime = serializers.SerializerMethodField(method_name='convert_date')
    is_expired = serializers.SerializerMethodField(method_name='get_expired')
    class Meta:
        model = Task
        fields = ['id', 'category', 'executor', 'creator', 'createDateTime', 'is_done', 'is_expired']

    def get_expired(self, obj):
        return obj.expired


    def convert_date(self, obj):
        return obj.createDateTime.date()


class TaskTableDetailSerializer(serializers.ModelSerializer):
    """
    Task table serializer with more detail and with images
    """

    category = CategorySerializer(many=False)
    executor = CustomUserSerializer(many=False)
    creator = CustomUserSerializer(many=False)
    images = ImagesSerializer(many=True)
    answer = GetAnswerSerializer(many=True)
    createDateTime = serializers.SerializerMethodField(method_name='convert_date')
    is_expired = serializers.SerializerMethodField(method_name='get_expired')

    class Meta:
        model = Task
        exclude = ('address',)

    def get_expired(self, obj):
        return obj.expired

    def convert_date(self, obj):
        return obj.createDateTime.date()


class CreateTaskSerializer(serializers.ModelSerializer):
    """
    Create task serializer
    """

    class Meta:
        model = Task
        fields = '__all__'


class UpdateTaskSerializer(serializers.ModelSerializer):
    """
    Serializer fro close task
    """

    class Meta:
        model = Task
        fields = ['is_done']
