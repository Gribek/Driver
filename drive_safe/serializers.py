from rest_framework import serializers
from drive_safe.models import *


class AdviceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Advice
        exclude = ('passed_by', 'likes')
        depth = 1


class TestQuestionsSerializer(serializers.ModelSerializer):
    class Meta:
        model = TestQuestions
        exclude = ('advice',)


class ForumQuestionsSerializer(serializers.ModelSerializer):
    class Meta:
        model = ForumQuestion
        fields = "__all__"


class ForumAnswersSerializer(serializers.ModelSerializer):
    class Meta:
        model = ForumAnswers
        fields = "__all__"


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    def create(self, validated_data):
        user = User.objects.create(
            username=validated_data['username']
        )
        user.set_password(validated_data['password'])
        user.save()

        return user

    class Meta:
        model = User
        fields = ("id", "username", "password",)

