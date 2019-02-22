from django.core.exceptions import ObjectDoesNotExist
from django.http import Http404
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from drive_safe.serializers import *
from django.contrib.auth.models import User


def get_user(user_id):
    try:
        user = User.objects.get(id=user_id)
    except User.DoesNotExist:
        raise Http404
    return user


def get_advice_object(advice_id):
    try:
        return Advice.objects.get(pk=advice_id)
    except Advice.DoesNotExist:
        raise Http404


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


class TestCheck(APIView):
    """
    Checks the received answers to test questions.
    Add points for the test.
    """

    def post(self, request, user_id, advice_id, format=None):
        serializer = TestAnswerSerializer(data=request.data, many=True)
        if serializer.is_valid():
            advice = get_advice_object(advice_id)
            user = get_user(user_id)
            advice_test_questions = advice.testquestions_set.all()
            number_of_questions = len(advice_test_questions)
            number_of_answers = len(serializer.validated_data)

            if TestPassed.objects.filter(user=user,
                                         advice=advice).exists():  # check if user passed this test before
                return Response(status=status.HTTP_400_BAD_REQUEST)
            if not number_of_questions == number_of_answers:  # check if number of test answers equals number of test questions
                return Response(status=status.HTTP_400_BAD_REQUEST)

            number_of_correct_answers = 0
            incorrect_answers = {'incorrect_answers': []}
            for element in serializer.validated_data:
                question_id = element['question_id']
                user_answer = element['question_answer']
                try:
                    test_question = advice_test_questions.get(
                        pk=question_id)  # check if this question belong to this test
                    advice_test_questions = advice_test_questions.exclude(
                        id=question_id)  # remove once checked question from question pool
                    correct_answer = test_question.correct_answer
                    if correct_answer.upper() == user_answer.upper():
                        number_of_correct_answers += 1
                    else:
                        incorrect_answers["incorrect_answers"].append(question_id)
                except ObjectDoesNotExist:
                    return Response(status=status.HTTP_400_BAD_REQUEST)

            if number_of_questions == number_of_correct_answers:
                self.add_points_to_user(user, advice)  # add points to the user for the test
                test_passed = TestPassed.objects.create(user=get_user(user_id), advice=advice)
                result_serializer = TestPassedSerializer(test_passed)
                return Response(result_serializer.data, status=status.HTTP_201_CREATED)
            else:
                result_serializer = TestFailedSerializer(incorrect_answers)
                return Response(result_serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def add_points_to_user(self, user, advice):
        points_to_add = advice.test_points
        user_score_instance = user.user_score
        user_points = user_score_instance.score + points_to_add
        user_score_instance.score = user_points
        user_score_instance.save()
        return None


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
    """
    Registration of a new user
    """

    def post(self, request, format=None):
        serializer = UserRegistrationSerializer(data=request.data)
        if serializer.is_valid():
            new_user = serializer.save()
            UserScore.objects.create(user=new_user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class GetUserInfo(APIView):
    """
    Return user id, username and user score with given user id
    """

    def get(self, request, user_id, format=None):
        user = get_user(user_id)
        serializer = UserInfoSerializer(user)
        return Response(serializer.data)
