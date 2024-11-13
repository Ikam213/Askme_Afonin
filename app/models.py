from django.db import models
from django.contrib.auth.models import User

class Person(models.Model):
    username = models.CharField(max_length=20)
   
    def __str__(self):
        return self.username
class Question(models.Model):
    title = models.CharField(max_length=20)
    body = models.TextField(max_length=1000)
    users = models.ForeignKey(Person, on_delete=models.CASCADE)

    def __str__(self):
        return self.title

class Answer(models.Model):
    title = models.CharField(max_length=20)
    body = models.TextField(max_length=1000)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)

    def __str__(self):
        return self.title

class Tag(models.Model):
    tag_title = models.CharField(max_length=20)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)

    def __str__(self):
        return self.tag_title

class Like(models.Model):
    amount = models.IntegerField()
    question = models.ForeignKey(Question, on_delete=models.CASCADE)

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    avatar = models.ImageField(null = True, blank = True)

    def __str__(self):
        return self.user.username
