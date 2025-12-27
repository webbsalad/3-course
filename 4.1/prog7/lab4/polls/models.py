from django.db import models
from django.contrib.auth import get_user_model
from django.utils import timezone


class Question(models.Model):
    question_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField(default=timezone.now)
    author = models.ForeignKey(get_user_model(), null=True, blank=True, on_delete=models.SET_NULL)

    def __str__(self):
        return self.question_text


class Choice(models.Model):
    question = models.ForeignKey(Question, related_name='choices', on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    votes = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.choice_text

from django.db import models

# Create your models here.
