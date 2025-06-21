# schedules/models.py
from django.db import models

class Schedule(models.Model):
    STAGE_CHOICES = [
        (1, 'First Year'),
        (2, 'Second Year'),
        (3, 'Third Year'),
        (4, 'Fourth Year'),
    ]

    TYPE_CHOICES = [
        ('lecture', 'Lecture Schedule'),
        ('exam', 'Exam Schedule'),
    ]

    # <<< ده السطر الجديد اللي هتضيفه أو تعدله لو موجود (المفروض تضيفه)
    title = models.CharField(max_length=255, default='Unnamed Schedule') # مثال: عنوان الجدول

    stage = models.IntegerField(choices=STAGE_CHOICES)
    schedule_type = models.CharField(max_length=10, choices=TYPE_CHOICES)
    image = models.ImageField(upload_to='schedules/')

    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        # هنعدل هنا عشان نستخدم الـ title اللي ضفناه
        return f"{self.title} - {self.get_schedule_type_display()} - {self.get_stage_display()}"