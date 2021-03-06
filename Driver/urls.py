"""Driver URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from django.urls import path
from drive_safe.views import *

from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

schema_view = get_schema_view(
    openapi.Info(
        title="Snippets API",
        default_version='v1',
        description="Test description",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="contact@snippets.local"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path('admin/', admin.site.urls),
    url(r'^advices/$', AdviceList.as_view(), name="advices"),
    url(r'^advices/(?P<advice_id>(\d)+)$', AdviceDetail.as_view(), name="advice_detail"),
    url(r'^advices/tag/(?P<tag_id>(\d)+)$', AdviceTagList.as_view()),
    url(r'^advices/test/(?P<advice_id>(\d)+)$', AdviceTest.as_view()),
    url(r'^forum_questions/$', ForumQuestionList.as_view(), name="forum_questions"),
    url(r'^forum_questions/(?P<question_id>(\d)+)$', ForumQuestionDetail.as_view(), name='forum_question_detail'),
    url(r'^forum_answers/$', ForumAnswersList.as_view(), name="forum_answers"),
    url(r'^forum_answers/question/(?P<question_id>(\d)+)$', ForumAnswersForQuestion.as_view()),
    url(r'^forum_answers/(?P<answer_id>(\d)+)$', ForumAnswersDetail.as_view()),
    url(r'^new_user/$', UserRegistration.as_view(), name="new_user"),
    url(r'^user_info/(?P<user_id>(\d)+)$', GetUserInfo.as_view()),
    url(r'^test_check/(?P<user_id>(\d)+)/(?P<advice_id>(\d)+)$', TestCheck.as_view()),
    url(r'^swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    url(r'^swagger/$', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    url(r'^redoc/$', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]
