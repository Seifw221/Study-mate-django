from rest_framework import serializers
from .models import Course, CoursePDF


class CoursePDFSerializer(serializers.ModelSerializer):
    pdf_file = serializers.FileField(use_url=True)

    class Meta:
        model = CoursePDF
        fields = ['id', 'course', 'pdf_file']


class CourseSerializer(serializers.ModelSerializer):
    pdfs = CoursePDFSerializer(many=True, read_only=True)

    class Meta:
        model = Course
        fields = ['id', 'name', 'doctor', 'department', 'credit_hours', 'pdfs', 'students', 'course_description', 'image_url'] # <--- هذا هو الحقل الناقص الذي يجب إضافته