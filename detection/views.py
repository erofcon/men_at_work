from django.db.models import QuerySet
from rest_framework.generics import ListAPIView, RetrieveAPIView, DestroyAPIView, CreateAPIView
from .serializers import DetectedTableSerializer, DetailDetectedTableSerializer, ReturnDetectedTableSerializer
from .models import DetectionTable, Images
from .tasks import run_detection
from men_at_work.permissions import UserCanView, UserCanCreate


class DetectedList(ListAPIView):
    """
    Get Detection list
    """

    permission_classes = [UserCanView]
    queryset = DetectionTable.objects.all()
    serializer_class = ReturnDetectedTableSerializer

    def get_queryset(self):

        assert self.queryset is not None, (
                "'%s' should either include a `queryset` attribute, "
                "or override the `get_queryset()` method."
                % self.__class__.__name__
        )

        if self.request.user.is_superuser:
            queryset = self.queryset.all()

        elif self.request.user.is_creator:
            queryset = self.queryset.filter(creator=self.request.user)

        return queryset


class GetDetailDetection(RetrieveAPIView):
    """
    Get detail Detection with images
    """

    permission_classes = [UserCanView]
    queryset = DetectionTable
    serializer_class = DetailDetectedTableSerializer


class DeleteDetection(DestroyAPIView):
    """
    Delete Detection
    """

    permission_classes = [UserCanCreate]
    queryset = DetectionTable.objects.all()

    def perform_destroy(self, instance):
        if instance.creator == self.request.user or self.request.user.is_superuser:
            instance.delete()


class DeleteImage(DestroyAPIView):
    """
    Delete Image
    """

    permission_classes = [UserCanCreate]
    queryset = Images.objects.all()

    def perform_destroy(self, instance):
        if instance.date_table_id.creator == self.request.user or self.request.user.is_superuser:
            instance.delete()


class RunDetection(CreateAPIView):
    """
    Run to detection
    """

    permission_classes = [UserCanCreate]
    queryset = DetectionTable
    serializer_class = DetectedTableSerializer

    def perform_create(self, serializer):
        serializer.validated_data['creator'] = self.request.user
        serializer.validated_data['in_processing'] = True
        table = serializer.save()
        run_detection.delay(table.id)
