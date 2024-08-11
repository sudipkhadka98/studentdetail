from django.db import models
from django.contrib.auth.models import User

class Student(models.Model):
    MALE='MALE'
    FEMALE='FEMALE'
    GENDER_CHOICES = [
        (MALE, 'male'),
        (FEMALE, 'female'),
    ]
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    rollno = models.PositiveIntegerField()
    firstname = models.CharField(max_length=10)
    lastname = models.CharField(max_length=10)
    address = models.CharField(max_length=30)
    phone = models.PositiveIntegerField()
    gender = models.CharField(max_length=6, choices=GENDER_CHOICES)

# Create your models here.
    def __str__(self) -> str:
        return self.title