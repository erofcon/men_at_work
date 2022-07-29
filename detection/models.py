from django.db import models
from user.models import CustomUser


class DetectionTable(models.Model):
    """
    Table with data uploaded for detection
    """

    description = models.CharField(verbose_name='file description', max_length=300, blank=True, null=True)
    date = models.DateTimeField(verbose_name='upload date and time')
    video = models.FileField(verbose_name='upload video', upload_to='upload_video/', blank=True, null=True)
    creator = models.ForeignKey(CustomUser, verbose_name='creator', null=True, blank=True, on_delete=models.SET_NULL,
                                related_name='run_creator')
    return_error = models.BooleanField(verbose_name="whether an error occurred during detection", default=False)
    in_processing = models.BooleanField(verbose_name="In process or not", default=True)

    def __str__(self):
        return self.date.date().__str__()

    class Meta:
        verbose_name = 'Table with data uploaded for detection'
        verbose_name_plural = 'Table with data uploaded for detection'


class Images(models.Model):
    """
    Table save images
    """

    url = models.FileField(verbose_name='image path')
    latitude = models.FloatField(verbose_name='location latitude', null=True, blank=True)
    longitude = models.FloatField(verbose_name='location longitude', null=True, blank=True)
    count_objects = models.IntegerField(verbose_name='count find objects in image', null=True, blank=True)
    date_table_id = models.ForeignKey(DetectionTable, on_delete=models.CASCADE, related_name='images')

    def __str__(self):
        return str(self.url.url)

    class Meta:
        verbose_name = 'Table save image'
        verbose_name_plural = 'Table save images'


class TrackerData(models.Model):
    """
    Table with data from GLONASS tracker
    """

    latitude = models.FloatField()
    longitude = models.FloatField()
    navigationtime = models.DateTimeField()
    imei = models.CharField(max_length=100)

    class Meta:
        verbose_name = 'Table with data from GLONASS tracker'
        verbose_name_plural = 'Table with data from GLONASS tracker'
