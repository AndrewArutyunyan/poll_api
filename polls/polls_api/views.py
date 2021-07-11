import datetime
from django.contrib.auth.models import User
from django.utils.timezone import get_default_timezone
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import authentication, permissions, status, viewsets, generics
from .models import Poll, Question, Choice, Answer, Participant
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
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user.is_superuser


class IsAdminOrPostOnly(permissions.BasePermission):
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
        if request.method == 'POST':
            return True
        return request.user.is_superuser


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


class AnswerViewSet(viewsets.ModelViewSet):
    """
    list:
    Return a list of all answers of users

    create:
    post an answer on question
    """
    queryset = Answer.objects.all()
    serializer_class = serializers.AnswerSerializer
    permission_classes = [IsAdminOrPostOnly]

    def perform_create(self, serializer):
        """
        Create an answer
        :param serializer: AnswerSerializer
        :return: AnswerSerializer
        """
        serializer.is_valid()
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
    get:
    Returns all participants in all polls
    """

    def get(self, request):
        """
        Return only answers related to the question
        :return: queryset of answers on the question
        """
        queryset = Participant.objects.all()
        serializer = serializers.ParticipantSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class UserView(APIView):
    """
    get:
    Returns all answers of the participant

    patch:
    Change user data
    """

    def get(self, request, user_id):
        """
        Return only answers related to the question
        """
        queryset = Participant.objects.filter(user_id=user_id)
        if queryset.count() < 1:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = serializers.ParticipantSerializer(queryset.last())
        return Response(serializer.data)

    def patch(self, request, user_id):
        """
        Change name or email
        """
        if request.data.get('answers') or request.data.get('user_id'):
            return Response(status=status.HTTP_403_FORBIDDEN)
        queryset = Participant.objects.filter(user_id=user_id)
        if queryset.count() < 1:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = serializers.ParticipantSerializer(queryset.last(), data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(data=serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)