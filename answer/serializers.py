from rest_framework import serializers
from .models import Answer, AnswerImages


class AnswerImagesSerializer(serializers.ModelSerializer):
    """
    Serializer for table AnswerImages
    """

    url = serializers.SerializerMethodField(method_name='get_url')

    class Meta:
        model = AnswerImages
        fields = '__all__'

    def get_url(self, obj):
        return obj.get_url()


class CreateAnswerSerializer(serializers.ModelSerializer):
    """
    Answer serializer for create
    """

    answerImages = serializers.SerializerMethodField(method_name='get_images')
    replyDate = serializers.SerializerMethodField(method_name='convert_date')

    class Meta:
        model = Answer
        fields = '__all__'

    def get_images(self, obj):
        answer_images = obj.answerImages.all()

        serializer = AnswerImagesSerializer(answer_images, many=True)
        return serializer.data

    def convert_date(self, obj):
        return obj.replyDate.date()


class GetAnswerSerializer(serializers.ModelSerializer):
    """
    Answer serializer
    """

    answerImages = AnswerImagesSerializer(many=True)
    replyDate = serializers.SerializerMethodField(method_name='convert_date')

    class Meta:
        model = Answer
        fields = '__all__'

    def convert_date(self, obj):
        return obj.replyDate.date()