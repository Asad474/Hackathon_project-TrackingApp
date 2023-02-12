from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.
class MyUser(AbstractUser):
    email = models.EmailField(unique = True, null = True)

    USERNAME_FIELD = 'email' 
    REQUIRED_FIELDS = ['username']

    def __str__(self) -> str:
        return self.username


class Userprofile(models.Model):
    user = models.OneToOneField(MyUser, on_delete = models.CASCADE)
    height = models.FloatField()
    weight = models.FloatField()
    age = models.IntegerField(null = True)
    gender = models.CharField(max_length = 10)

    def __str__(self) -> str:
        return f'{self.user.username} (age - {self.age})'


class Activity(models.Model):
    user = models.ForeignKey(Userprofile, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    duration = models.IntegerField()
    met = models.FloatField()
    calorie = models.FloatField()

    def __str__(self) -> str:
        return self.name


class Food(models.Model):
    user = models.ForeignKey(Userprofile, on_delete=models.CASCADE)
    food = models.CharField(max_length=100)
    amount = models.IntegerField()
    protein = models.FloatField()
    fat = models.FloatField()
    carbohydrates = models.FloatField()
    calorie = models.FloatField()

    def __str__(self) -> str:
        return self.food