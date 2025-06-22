# schedules/serializer.py

from rest_framework import serializers
from .models import Schedule

class ScheduleSerializer(serializers.ModelSerializer):
    image = serializers.ImageField(use_url=True)

    class Meta:
        model = Schedule
        # ** إضافة 'department' هنا **
        fields = ['id', 'stage', 'schedule_type', 'image', 'title', 'uploaded_at', 'department']