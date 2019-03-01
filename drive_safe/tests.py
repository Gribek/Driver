from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from drive_safe.models import ForumQuestion, User, Advice
from drive_safe.serializers import ForumQuestionsSerializer


class UserTests(APITestCase):
    def test_create_user(self):
        """
        Ensure we can create a new user.
        """
        url = reverse('new_user')
        data = {
            "username": "janek",
            "password": "dferfdv324gfds"
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(User.objects.get().username, "janek")
        return response.data


class AdviceTests(APITestCase):
    def setUp(self):
        self.advice1 = Advice.objects.create(title="test1", text='test', test_points=0)
        self.advice2 = Advice.objects.create(title="test2", text='test', test_points=0)
        self.advice3 = Advice.objects.create(title="test3", text='test', test_points=0)

    def test_get_all_advices(self):
        """
            Ensure we can get a list of all advice objects.
        """
        url = reverse('advices')
        data = None
        response = self.client.get(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 3)

    def test_get_advice_by_id(self):
        """
            Ensure we can get an advice object by id.
        """
        url = reverse('advice_detail', args=[self.advice1.id])
        data = None
        response = self.client.get(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data.get('id'), self.advice1.id)


class ForumTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create(username='adam', password='gdssgtrf234ds')
        self.advice = Advice.objects.create(title="test", text='test', test_points=0)
        self.forum_question1 = ForumQuestion.objects.create(text='test1', advice=self.advice, user=self.user)
        self.forum_question2 = ForumQuestion.objects.create(text='test2', advice=self.advice, user=self.user)
        self.forum_question3 = ForumQuestion.objects.create(text='test3', advice=self.advice, user=self.user)
        self.forum_question4 = ForumQuestion.objects.create(text='test4', advice=self.advice, user=self.user)

    def test_create_forum_question(self):
        """
        Ensure we can create a new forum question object.
        """
        url = reverse('forum_questions')
        data = {
            "text": "Question",
            "advice": self.advice.id,
            "user": self.user.id
        }
        response = self.client.post(url, data, format='json')
        new_object_id = response.data.get('id')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(ForumQuestion.objects.count(), 5)
        self.assertEqual(ForumQuestion.objects.get(id=new_object_id).text, 'Question')
        self.assertEqual(ForumQuestion.objects.get(id=new_object_id).advice, Advice.objects.get(id=self.advice.id))
        self.assertEqual(ForumQuestion.objects.get(id=new_object_id).user, User.objects.get(id=self.user.id))

    def test_get_all_forum_questions(self):
        """
        Ensure we can get list of all forum question objects.
        """
        url = reverse('forum_questions')
        data = None
        response = self.client.get(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 4)

    def test_get_forum_question_by_id(self):
        """
            Ensure we can get a forum question object by id.
        """
        url = reverse('forum_question_detail', args=[self.forum_question1.id])
        data = None
        response = self.client.get(url, data, format='json')
        # self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data.get('id'), self.forum_question1.id)

    def test_update_forum_question(self):
        """
            Ensure we can update a forum question object.
        """
        url = reverse('forum_question_detail', args=[self.forum_question1.id])
        data = ForumQuestionsSerializer(self.forum_question1).data
        data.update({'text': 'text changed test'})
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertNotEqual(response.data.get('text'), self.forum_question1.text)

    def test_delete_forum_question(self):
        """
            Ensure we can delete a forum question object.
        """
        url = reverse('forum_question_detail', args=[self.forum_question1.id])
        data = None
        response = self.client.delete(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(ForumQuestion.objects.filter(id=self.forum_question1.id).exists())
