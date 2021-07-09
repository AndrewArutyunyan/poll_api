import datetime

from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.generics import get_object_or_404
from rest_framework import authentication, permissions, status
from django.contrib.auth.models import User

from .models import Poll, Question
from .serializers import PollSerializer, QuestionSerializer


# User working with polls.
class PollsView(APIView):
    permission_classes = [permissions.AllowAny]

    # Show list of polls
    def get(self, request):
        now = datetime.datetime.now()
        if not request.user.is_superuser:
            polls = Poll.objects.filter(start_date__lte=now, expiration_date__gt=now)
        else:
            polls = Poll.objects.all()
        if polls.count() < 1:
            return Response("It's empty", status=status.HTTP_204_NO_CONTENT)
        serializer = PollSerializer(polls, many=True)
        print("____GET_______GET_____")
        return Response(serializer.data)

    # Add poll, permission: su only
    def post(self, request):
        if not request.user.is_superuser:
            return Response(status=status.HTTP_403_FORBIDDEN)
        # json example: {"poll":{"title":"who are you?", "expiration_date":"2021-07-08T00:00:00Z"}}
        print("___POST_____POST__")
        poll_request = request.data.get('poll')
        # create a poll from above data
        serializer = PollSerializer(data=poll_request)
        if serializer.is_valid(raise_exception=True):
            poll_saved = serializer.save()
        return Response({"success": "Poll '{}' created".format(poll_saved.title)})

    # Delete all polls, permission: su only
    def delete(self, request):
        print("___DELETE_____DELETE__")
        Poll.objects.all().delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class QuestionsView(APIView):
    permission_classes = [permissions.AllowAny]

    def get(self, request, poll_id_requested):
        poll = Poll.objects.filter(id=poll_id_requested)
        if not request.user.is_superuser && s = Poll.objects.filter(start_date__lte=now, expiration_date__gt=now)
        questions = Question.objects.filter(poll=poll_id_requested)
        questions_serializer = QuestionSerializer(questions, many=True)
        return Response(questions_serializer.data, status=status.HTTP_200_OK)