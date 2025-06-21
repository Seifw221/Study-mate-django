# schedules/serializer.py
from rest_framework import serializers
from .models import Schedule

class ScheduleSerializer(serializers.ModelSerializer):
    image_url = serializers.SerializerMethodField() # هذا سيظل موجوداً لجلب الـ URL للصورة

    class Meta:
        model = Schedule
        # سنحدد الحقول صراحة بدلاً من '__all__' للتأكد من المعالجة الصحيحة
        fields = ['id', 'stage', 'schedule_type', 'image_url', 'title', 'uploaded_at'] # تأكد من أن 'title' موجود في موديل Schedule لو هتستخدمه
                                                                                       # وإذا لم يكن، قم بإزالته.
                                                                                       # أيضا، حقل 'department' لا يوجد في المودل الخاص بك.

    def get_image_url(self, obj):
        request = self.context.get('request')
        if obj.image and hasattr(obj.image, 'url'):
            if request:
                return request.build_absolute_uri(obj.image.url)
            return obj.image.url # ارجع المسار النسبي إذا لم يكن request متاحاً
        return None