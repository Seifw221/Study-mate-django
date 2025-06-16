from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)
    username = models.CharField(max_length=150)
    is_active = models.BooleanField(default=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']
    

    def _str_(self):
        return self.email

class StudentInfo(models.Model):
    DEPARTMENT_CHOICES = [
        ('CS', 'Computer Science'),
        ('IT', 'Information Technology'),
        ('IS', 'Information Systems'),
    ]
    ACADEMIC_YEAR_CHOICES = [
        ('1', 'First Year'),
        ('2', 'Second Year'),
        ('3', 'Third Year'),
        ('4', 'Fourth Year'),
    ]
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='studentinfo')
    full_name = models.CharField(max_length=100)
    department = models.CharField(max_length=100, choices=DEPARTMENT_CHOICES)
    academic_year = models.CharField(max_length=20,choices=ACADEMIC_YEAR_CHOICES)    

