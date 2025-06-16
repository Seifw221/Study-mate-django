from django.db import models
from academy.models import Course

class Test(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='tests')
    due_date = models.DateTimeField()
    link = models.URLField()

    def __str__(self):
        return f"Test for {self.course} due on {self.due_date}"
