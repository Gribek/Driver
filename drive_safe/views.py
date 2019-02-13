from django.http import Http404
from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from drive_safe.models import *
from drive_safe.serializers import *


class AdviceList(APIView):
    """
    Return list of all advices sorted by creation date
    """

    def get(self, request, format=None):
        advices = Advice.objects.all().order_by("date_added")
        serializer = AdviceSerializer(advices, many=True)
        return Response(serializer.data)


class AdviceTagList(APIView):
    """
    Return list of advices matching to given tag id
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
    Return advice with given id
    """

    def get(self, request, advice_id, format=None):
        advice = get_advice_object(advice_id)
        serializer = AdviceSerializer(advice)
        return Response(serializer.data)


class AdviceTest(APIView):
    """
    Return test questions for given advice
    """

    def get(self, request, advice_id, format=None):
        advice = get_advice_object(advice_id)
        test_questions = advice.testquestions_set.all()
        serializer = TestQuestionsSerializer(test_questions, many=True)
        return Response(serializer.data)
