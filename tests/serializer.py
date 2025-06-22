# tests/serializers.py (معدل)
from rest_framework import serializers
from .models import Test
from academy.serializer import CourseSerializer # عشان نجيب تفاصيل الكورس المرتبط

class TestSerializer(serializers.ModelSerializer):
    # دي عشان لما تجيب الـ Test، تجيب معاه بيانات الكورس كاملة
    # read_only عشان متقدرش تعدل الكورس من TestSerializer
    # وممكن تستخدم StringRelatedField لو عايز بس اسم الكورس/الدكتور
    course_details = CourseSerializer(source='course', read_only=True)

    class Meta:
        model = Test
        fields = ['id', 'course', 'title', 'description', 'due_date', 'deadline', 'type', 'link', 'course_details']
        # 'course' هنا عشان لما تعمل POST/PUT/PATCH تبعت الـ ID بتاع الكورس
        # 'course_details' عشان لما تعمل GET يجيلك بيانات الكورس كاملة