from django.urls import path, re_path, include
from rest_framework.routers import DefaultRouter
from rest_framework.schemas import get_schema_view
from rest_framework.documentation import include_docs_urls

from . import views

router = DefaultRouter()
router.register(r'poll', views.PollViewSet)
router.register(r'poll/(?P<poll_id>[0-9]+)/question', views.QuestionViewSet)
router.register(r'poll/(?P<poll_id>[0-9]+)/question/(?P<question_id>[0-9]+)/choice', views.ChoicesViewSet)
router.register(r'poll/(?P<poll_id>[0-9]+)/question/(?P<question_id>[0-9]+)/answer', views.AnswerViewSet)

schema_view = get_schema_view(title='Polls API',
                              description='An API to publish polls and collect answers')
app_name = "polls"

urlpatterns = [
    path('api/', include(router.urls)),
    re_path(r'api/user/(?P<user_id>[0-9]+)', views.UserView.as_view()),
    re_path(r'api/user', views.UserListView.as_view()),

    path('schema/', schema_view),
    path('docs/', include_docs_urls(title='Polls API'))
]