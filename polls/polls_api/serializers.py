from abc import ABC

from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Poll, Question, Answer, Choice, Participant


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
        fields = ['question', 'text_input', 'choices', 'user_id_requested', 'date']

    def validate_choices(self, value):
        question_id = self.initial_data.get('question')
        question = Question.objects.get(id=question_id)
        if question.type == 'TEXT':
            if not self.initial_data.get('text_input'):
                raise serializers.ValidationError(detail='Provide text input to this question')
            return None
        elif question.type == 'SINGLE':
            if len(value) != 1:
                raise serializers.ValidationError(detail='Select one')
        if len(value) < 1: # multi-choice variant
            raise serializers.ValidationError(detail='Select at least one')
        for choice in value:
            if choice.question.id != question.id:
                print(choice.question.id)
                print(question_id)
                raise serializers.ValidationError(detail='Choice do not correspond question')
        return value

    def get_user_id(self, **validated_data):
        user_id_requested = validated_data.get('user_id_requested')
        # check if user exists
        participant_queryset = Participant.objects.filter(user_id=user_id_requested)
        if participant_queryset.count() < 1:
            participant = Participant.objects.create(user_id=user_id_requested)
        else:
            participant = participant_queryset.last()
        validated_data.update(user_id=participant)
        return validated_data

    def create(self, validated_data):
        validated_data = self.get_user_id(**validated_data)
        choices = validated_data.pop('choices')
        answer_object = Answer(**validated_data)
        answer_object.save()
        if choices:
            answer_object.choices.set(choices)
        return answer_object


class ParticipantSerializer(serializers.ModelSerializer):
    answers = AnswerSerializer(many=True, read_only=True, allow_null=True)

    class Meta:
        model = Participant
        fields = ['user_id', 'first_name', 'last_name', 'email', 'answers']
