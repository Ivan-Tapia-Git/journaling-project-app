from django.db import models

# Create your models here.

class Topic(models.Model):
    topic_text = models.CharField(max_length=200)
    date_added = models.DateTimeField('date added', auto_now_add=True)

    def __str__(self):
        return self.topic_text


class Entry(models.Model):
    # Links the Entry with the Topic, makes sure it gets deleted.
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE)
    entry_title = models.CharField(max_length=100)
    entry_text = models.CharField(max_length=4000)
    date_added = models.DateTimeField('date added', auto_now_add=True)

    def __str__(self):
        return self.entry_title