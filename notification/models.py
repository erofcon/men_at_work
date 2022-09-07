from django.db import models
from user.models import CustomUser
from task.models import Task
from detection.models import DetectionTable


class TaskNotificationTable(models.Model):
    """
    Table with TaskNotifications
    """

    CHOICES = (
        ('new task', 'new_task'),
        ('answer', 'answer'),
        ('close task', 'close_task')
    )

    task_id = models.ForeignKey(Task, verbose_name='related task', on_delete=models.CASCADE)
    related_user = models.ForeignKey(CustomUser, verbose_name='related user', on_delete=models.CASCADE)
    type = models.CharField(max_length=50, verbose_name='notification type', choices=CHOICES)
    createDateTime = models.DateTimeField(verbose_name='notification create date and time', auto_now=True)

    def __str__(self):
        return self.type

    class Meta:
        verbose_name = 'Table with notification'
        verbose_name_plural = 'Table with notifications'


class DetectionNotificationTable(models.Model):
    """
    Notification for table Detection
    """

    CHOICES = (
        ('detection finished', 'detection_finished'),
    )

    createDateTime = models.DateTimeField(verbose_name='notification create date and time', auto_now=True)
    type = models.CharField(max_length=50, verbose_name='notification type', choices=CHOICES)
    detection_id = models.ForeignKey(DetectionTable, verbose_name='related detection table', on_delete=models.CASCADE)
    recipient = models.ForeignKey(CustomUser, verbose_name='notification recipient', on_delete=models.CASCADE)

    def __str__(self):
        return self.type

    class Meta:
        verbose_name = 'Table with detection notification'
        verbose_name_plural = 'Table with detection notifications'
