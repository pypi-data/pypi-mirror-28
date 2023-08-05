from datetime import timedelta

from django.db import models
from django.utils import timezone


class Question(models.Model):
    question_text = models.CharField(max_length=256)
    pub_date = models.DateTimeField()

    def __str__(self):
        return self.question_text

    def was_published_recently(self):
        now = timezone.now()
        return now - timedelta(days=1) < self.pub_date < now


class Choice(models.Model):
    choice_text = models.CharField(max_length=256)
    votes = models.IntegerField(default=0)
    question = models.ForeignKey(Question)

    def __str__(self):
        return self.choice_text


class User(models.Model):
    username = models.CharField(max_length=24)
    password = models.CharField(max_length=128)
