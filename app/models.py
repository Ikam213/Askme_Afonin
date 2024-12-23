from django.db import models
from django.contrib.auth.models import User
from django.db.models import Count
from django.utils import timezone

class QuestionManager(models.Manager):
    def new_questions(self):
        return self.order_by("-created_at")
   
    def hot_questions(self):
        return self.annotate(likes=Count("questionlike")).order_by("-likes")

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    avatar = models.ImageField(null = True, blank = True)

    def __str__(self):
        return self.user.username

class Question(models.Model):
    user = models.ForeignKey(Profile, on_delete=models.CASCADE)
    title = models.CharField(max_length=50)
    body = models.TextField(max_length=1000)
    created_at = models.DateTimeField(default=timezone.now)
    tags = models.ManyToManyField("Tag", related_name="questions", blank = True)

    objects = QuestionManager()

    def __str__(self):
        return self.title

class QuestionLike(models.Model):
    user = models.ForeignKey(Profile, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)

    class Meta:
        unique_together = ("user", "question")

class Answer(models.Model):
    user = models.ForeignKey(Profile, on_delete=models.CASCADE)
    title = models.CharField(max_length=50)
    body = models.TextField(max_length=1000)
    created_at = models.DateTimeField(default=timezone.now)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)

    def __str__(self):
        return self.title

class AnswerLike(models.Model):
    user = models.ForeignKey(Profile, on_delete=models.CASCADE)
    answer = models.ForeignKey(Answer, on_delete=models.CASCADE)

    class Meta:
        unique_together = ("user", "answer")

class Tag(models.Model):
    tag_title = models.CharField(max_length=20)

    def __str__(self):
        return self.tag_title

class Like(models.Model):
    user = models.ForeignKey(Profile, on_delete=models.CASCADE)
    answer = models.ForeignKey(Answer, on_delete=models.CASCADE)
