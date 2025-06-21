# schedules/views.py
from django.shortcuts import render
from project.shortcuts import IsAuth, has_permission
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Schedule # تأكد أن هذا هو المودل الخاص بك
from .serializer import ScheduleSerializer
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.permissions import IsAuthenticated, AllowAny

class ScheduleListCreateAPIView(APIView):
    # يمكنك إضافة permission_classes إذا لزم الأمر
    parser_classes = [MultiPartParser, FormParser]

    def get(self, request):
        schedules = Schedule.objects.all()
        serializer = ScheduleSerializer(schedules, many=True, context={'request': request})
        return Response(serializer.data)

    def post(self, request):
        if not IsAuth(request):
            return Response({"detail": "Authentication required"}, status=status.HTTP_401_UNAUTHORIZED)
        if not has_permission("schedules.change_schedule", request):
            return Response({"detail": "Permission denied"}, status=status.HTTP_403_FORBIDDEN)
        
        serializer = ScheduleSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ScheduleByStageAndTypeAPIView(APIView):
    permission_classes = [AllowAny] # أو [IsAuthenticated] حسب حاجتك
    
    def get(self, request, stage, schedule_type): # stage سيأتي كرقم، schedule_type كنص (lecture/exam)
        # فلترة الجداول بناءً على stage (رقم) و schedule_type (نص)
        schedules = Schedule.objects.filter(stage=stage, schedule_type=schedule_type)
        
        # لا يوجد فلترة بالـ 'department' هنا، لأن الحقل غير موجود في المودل
        # إذا أردت فلترة بالقسم، يجب إضافة حقل department لنموذج Schedule أولاً
        
        serializer = ScheduleSerializer(schedules, many=True, context={'request': request})
        return Response(serializer.data)


class ScheduleDetailAPIView(APIView):
    permission_classes = [IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser]

    def patch(self, request, schedule_id):
        if not IsAuth(request):
            return Response({"detail": "Authentication required"}, status=status.HTTP_401_UNAUTHORIZED)
        if not has_permission("schedules.change_schedule", request):
            return Response({"detail": "Permission denied"}, status=status.HTTP_403_FORBIDDEN)

        try:
            schedule = Schedule.objects.get(id=schedule_id)
        except Schedule.DoesNotExist:
            return Response({"detail": "Schedule not found."}, status=status.HTTP_404_NOT_FOUND)

        serializer = ScheduleSerializer(schedule, data=request.data, partial=True, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, schedule_id):
        if not IsAuth(request):
            return Response({"detail": "Authentication required"}, status=status.HTTP_401_UNAUTHORIZED)
        if not has_permission("schedules.delete_schedule", request):
            return Response({"detail": "Permission denied"}, status=status.HTTP_403_FORBIDDEN)

        try:
            schedule = Schedule.objects.get(id=schedule_id)
        except Schedule.DoesNotExist:
            return Response({"detail": "Schedule not found."}, status=status.HTTP_404_NOT_FOUND)

        schedule.delete()
        return Response({"detail": "Schedule deleted successfully."}, status=status.HTTP_204_NO_CONTENT)