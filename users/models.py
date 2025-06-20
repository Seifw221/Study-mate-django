# models.py
from django.contrib.auth.models import AbstractUser
from django.db import models # <<< تأكد من وجود هذا الاستيراد

class CustomUser(AbstractUser):
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

    email = models.EmailField(unique=True)
    username = models.CharField(max_length=150) # هذا الحقل ما زال موجوداً
    is_active = models.BooleanField(default=True)

    # بيانات الطالب
    full_name = models.CharField(max_length=100)
    department = models.CharField(max_length=100, choices=DEPARTMENT_CHOICES)
    academic_year = models.CharField(max_length=20, choices=ACADEMIC_YEAR_CHOICES)

    USERNAME_FIELD = 'email' # << هذا هو الأهم ويجعل الإيميل هو حقل تسجيل الدخول
    REQUIRED_FIELDS = ['username'] # هذا يعني أن 'username' مطلوب عند إنشاء Superuser أو باستخدام بعض الفورمات

    def __str__(self):
        return self.email