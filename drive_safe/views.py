from django.http import Http404, JsonResponse
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
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


def get_forum_question_object(question_id):
    try:
        return ForumQuestion.objects.get(pk=question_id)
    except ForumQuestion.DoesNotExist:
        raise Http404


class AdviceList(GenericAPIView):
    """
    Return list of all advices sorted by creation date.
    """

    serializer_class = AdviceSerializer
    queryset = Advice.objects.all().order_by("date_added")

    def get(self, request, format=None):
        advices = self.get_queryset()
        serializer = self.serializer_class(advices, many=True)
        return Response(serializer.data)


class AdviceTagList(GenericAPIView):
    """
    Return list of advices matching to given tag id.
    """

    serializer_class = AdviceSerializer
    queryset = Advice.objects.all()

    def get(self, request, tag_id, format=None):
        advices = self.get_queryset().filter(tags=tag_id)
        serializer = self.serializer_class(advices, many=True)
        return Response(serializer.data)


class AdviceDetail(GenericAPIView):
    """
    Return advice with given id.
    """

    serializer_class = AdviceSerializer

    def get(self, request, advice_id, format=None):
        advice = get_advice_object(advice_id)
        serializer = self.serializer_class(advice)
        return Response(serializer.data)


class AdviceTest(GenericAPIView):
    """
    Return test questions for given advice id.
    """

    serializer_class = TestQuestionsSerializer
    queryset = ''

    def get(self, request, advice_id, format=None):
        advice = get_advice_object(advice_id)
        test_questions = advice.testquestions_set.all()
        serializer = self.serializer_class(test_questions, many=True)
        return Response(serializer.data)


class TestCheck(GenericAPIView):
    """
    Checks the received answers to test questions.
    Add points for the test.
    """

    serializer_class = TestAnswerSerializer

    def post(self, request, user_id, advice_id, format=None):
        serializer = self.serializer_class(data=request.data, many=True)
        if serializer.is_valid():
            advice = get_advice_object(advice_id)
            user = get_user(user_id)
            # check if the user has not passed this test before
            if TestPassed.objects.filter(user=user, advice=advice).exists():
                return JsonResponse({'error message': 'Test already passed'},
                                    status=status.HTTP_400_BAD_REQUEST)

            test_questions = advice.testquestions_set.all()
            number_of_questions = len(test_questions)
            number_of_answers = len(serializer.validated_data)
            if not number_of_questions == number_of_answers:
                return JsonResponse({'message': 'Wrong number of answers'},
                                    status=status.HTTP_400_BAD_REQUEST)

            number_of_correct_answers = 0
            incorrect_answers = {'incorrect_answers': []}
            for element in serializer.validated_data:
                question_id = element['question_id']
                user_answer = element['question_answer']
                try:
                    # check if this question belong to this test
                    question = test_questions.get(
                        id=question_id)
                    # remove once checked question from question pool
                    test_questions = test_questions.exclude(
                        id=question_id)
                except TestQuestions.DoesNotExist:
                    return JsonResponse(
                        {'message': 'Question does not belong to the test'},
                        status=status.HTTP_400_BAD_REQUEST
                    )
                correct_answer = question.correct_answer
                if correct_answer.upper() == user_answer.upper():
                    number_of_correct_answers += 1
                else:
                    incorrect_answers["incorrect_answers"].append(question_id)

            if number_of_correct_answers == number_of_questions:
                TestCheck.add_points_to_user(user, advice)
                test_passed = TestPassed.objects.create(user=user,
                                                        advice=advice)
                result_serializer = TestPassedSerializer(test_passed)
                return Response(result_serializer.data,
                                status=status.HTTP_201_CREATED)
            else:
                result_serializer = TestFailedSerializer(incorrect_answers)
                return Response(result_serializer.data,
                                status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @staticmethod
    def add_points_to_user(user, advice):
        points_to_add = advice.test_points
        user_score_instance = user.user_score
        user_score_instance.score += points_to_add
        user_score_instance.save()
        return None


class ForumQuestionList(GenericAPIView):
    """
    get:
    Return a list of all forum questions.

    post:
    Create a new forum question instance.
    """

    serializer_class = ForumQuestionsSerializer
    queryset = ForumQuestion.objects.all()

    def get(self, request, format=None):
        forum_questions = self.get_queryset()
        serializer = self.serializer_class(forum_questions, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ForumQuestionDetail(GenericAPIView):
    """
    get:
    Retrieve a forum question instance.

    put:
    Update a forum question instance.

    delete:
    Delete a forum question instance.
    """

    serializer_class = ForumQuestionsSerializer

    def get(self, request, question_id, format=None):
        forum_question = get_forum_question_object(question_id)
        serializer = self.serializer_class(forum_question)
        return Response(serializer.data)

    def put(self, request, question_id, format=None):
        forum_question = get_forum_question_object(question_id)
        serializer = self.serializer_class(forum_question,
                                           data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, question_id, format=None):
        forum_question = get_forum_question_object(question_id)
        forum_question.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class ForumAnswersList(GenericAPIView):
    """
    get:
    Return a list of all forum answers

    post:
    Create a new forum answer instance.
    """

    serializer_class = ForumAnswersSerializer
    queryset = ForumAnswers.objects.all()

    def get(self, request, format=None):
        forum_answers = self.get_queryset()
        serializer = self.serializer_class(forum_answers, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ForumAnswersForQuestion(GenericAPIView):
    """
    Return a list of forum answers for given forum question id
    """

    serializer_class = ForumAnswersSerializer
    queryset = ''

    def get(self, request, question_id, format=None):
        forum_question = get_forum_question_object(question_id)
        forum_answers = forum_question.forumanswers_set.all()
        serializer = self.serializer_class(forum_answers, many=True)
        return Response(serializer.data)


class ForumAnswersDetail(GenericAPIView):
    """
        get:
        Retrieve a forum answer instance.

        put:
        Update a forum answer instance.

        delete:
        Delete a forum answer instance.
        """

    serializer_class = ForumAnswersSerializer

    def get_answer_object(self, id):
        try:
            return ForumAnswers.objects.get(pk=id)
        except ForumAnswers.DoesNotExist:
            raise Http404

    def get(self, request, answer_id, format=None):
        forum_answer = self.get_answer_object(answer_id)
        serializer = self.serializer_class(forum_answer)
        return Response(serializer.data)

    def put(self, request, answer_id, format=None):
        forum_answer = self.get_answer_object(answer_id)
        serializer = self.serializer_class(forum_answer, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, answer_id, format=None):
        forum_answer = self.get_answer_object(answer_id)
        forum_answer.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class UserRegistration(GenericAPIView):
    """
    Registration of a new user
    """

    serializer_class = UserRegistrationSerializer

    def post(self, request, format=None):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            new_user = serializer.save()
            UserScore.objects.create(user=new_user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class GetUserInfo(GenericAPIView):
    """
    Return user id, username and user score with given user id
    """

    serializer_class = UserInfoSerializer

    def get(self, request, user_id, format=None):
        user = get_user(user_id)
        serializer = self.serializer_class(user)
        return Response(serializer.data)
