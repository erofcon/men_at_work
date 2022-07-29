from django.db import models
from django.contrib.auth.models import AbstractUser
from phonenumber_field.modelfields import PhoneNumberField


class CustomUser(AbstractUser):
    """
    Create custom User
    """

    is_creator = models.BooleanField(verbose_name='Is creator ',
                                     help_text='Check if the user can create a task',
                                     default=False)
    is_executor = models.BooleanField(verbose_name='Is executor',
                                      help_text='Check if the user can execute a task', default=False)
    number_phone = PhoneNumberField(verbose_name="user's phone number", blank=True, null=True)
