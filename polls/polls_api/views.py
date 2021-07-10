import datetime
from django.contrib.auth.models import User
from django.utils.timezone import get_default_timezone
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import authentication, permissions, status, viewsets, generics
from .models import Poll, Question, Choice, Answer
from . import serializers


# Permissions
class IsAdminOrReadOnly(permissions.BasePermission):
    """
    Object-level permission to only allow admin to edit it
    """

    def has_permission(self, request, view):
        """
        Read permissions allowed, modify and delete are not
        :param request:
        :param view:
        :return: binary decision
        """
        print(request.method)
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user.is_superuser


class IsAdminOrWriteOnly(permissions.BasePermission):
    """
    Object-level permission to only allow admin to edit it
    """

    def has_permission(self, request, view):
        """
        Read permissions allowed, modify and delete are not
        :param request:
        :param view:
        :param obj:
        :return: binary decision
        """
        print(request.method)
        if request.method == 'GET':
            return request.user.is_superuser
        return True


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
        serializer = serializers.PollSerializer(polls, many=True)
        print("____GET_______GET_____")
        return Response(serializer.data)

    # # Add poll, permission: su only
    # def post(self, request):
    #     if not request.user.is_superuser:
    #         return Response(status=status.HTTP_403_FORBIDDEN)
    #     # json example: {"poll":{"title":"who are you?", "expiration_date":"2021-07-08T00:00:00Z"}}
    #     print("___POST_____POST__")
    #     poll_request = request.data.get('poll')
    #     # create a poll from above data
    #     serializer = PollSerializer(data=poll_request)
    #     if serializer.is_valid(raise_exception=True):
    #         poll_saved = serializer.save()
    #     return Response({"success": "Poll '{}' created".format(poll_saved.title)})
    #
    # # Delete all polls, permission: su only
    # def delete(self, request):
    #     if not request.user.is_superuser:
    #         return Response(status=status.HTTP_403_FORBIDDEN)
    #     print("___DELETE_____DELETE__")
    #     Poll.objects.all().delete()
    #     return Response(status=status.HTTP_204_NO_CONTENT)


class QuestionsView(APIView):
    permission_classes = [permissions.AllowAny]

    def get(self, request, poll_id_requested):
        # find poll by id
        poll_q = Poll.objects.filter(id=poll_id_requested)  # poll QuerySet
        if not poll_q:
            return Response(status=status.HTTP_404_NOT_FOUND)
        else:
            poll = poll_q.first()  # assumes poll id is unique
        # check if expired
        now = datetime.datetime.now(tz=None).replace(tzinfo=get_default_timezone())
        if not request.user.is_superuser and poll.expiration_date < now:
            return Response(status=status.HTTP_404_NOT_FOUND)
        # get all questions in poll
        questions = Question.objects.filter(poll=poll_id_requested)
        # serialize

        questions_serializer = serializers.QuestionWithMultipleChoicesType(questions, many=True)
        # send all questions
        return Response(questions_serializer.data, status=status.HTTP_200_OK)


class ChoicesView(APIView):
    permission_classes = [permissions.AllowAny]


class PollViewSet(viewsets.ModelViewSet):
    """
    list:
    Return a list of all polls that aren't expired

    create:
    Create new poll

    retrieve:
    Return the given poll.

    update:
    Replace poll

    partial_update:
    Change poll fields data

    destroy:
    Delete poll
    """
    queryset = Poll.objects.all()
    serializer_class = serializers.PollSerializer  # for list view
    detail_serializer_class = serializers.PollDetailSerializer  # for detail view
    permission_classes = [IsAdminOrReadOnly]

    def get_serializer_class(self):
        """
        Determines which serializer to use 'list' or 'detail'
        :return: serializer class
        """
        if self.action == 'retrieve':
            if hasattr(self, 'detail_serializer_class'):
                return self.detail_serializer_class
        return super().get_serializer_class()

    def get_queryset(self):
        """
        Restricts the returned queries by filtering
        against a 'expiration_date' query parameter
        :return: queryset of active polls
        """
        queryset = Poll.objects.all()
        now = datetime.datetime.now(tz=None).replace(tzinfo=get_default_timezone())
        queryset = queryset.filter(start_date__lte=now, expiration_date__gt=now)
        return queryset


