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

urlpatterns = [
    path('admin/', admin.site.urls),
    url(r'^advices/$', AdviceList.as_view()),
    url(r'^advices/(?P<advice_id>(\d)+)$', AdviceDetail.as_view()),
    url(r'^advices/tag/(?P<tag_id>(\d)+)$', AdviceTagList.as_view()),
    url(r'^advices/test/(?P<advice_id>(\d)+)$', AdviceTest.as_view()),
    url(r'^forum_questions/$', ForumQuestionList.as_view()),
    url(r'^forum_questions/(?P<question_id>(\d)+)$', ForumQuestionDetail.as_view()),
    url(r'^forum_answers/$', ForumAnswersList.as_view()),
    url(r'^forum_answers/question/(?P<question_id>(\d)+)$', ForumAnswersForQuestion.as_view()),
    url(r'^forum_answers/(?P<answer_id>(\d)+)$', ForumAnswersDetail.as_view()),
]
