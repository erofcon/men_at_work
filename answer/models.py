from django.db import models
from task.models import Task


class Answer(models.Model):
    """
    Answer table for task
    """

    description = models.CharField(verbose_name='answer description', max_length=500)
    replyDate = models.DateTimeField(verbose_name='date and time create answer', auto_now=True)
    task = models.ForeignKey(Task, verbose_name='related task', on_delete=models.CASCADE, related_name='answer')

    def __str__(self):
        return self.description.__str__()

    class Meta:
        ordering = ('-replyDate',)
        verbose_name = 'Table with answer'
        verbose_name_plural = 'Table with answers'


class AnswerImages(models.Model):
    """
    Table with answer images
    """

    url = models.ImageField(verbose_name='answer image', upload_to='task_answer/', blank=True, null=True)
    answer = models.ForeignKey(Answer, verbose_name='related answer', null=True, blank=True,
                               on_delete=models.CASCADE,
                               related_name='answerImages')

    def get_url(self):
        return 'http://127.0.0.1:8000' + self.url.url

    def __str__(self):
        return self.url.url

    class Meta:
        verbose_name = 'Table with answer image'
        verbose_name_plural = 'Table with answer images'
