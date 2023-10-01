from django.contrib import admin

from .models import *


class QuizAdmin(admin.ModelAdmin):
    list_display = ('query',)
    model = Quiz

class TopicAdmin(admin.ModelAdmin):
    list_display = ('topic',)
    model = TopicData

admin.site.register(Quiz, QuizAdmin)
admin.site.register(TopicData, TopicAdmin)
