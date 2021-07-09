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
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'first_name', 'last_name']


class PollSerializer(serializers.ModelSerializer):
    class Meta:
        model = Poll
        fields = '__all__'

    def create(self, validated_data):
        return Poll.objects.create(**validated_data)


class ChoiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Choice
        fields = ['title']


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
    choice = ChoiceSerializer(read_only=True, many=True)

    class Meta:
        model = Question
        fields = ['id', 'text', 'type']
