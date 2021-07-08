from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.parsers import JSONParser
from rest_framework import authentication, permissions, status
from django.contrib.auth.models import User

from .models import Poll, Question
from .serializers import PollSerializer


# Create your views here.
class PollsView(APIView):
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.AllowAny]

    def get(self, request, poll_id_requested=None):
        if poll_id_requested is None:
            polls = Poll.objects.all()
        else:
            print("POLL_ID GRANTED")
            polls = Poll.objects.filter(id=poll_id_requested)
            if polls.count() < 1:
                return Response("No such poll", status=status.HTTP_404_NOT_FOUND)
        if polls.count() < 1:
            return Response("It's empty",status=status.HTTP_204_NO_CONTENT)
        serializer = PollSerializer(polls, many=True)
        print("____GET_______GET_____")
        print(serializer.data)
        return Response(serializer.data)

    def post(self, request):

        # json example: {"poll":{"title":"who are you?", "expiration_date":"2021-07-08T00:00:00Z"}}
        print("___POST_____POST__")
        poll_request = request.data.get('poll')

        # create a poll from above data
        serializer = PollSerializer(data=poll_request)
        if serializer.is_valid(raise_exception=True):
            poll_saved = serializer.save()
        return Response({"success": "Poll '{}' created".format(poll_saved.title)})

    def delete(self, request, poll_id_requested=None):
        print("___DELETE_____DELETE__")
        if poll_id_requested is None:
            polls_to_delete = Poll.objects.all()
        else:
            print("POLL_ID GRANTED")
            polls_to_delete = Poll.objects.filter(id=poll_id_requested)
            if polls_to_delete.count() < 1:
                return Response("No such poll", status=status.HTTP_404_NOT_FOUND)
        polls_to_delete.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


