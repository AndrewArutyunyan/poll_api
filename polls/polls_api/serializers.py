from abc import ABC

from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Poll, Question, Answer, Choice


# class PollSerializer(serializers.Serializer):
#     poll_id = serializers.IntegerField()
#     title = serializers.CharField(max_length=1024)
#     start_date = serializers.DateTimeField()
#     expiration_date = serializers.DateTimeField()
#     description = serializers.CharField(max_length=4096, allow_blank=True)


class ChoiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Choice
        fields = ['question', 'title']


class QuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Question
        fields = '__all__'


class QuestionWithTextInputType(serializers.ModelSerializer):
    class Meta:
        model = Question
        fields = '__all__'


class QuestionWithSingleChoiceType(serializers.ModelSerializer):
    choice = ChoiceSerializer(read_only=True)

    class Meta:
        model = Question
        fields = ['id', 'text', 'type']


class QuestionWithMultipleChoicesType(serializers.ModelSerializer):
    choice = ChoiceSerializer(read_only=True, many=True, allow_null=True)

    class Meta:
        model = Question
        fields = ['id', 'text', 'type', 'choice']


class QuestionDetailSerializer(serializers.ModelSerializer):
    choices = ChoiceSerializer(read_only=True, many=True)

    class Meta:
        model = Question
        fields = ['text', 'type', 'choices']


class PollSerializer(serializers.ModelSerializer):
    class Meta:
        model = Poll
        fields = '__all__'


class PollDetailSerializer(serializers.ModelSerializer):
    questions = QuestionSerializer(many=True, read_only=True)

    class Meta:
        model = Poll
        fields = ['title', 'start_date', 'expiration_date', 'description', 'questions']


class AnswerSerializer(serializers.ModelSerializer):
    # choices = ChoiceSerializer(many=True, read_only=True)

    class Meta:
        model = Answer
        fields = ['question', 'text_input', 'choices', 'user_id', 'date']


class UserSerializer(serializers.ModelSerializer):
    polls = serializers.PrimaryKeyRelatedField(many=True,
                                               queryset=Poll.objects.all())
    answers = AnswerSerializer(many=True, read_only=True)

    class Meta:
        model = User
        fields = ['id', 'first_name', 'last_name', 'polls', 'answers']