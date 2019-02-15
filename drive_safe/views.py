from django.http import Http404
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from drive_safe.models import *
from drive_safe.serializers import *


# *** Advices & Tests *** #

class AdviceList(APIView):
    """
    Return list of all advices sorted by creation date.
    """

    def get(self, request, format=None):
        advices = Advice.objects.all().order_by("date_added")
        serializer = AdviceSerializer(advices, many=True)
        return Response(serializer.data)


class AdviceTagList(APIView):
    """
    Return list of advices matching to given tag id.
    """

    def get(self, request, tag_id, format=None):
        advices = Advice.objects.filter(tags=tag_id)
        serializer = AdviceSerializer(advices, many=True)
        return Response(serializer.data)


def get_advice_object(id):
    try:
        return Advice.objects.get(pk=id)
    except Advice.DoesNotExist:
        raise Http404


class AdviceDetail(APIView):
    """
    Return advice with given id.
    """

    def get(self, request, advice_id, format=None):
        advice = get_advice_object(advice_id)
        serializer = AdviceSerializer(advice)
        return Response(serializer.data)


class AdviceTest(APIView):
    """
    Return test questions for given advice id.
    """

    def get(self, request, advice_id, format=None):
        advice = get_advice_object(advice_id)
        test_questions = advice.testquestions_set.all()
        serializer = TestQuestionsSerializer(test_questions, many=True)
        return Response(serializer.data)


# *** # *** # *** Forum *** # *** # *** #

class ForumQuestionList(APIView):
    """
    get:
    Return a list of all forum questions.

    post:
    Create a new forum question instance.
    """

    def get(self, request, format=None):
        forum_questions = ForumQuestion.objects.all()
        serializer = ForumQuestionsSerializer(forum_questions, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = ForumQuestionsSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


def get_forum_question_object(id):
    try:
        return ForumQuestion.objects.get(pk=id)
    except ForumQuestion.DoesNotExist:
        raise Http404


class ForumQuestionDetail(APIView):
    """
    get:
    Retrieve a forum question instance.

    put:
    Update a forum question instance.

    delete:
    Delete a forum question instance.
    """

    def get(self, request, question_id, format=None):
        forum_question = get_forum_question_object(question_id)
        serializer = ForumQuestionsSerializer(forum_question)
        return Response(serializer.data)

    def put(self, request, question_id, format=None):
        forum_question = get_forum_question_object(question_id)
        serializer = ForumQuestionsSerializer(forum_question, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, question_id, format=None):
        forum_question = get_forum_question_object(question_id)
        forum_question.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class ForumAnswersList(APIView):
    """
    Return a list of all forum answers
    """

    def get(self, request, format=None):
        forum_answers = ForumAnswers.objects.all()
        serializer = ForumAnswersSerializer(forum_answers, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = ForumAnswersSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ForumAnswersForQuestion(APIView):
    """
    Return a list of forum answers for given forum question id
    """

    def get(self, request, question_id, format=None):
        forum_question = get_forum_question_object(question_id)
        forum_answers = forum_question.forumanswers_set.all()
        serializer = ForumAnswersSerializer(forum_answers, many=True)
        return Response(serializer.data)


class ForumAnswersDetail(APIView):
    """
        get:
        Retrieve a forum answer instance.

        put:
        Update a forum answer instance.

        delete:
        Delete a forum answer instance.
        """

    def get_object(self, id):
        try:
            return ForumAnswers.objects.get(pk=id)
        except ForumAnswers.DoesNotExist:
            raise Http404

    def get(self, request, answer_id, format=None):
        forum_answer = self.get_object(answer_id)
        serializer = ForumAnswersSerializer(forum_answer)
        return Response(serializer.data)

    def put(self, request, answer_id, format=None):
        forum_answer = self.get_object(answer_id)
        serializer = ForumAnswersSerializer(forum_answer, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, answer_id, format=None):
        forum_answer = self.get_object(answer_id)
        forum_answer.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


# *** # *** # *** Users *** # *** # *** #

class UserRegistration(APIView):

    def post(self, request, format=None):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
