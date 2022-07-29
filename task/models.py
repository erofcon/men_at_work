from datetime import datetime
from django.db import models
from django.db.models import ExpressionWrapper, BooleanField, Q
from user.models import CustomUser


class ExpiredManager(models.Manager):

    def get_queryset(self):
        return super().get_queryset().annotate(
            expired=ExpressionWrapper(Q(leadDateTime__lt=datetime.now()), output_field=BooleanField())
        )


class Category(models.Model):
    """
    Table with task category
    """

    name = models.CharField('category name', max_length=100)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Table with task category'
        verbose_name_plural = 'Table with task categories'


class Task(models.Model):
    """
    Table with tasks
    """""

    category = models.ForeignKey(Category, verbose_name='task category', null=True, blank=True,
                                 on_delete=models.SET_NULL,
                                 related_name='category')
    createDateTime = models.DateTimeField(verbose_name='task create date and time', auto_now=True)
    leadDateTime = models.DateTimeField(verbose_name='task lead date and time', blank=True, null=True)
    description = models.CharField(verbose_name='description of task', max_length=500, null=True, blank=True)
    latitude = models.FloatField(verbose_name='location latitude',  blank=True, null=True)
    longitude = models.FloatField(verbose_name='location longitude',  blank=True, null=True)
    address = models.TextField(verbose_name='location address', null=True, blank=True)
    executor = models.ForeignKey(CustomUser, verbose_name='task executor', null=True, blank=True,
                                 on_delete=models.SET_NULL,
                                 related_name='executor')
    creator = models.ForeignKey(CustomUser, verbose_name='task creator', null=True, blank=True,
                                on_delete=models.SET_NULL,
                                related_name='creator')
    is_done = models.BooleanField(verbose_name='Task is done or not', default=False)
    objects = ExpiredManager()

    def __str__(self):
        return self.createDateTime.date().__str__()

    class Meta:
        ordering = ('-createDateTime',)
        verbose_name = 'Table with task'
        verbose_name_plural = 'Table with tasks'


class Images(models.Model):
    """
    Table with task images
    """

    url = models.ImageField(upload_to='single_task/', blank=True, null=True)
    task = models.ForeignKey(Task, verbose_name='related task', null=True, blank=True,
                             on_delete=models.CASCADE,
                             related_name='images')

    def get_url(self):
        return 'http://127.0.0.1:8000' + self.url.url

    def __str__(self):
        return self.url.url

    class Meta:
        verbose_name = 'Table with task image'
        verbose_name_plural = 'Table with task images'
