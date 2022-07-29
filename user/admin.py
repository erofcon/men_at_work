from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser
from .forms import CustomUserCreationForm


class CustomUserAdmin(UserAdmin):
    """
    Change Django-Admin ViewSet
    """

    model = CustomUser
    add_form = CustomUserCreationForm
    list_display = (
        'username', 'email', 'first_name', 'last_name', 'is_creator', 'is_executor', 'is_superuser'
    )

    fieldsets = (
        *UserAdmin.fieldsets,
        (
            '',
            {
                'fields': (
                    'is_creator',
                    'is_executor',
                    'number_phone',
                )
            },
        )
    )


admin.site.register(CustomUser, CustomUserAdmin)
