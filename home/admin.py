from django.contrib import admin

from .models import *


class QuizAdmin(admin.ModelAdmin):
    list_display = ('query',)
    model = Quiz

class BrainstormAdmin(admin.ModelAdmin):
    list_display = ('query',)
    model = BrainstormData

admin.site.register(Quiz, QuizAdmin)
admin.site.register(BrainstormData, BrainstormAdmin)
