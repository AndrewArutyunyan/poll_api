from django.urls import path, re_path, include
from rest_framework.routers import DefaultRouter
from rest_framework.schemas import get_schema_view
from rest_framework.documentation import include_docs_urls

from . import views

router = DefaultRouter()
router.register(r'poll', views.PollViewSet)
router.register(r'poll/(?P<poll_id>[0-9]+)/question', views.QuestionViewSet)
router.register(r'poll/(?P<poll_id>[0-9]+)/question/(?P<question_id>[0-9]+)/choice', views.ChoicesViewSet)

schema_view = get_schema_view(title='Polls API',
                              description='An API to publish polls and collect answers')
app_name = "polls"

urlpatterns = [
    path('api/', include(router.urls)),
    re_path(r'poll/(?P<poll_id>[0-9]+)/question/(?P<question_id>[0-9]+)/answer', views.AnswerView.as_view()),
    path('schema/', schema_view),
    path('docs/', include_docs_urls(title='Polls API'))
]

# urlpatterns = [
#     path('polls/', PollsView.as_view()),
#     re_path(r'^polls/poll_(?P<poll_id_requested>[0-9]+)/$', QuestionsView.as_view()),
#     re_path(r'^polls/poll_(?P<poll_id_requested>[0-9]+)/(?P<question_id_requested>[0-9]+)/$', ChoicesView.as_view()),
# ]
