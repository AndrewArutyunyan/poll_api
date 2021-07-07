from django.db import models
from django.contrib.auth import get_user_model


# models for polls_api

class Poll(models.Model):
    poll_id = models.IntegerField(default=0, unique=True)
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
                             verbose_name='related_poll',
                             on_delete=models.CASCADE)

    def __str__(self):
        return self.text


class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    title = models.CharField(max_length=4096)
    lock_other = models.BooleanField(default=False)

    def __str__(self):
        return self.title


class Answer(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.DO_NOTHING)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    text_input = models.CharField('text answer', max_length=8096, null=True)
    single_choice = models.ForeignKey(Choice,
                                      on_delete=models.CASCADE,
                                      null=True,
                                      related_name='single_choice')
    multi_choice = models.ManyToManyField(Choice,
                                          related_name='one_of_the_choices')
    date = models.DateTimeField(auto_now_add=True)
