from django.db import models

# Create your models here.
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

    stage = models.IntegerField(choices=STAGE_CHOICES)
    schedule_type = models.CharField(max_length=10, choices=TYPE_CHOICES)
    image = models.ImageField(upload_to='schedules/')

    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.get_schedule_type_display()} - {self.get_stage_display()}"
