from django.db import models
from django.db.models import JSONField


class Quiz(models.Model):
    query = models.CharField(max_length=300)
    data = JSONField(null=True, blank=True)

    class Meta:
        db_table = 'quizes'

    def __str__(self):
        return '{}'.format(self.query.title())
    

class BrainstormData(models.Model):
    query = models.CharField(max_length=300)
    data = JSONField(null=True, blank=True)

    class Meta:
        db_table = 'brainstorm_data'

    def __str__(self):
        return '{}'.format(self.query.title())