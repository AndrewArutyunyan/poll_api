from django.contrib import admin
from django.forms import TextInput, Textarea
from django.db import models
from .models import Poll, Question, Choice, Answer, Participant


# Register your models here.
class AnswerInline(admin.TabularInline):
    model = Answer
    extra = 0
    formfield_overrides = {
        models.CharField: {'widget': TextInput(attrs={'size': 20})},
        models.TextField: {'widget': Textarea(attrs={'rows': 3, 'cols': 30})}
    }


class ChoiceInline(admin.TabularInline):
    model = Choice
    extra = 0
    formfield_overrides = {
        models.CharField: {'widget': TextInput(attrs={'size': 20})},
        models.TextField: {'widget': Textarea(attrs={'rows': 3, 'cols': 30})}
    }


class QuestionInline(admin.TabularInline):
    model = Question
    extra = 0
    formfield_overrides = {
        models.TextField: {'widget': Textarea(attrs={'rows': 3, 'cols': 50})}
    }


class QuestionAdmin(admin.ModelAdmin):
    list_display = ('text', 'type')
    inlines = [
        ChoiceInline
    ]
    formfield_overrides = {
        models.TextField: {'widget': Textarea(attrs={'rows': 3})}
    }


class PollAdmin(admin.ModelAdmin):
    list_display = ('pk', 'title', 'description')
    inlines = [
        QuestionInline
    ]


class AnswerAdmin(admin.ModelAdmin):
    list_display = ('question', 'text_input', 'date', 'user_id')


class ParticipantAdmin(admin.ModelAdmin):
    inlines = [
        AnswerInline
    ]
    list_display = ('user_id', 'first_name', 'last_name', 'email')


admin.site.register(Poll, PollAdmin)
admin.site.register(Question, QuestionAdmin)
admin.site.register(Answer, AnswerAdmin)
admin.site.register(Participant, ParticipantAdmin)
