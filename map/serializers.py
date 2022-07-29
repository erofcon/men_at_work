from rest_framework import serializers
from task.models import Task, Images
from task.serializers import CategorySerializer, ImagesSerializer
from user.serializers import CustomUserSerializer

#
# class ImagesSerializer(serializers.ModelSerializer):
#     """
#     Сериалайзер таблицы Images
#     """
#
#     url = serializers.SerializerMethodField(method_name='get_url')
#
#     class Meta:
#         model = Images
#         fields = ['id', 'url']
#
#     def get_url(self, instance):
#         return instance.get_url()


class GetTaskToMapSerialize(serializers.ModelSerializer):
    """
    Task table serializer with one image
    """

    images = serializers.SerializerMethodField(method_name='get_image')
    category = CategorySerializer(many=False)
    executor = CustomUserSerializer(many=False)
    creator = CustomUserSerializer(many=False)
    state = serializers.SerializerMethodField(method_name='is_expired')
    createDateTime = serializers.SerializerMethodField(method_name='convert_date')

    class Meta:
        model = Task

        fields = ['id', 'images', 'category', 'executor', 'creator', 'state', 'createDateTime']

    def get_image(self, instance):
        queryset = instance.images.first()
        serializer = ImagesSerializer(queryset)

        return serializer.data

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



