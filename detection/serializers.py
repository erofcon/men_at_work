from rest_framework import serializers
from .models import DetectionTable, Images


class ImagesSerializer(serializers.ModelSerializer):
    """
    Image table serializer
    """

    class Meta:
        model = Images
        fields = '__all__'


class DetectedTableSerializer(serializers.ModelSerializer):
    """
    DetectedTable table serializer
    """

    class Meta:
        model = DetectionTable
        fields = '__all__'


class ReturnDetectedTableSerializer(serializers.ModelSerializer):
    """
    DetectedTable table serializer
    """
    date = serializers.SerializerMethodField(method_name='convert_date')
    count_img = serializers.SerializerMethodField(method_name='get_count_img')

    class Meta:
        model = DetectionTable
        fields = '__all__'

    def convert_date(self, obj):
        return obj.date.date().__str__()

    def get_count_img(self, obj):
        ob = obj.images.all()
        return ob.count()


class DetailDetectedTableSerializer(serializers.ModelSerializer):
    """
    DetectedTable table serializer with images
    """

    images = ImagesSerializer(many=True)

    class Meta:
        model = DetectionTable
        fields = '__all__'
