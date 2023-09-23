from django.contrib import admin

from .models import *


class UserAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'email', 'date_joined', 'is_superuser',)
    model = User


admin.site.register(User, UserAdmin)