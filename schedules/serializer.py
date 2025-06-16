# schedules/serializers.py

from rest_framework import serializers
from .models import Schedule

class ScheduleSerializer(serializers.ModelSerializer):
    image = serializers.SerializerMethodField()

    def get_image(self, obj):
        request = self.context.get('request')
        return request.build_absolute_uri(obj.image.url)

    class Meta:
        model = Schedule
        fields = ['id', 'stage', 'schedule_type', 'image', 'uploaded_at']
