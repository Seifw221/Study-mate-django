from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Test
from .serializer import TestSerializer
from django.shortcuts import get_object_or_404
from project.shortcuts import IsAuth, has_permission


class TestListCreateAPIView(APIView):
    def get(self, request):
        tests = Test.objects.all()
        serializer = TestSerializer(tests, many=True, context={'request': request})
        return Response(serializer.data)

    def post(self, request):
        if not IsAuth(request):
            return Response({"detail": "Authentication required"}, status=401)
        if not has_permission("academy.change_course", request):
            return Response({"detail": "Permission denied"}, status=403)
        serializer = TestSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            test = serializer.save()
            return Response(TestSerializer(test, context={'request': request}).data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request):
        if not IsAuth(request):
            return Response({"detail": "Authentication required"}, status=401)
        if not has_permission("academy.change_course", request):
            return Response({"detail": "Permission denied"}, status=403)
        test_id = request.data.get('id')
        if not test_id:
            return Response({"detail": "Test ID is required for patch."}, status=400)
        test = get_object_or_404(Test, id=test_id)
        serializer = TestSerializer(test, data=request.data, partial=True, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)
