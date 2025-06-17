from django.shortcuts import render
from project.shortcuts import IsAuth, has_permission
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Schedule
from .serializer import ScheduleSerializer
from rest_framework.parsers import MultiPartParser, FormParser

class ScheduleListCreateAPIView(APIView):
    parser_classes = [MultiPartParser, FormParser]

    def get(self, request):
        schedules = Schedule.objects.all()
        serializer = ScheduleSerializer(schedules, many=True, context={'request': request})
        return Response(serializer.data)

    def post(self, request):
        if not IsAuth(request):
            return Response({"detail": "Authentication required"}, status=401)
        if not has_permission("schedules.change_schedule", request):
            return Response({"detail": "Permission denied"}, status=403)
        serializer = ScheduleSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ScheduleByStageAndTypeAPIView(APIView):
    def get(self, request, stage, schedule_type):
        schedules = Schedule.objects.filter(stage=stage, schedule_type=schedule_type)
        serializer = ScheduleSerializer(schedules, many=True, context={'request': request})
        return Response(serializer.data)




class ScheduleDetailAPIView(APIView):
    parser_classes = [MultiPartParser, FormParser]

    def patch(self, request, schedule_id):
        if not IsAuth(request):
            return Response({"detail": "Authentication required"}, status=401)
        if not has_permission("schedules.change_schedule", request):
            return Response({"detail": "Permission denied"}, status=403)

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
            return Response({"detail": "Authentication required"}, status=401)
        if not has_permission("schedules.delete_schedule", request):
            return Response({"detail": "Permission denied"}, status=403)

        try:
            schedule = Schedule.objects.get(id=schedule_id)
        except Schedule.DoesNotExist:
            return Response({"detail": "Schedule not found."}, status=status.HTTP_404_NOT_FOUND)

        schedule.delete()
        return Response({"detail": "Schedule deleted successfully."}, status=status.HTTP_204_NO_CONTENT)
