from rest_framework import serializers
from .models import Course, CoursePDF

class CoursePDFSerializer(serializers.ModelSerializer):
    pdf_file = serializers.SerializerMethodField()

    def get_pdf_file(self, obj):
        request = self.context.get('request')
        if request is not None:
            return request.build_absolute_uri(obj.pdf_file.url)
        return obj.pdf_file.url

    class Meta:
        model = CoursePDF
        fields = ['id', 'course', 'pdf_file']  # نخلي course يظهر في حالة الاستخدام المباشر


class CourseSerializer(serializers.ModelSerializer):
    pdfs = CoursePDFSerializer(many=True, read_only=True)

    class Meta:
        model = Course
        fields = ['id', 'name', 'doctor', 'department', 'credit_hours', 'pdfs','students','course_description']
