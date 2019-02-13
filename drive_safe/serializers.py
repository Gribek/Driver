from rest_framework import serializers
from drive_safe.models import Advice, Tags, TestQuestions


class AdviceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Advice
        exclude = ('passed_by', 'likes')
        depth = 1


class TestQuestionsSerializer(serializers.ModelSerializer):
    class Meta:
        model = TestQuestions
        exclude = ('advice',)
