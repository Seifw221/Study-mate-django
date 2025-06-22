# courses/models.py
from django.db import models
from cloudinary_storage.storage import MediaCloudinaryStorage
from cloudinary.models import CloudinaryField

class Course(models.Model):
    name = models.CharField(max_length=255)
    doctor = models.CharField(max_length=255)
    department = models.CharField(max_length=255)
    credit_hours = models.IntegerField()
    students = models.IntegerField(null=True, blank=True)
    course_description = models.TextField()
    image_url = models.URLField(max_length=500, blank=True, null=True) # <--- أضف هذا الحقل

    def __str__(self):
        return self.name

class CoursePDF(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='pdfs')
    pdf_file = CloudinaryField(
        resource_type='raw', 
        folder='damanhour/Staff/pdfs',
        blank=True, null=True
        )

    def __str__(self):
        return f"{self.course.name} PDF"