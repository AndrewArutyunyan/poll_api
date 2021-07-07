from abc import ABC

from rest_framework import serializers
from .models import Poll, Question, Answer, Choice


# class PollSerializer(serializers.Serializer):
#     poll_id = serializers.IntegerField()
#     title = serializers.CharField(max_length=1024)
#     start_date = serializers.DateTimeField()
#     expiration_date = serializers.DateTimeField()
#     description = serializers.CharField(max_length=4096, allow_blank=True)

class PollSerializer(serializers.ModelSerializer):
    #questions = serializers.PrimaryKeyRelatedField(allow_null=True, many=True, queryset=Question.objects.all())

    class Meta:
        model = Poll
        fields = '__all__'
        #read_only_fields = ('poll_id', 'start_date')

    def create(self, validated_data):
        return Poll.objects.create(**validated_data)


class QuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Question
        fields = '__all__'