class QuestionViewSet(viewsets.ModelViewSet):
    """
    retrieve:
    Return the given question with choices.

    list:
    Return a list of all questions
    """
    queryset = Question.objects.all()
    serializer_class = serializers.QuestionSerializer
    detail_serializer_class = serializers.QuestionDetailSerializer
    # detail_serializer_class_text_type = serializers.QuestionWithTextInputType
    # detail_serializer_class_single_type = serializers.QuestionWithSingleChoiceType
    # detail_serializer_class_multiple_type = serializers.QuestionWithMultipleChoicesType
    permission_classes = [IsAdminOrReadOnly]

    def get_serializer_class(self):
        """
        For retrieve action return question choices, using corresponding serializer
        :return: serializer class
        """
        if self.action == 'retrieve':
            if hasattr(self, 'detail_serializer_class'):
                return self.detail_serializer_class
        return super().get_serializer_class()

    def get_queryset(self):
        """
        Returns only questions related to the chosen poll
        :return: queryset of questions of the poll
        """
        queryset = Question.objects.filter(poll=self.kwargs['poll_id'])
        return queryset


class ChoicesViewSet(viewsets.ModelViewSet):
    """
    Return choices for given question.
    """
    queryset = Choice.objects.all()
    serializer_class = serializers.ChoiceSerializer
    permission_classes = [IsAdminOrReadOnly]

    def get_queryset(self):
        """
        Returns only choices related to the question
        :return: queryset of choices of the question
        """
        queryset = Choice.objects.filter(question=self.kwargs['question_id'])
        return queryset


class AnswerView(generics.ListCreateAPIView):
    """
    list:
    Return a list of all answers of users

    create:
    post an answer on question
    """
    queryset = Answer.objects.all()
    serializer_class = serializers.AnswerSerializer
    permission_classes = [IsAdminOrWriteOnly]

    def perform_create(self, serializer):
        """
        Create an answer
        :param serializer: AnswerSerializer
        :return: AnswerSerializer
        """
        serializer.save()

    def get_queryset(self):
        """
        Return only answers related to the question
        :return: queryset of answers on the question
        """
        queryset = Answer.objects.filter(question=self.kwargs['question_id'])
        return queryset


class UserListView(APIView):
    """

    """

    def get(self, request):
        """
        Return only answers related to the question
        :return: queryset of answers on the question
        """
        print(list(Answer.objects.all()))
        return Response(status=status.HTTP_403_FORBIDDEN)


class UserView(APIView):
    """

    """

    def get(self, request, user_id):
        """
        Return only answers related to the question
        :return: queryset of answers on the question
        """
        queryset = Answer.objects.filter(user_id=user_id)
        serializer = serializers.AnswerSerializer(queryset, many=True)
        return Response(serializer.data)

    # Show list of answers, permission: admin only
    # def get(self, request):
    #     now = datetime.datetime.now()
    #     if not request.user.is_superuser:
    #         polls = Poll.objects.filter(start_date__lte=now, expiration_date__gt=now)
    #     else:
    #         polls = Poll.objects.all()
    #     if polls.count() < 1:
    #         return Response("It's empty", status=status.HTTP_204_NO_CONTENT)
    #     serializer = serializers.PollSerializer(polls, many=True)
    #     print("____GET_______GET_____")
    #     return Response(serializer.data)

    # # Publish answer, permission: everyone
    # def post(self, request):
    #     if not request.user.is_superuser:
    #         return Response(status=status.HTTP_403_FORBIDDEN)
    #     # json example: {"poll":{"title":"who are you?", "expiration_date":"2021-07-08T00:00:00Z"}}
    #     print("___POST_____POST__")
    #     poll_request = request.data.get('poll')
    #     # create a poll from above data
    #     serializer = PollSerializer(data=poll_request)
    #     if serializer.is_valid(raise_exception=True):
    #         poll_saved = serializer.save()
    #     return Response({"success": "Poll '{}' created".format(poll_saved.title)})
    #
    # # Delete all polls, permission: su only
    # def delete(self, request):
    #     if not request.user.is_superuser:
    #         return Response(status=status.HTTP_403_FORBIDDEN)
    #     print("___DELETE_____DELETE__")
    #     Poll.objects.all().delete()
    #     return Response(status=status.HTTP_204_NO_CONTENT)
