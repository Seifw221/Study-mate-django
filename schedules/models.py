# schedules/models.py
from django.db import models

class Schedule(models.Model):
    # Choices for schedule_type (e.g., 'Lectures', 'Exams')
    SCHEDULE_TYPE_CHOICES = [
        ('Lectures', 'Lectures Schedule'),
        ('Exams', 'Exams Schedule'),
    ]

    # Choices for stage (e.g., 'First', 'Second', 'Third', 'Fourth')
    STAGE_CHOICES = [
        ('First', 'First Year'),
        ('Second', 'Second Year'),
        ('Third', 'Third Year'),
        ('Fourth', 'Fourth Year'),
    ]

    # Choices for department (if applicable for certain stages)
    DEPARTMENT_CHOICES = [
        ('General', 'General (No specific department)'), # For years 1 & 2
        ('CS', 'Computer Science'),
        ('IT', 'Information Technology'),
        ('IS', 'Information Systems'),
    ]

    title = models.CharField(max_length=255)
    stage = models.CharField(max_length=20, choices=STAGE_CHOICES)
    schedule_type = models.CharField(max_length=20, choices=SCHEDULE_TYPE_CHOICES)
    department = models.CharField(max_length=100, choices=DEPARTMENT_CHOICES, default='General') # <<< تأكد من وجود هذا الحقل

    # ImageField for the schedule image
    image = models.ImageField(upload_to='schedules_images/', blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.title} - {self.stage} Year - {self.get_schedule_type_display()} - {self.get_department_display()}"

    class Meta:
        # Add a unique_together constraint if you want to ensure only one schedule
        # of a specific type, stage, and department exists.
        # For example, one 'Lectures' schedule for 'Third Year' 'CS' department.
        unique_together = ('stage', 'schedule_type', 'department')
        ordering = ['stage', 'schedule_type', 'department']