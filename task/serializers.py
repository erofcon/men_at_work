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
    state = serializers.SerializerMethodField(method_name='is_expired')
    createDateTime = serializers.SerializerMethodField(method_name='convert_date')

    class Meta:
        model = Task
        fields = 'id', 'description', 'category', 'description', 'createDateTime', 'creator', 'executor', 'state'

    def convert_date(self, obj):
        return obj.createDateTime.date()

    def is_expired(self, obj):
        if not obj.is_done:
            if obj.expired:
                return 'просрочено'
            else:
                return 'на выполнении'
        else:
            return 'выполнено'


class TaskTableDetailSerializer(serializers.ModelSerializer):
    """
    Task table serializer with more detail and with images
    """

    category = CategorySerializer(many=False)
    executor = CustomUserSerializer(many=False)
    creator = CustomUserSerializer(many=False)
    images = ImagesSerializer(many=True)
    answer = GetAnswerSerializer(many=True)
    state = serializers.SerializerMethodField(method_name='is_expired')
    createDateTime = serializers.SerializerMethodField(method_name='convert_date')

    class Meta:
        model = Task
        fields = '__all__'

    def is_expired(self, obj):
        if not obj.is_done:
            if obj.expired:
                return 'просрочено'
            else:
                return 'на выполнении'
        else:
            return 'выполнено'

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





