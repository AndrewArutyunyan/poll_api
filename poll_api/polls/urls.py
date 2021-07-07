from django.urls import path, re_path

from .views import PollsView

app_name = "polls"

urlpatterns = [
    path('polls/', PollsView.as_view()),
    re_path(r'^polls/poll_(?P<poll_id_requested>[0-9]+)/$', PollsView.as_view())
]
