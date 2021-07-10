from django.db import models
from django.contrib.auth import get_user_model


# models for polls_api

class Poll(models.Model):
    title = models.CharField(max_length=1024)
    start_date = models.DateTimeField(auto_now_add=True)
    expiration_date = models.DateTimeField()
    description = models.CharField(max_length=4096, blank=True)

    def __str__(self):
        return self.title


ANSWER_TYPES = [
    ('TEXT', 'Free text'),
    ('SINGLE', 'Single choice'),
    ('MULTI', 'Multiple choices')]


class Question(models.Model):
    text = models.TextField('question text', max_length=8192)
    type = models.CharField(max_length=6, choices=ANSWER_TYPES)
    poll = models.ForeignKey(Poll,
                             related_name='questions',
                             on_delete=models.CASCADE)

    def __str__(self):
        return self.text


class Choice(models.Model):
    question = models.ForeignKey(Question,
                                 related_name='choices',
                                 on_delete=models.CASCADE)
    title = models.CharField(max_length=4096)
    lock_other = models.BooleanField(default=False)

    def __str__(self):
        return self.title


class Answer(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    text_input = models.CharField('text answer',
                                  max_length=8096,
                                  null=True)
    choices = models.ManyToManyField(Choice, related_name='answers')
    date = models.DateTimeField(auto_now_add=True)
    user_id = models.IntegerField(default=7)

    class Meta:
        ordering = ['date']
