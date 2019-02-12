from django.contrib.auth.models import User
from django.db import models


# Create your models here.
class Advice(models.Model):
    title = models.CharField(max_length=128, verbose_name="Tytuł porady")
    text = models.TextField(verbose_name="Tekst porady")
    date_added = models.DateField(auto_now_add=True)
    tags = models.ManyToManyField("Tags", verbose_name="Tagi")
    test_points = models.SmallIntegerField(verbose_name="Ilość pkt za test")
    passed_by = models.ManyToManyField(User, related_name="users_tests_passed")
    likes = models.ManyToManyField(User, related_name="users_likes")

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Poradę"
        verbose_name_plural = "Porady"


class Tags(models.Model):
    name = models.CharField(max_length=32, verbose_name="Nazwa tagu")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Tag"
        verbose_name_plural = "Tagi"


class TestQuestions(models.Model):
    advice = models.ForeignKey(Advice, on_delete=models.CASCADE)
    question_text = models.TextField(verbose_name="Treść pytania")
    answer_a = models.TextField(verbose_name="Odpowiedź A")
    answer_b = models.TextField(verbose_name="Odpowiedź B")
    answer_c = models.TextField(verbose_name="Odpowiedź C")
    correct_answer = models.CharField(max_length=1, verbose_name="Poprawna odpowiedź")

    class Meta:
        verbose_name = "Pytanie testowe"
        verbose_name_plural = "Pytania testowe"


class UserScore(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    score = models.SmallIntegerField(default=0)


class ForumQuestion(models.Model):
    text = models.TextField()
    advice = models.ForeignKey(Advice, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date_added = models.DateField(auto_now_add=True)


class ForumAnswers(models.Model):
    text = models.TextField()
    question = models.ForeignKey(ForumQuestion, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date_added = models.DateField(auto_now_add=True)
