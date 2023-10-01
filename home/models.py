from django.db import models
from django.db.models import JSONField


class Quiz(models.Model):
    query = models.CharField(max_length=300)
    data = JSONField(null=True, blank=True)

    class Meta:
        db_table = 'quizes'

    def __str__(self):
        return '{}'.format(self.query.title())
    
class TopicData(models.Model):
    topic = models.CharField(max_length=300)
    Googledata = JSONField(null=True, blank=True)
    Redditdata = JSONField(null=True, blank=True)
    Ytdata = JSONField(null=True, blank=True)

    class Meta:
        db_table = 'topic_data'

    def __str__(self):
        return '{}'.format(self.topic.title())