from django.contrib import admin

from .models import *


class QuizAdmin(admin.ModelAdmin):
    list_display = ('query',)
    model = Quiz

admin.site.register(Quiz, QuizAdmin)
