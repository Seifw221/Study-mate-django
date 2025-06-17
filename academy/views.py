from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.parsers import MultiPartParser, FormParser
from project.shortcuts import IsAuth, has_permission
from .models import Course, CoursePDF
from .serializer import CourseSerializer, CoursePDFSerializer


class CourseListCreateAPIView(APIView):
    def get(self, request):
        courses = Course.objects.all()
        serializer = CourseSerializer(courses, many=True, context={'request': request})
        return Response(serializer.data)

    def post(self, request):
        if not IsAuth(request):
            return Response({"detail": "Authentication required"}, status=401)
        if not has_permission("academy.change_course", request):
            return Response({"detail": "Permission denied"}, status=403)
        serializer = CourseSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            course = serializer.save()
            return Response(CourseSerializer(course, context={'request': request}).data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CourseDetailAPIView(APIView):
    def get_object(self, pk):
        return get_object_or_404(Course, pk=pk)

    def get(self, request, pk):
        course = self.get_object(pk)
        serializer = CourseSerializer(course, context={'request': request})
        return Response(serializer.data)

    def put(self, request, pk):
        course = self.get_object(pk)
        serializer = CourseSerializer(course, data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, pk):
        if not IsAuth(request):
            return Response({"detail": "Authentication required"}, status=401)
        if not has_permission("academy.change_course", request):
            return Response({"detail": "Permission denied"}, status=403)
        course = self.get_object(pk)
        serializer = CourseSerializer(course, data=request.data, partial=True, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        if not IsAuth(request):
            return Response({"detail": "Authentication required"}, status=401)
        if not has_permission("academy.change_course", request):
            return Response({"detail": "Permission denied"}, status=403)
        course = self.get_object(pk)
        course.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class CoursePDFListCreateAPIView(APIView):
    parser_classes = (MultiPartParser, FormParser)  # For file upload
   
    def get(self, request, course_id):
        pdfs = CoursePDF.objects.filter(course__id=course_id)
        serializer = CoursePDFSerializer(pdfs, many=True, context={'request': request})
        return Response(serializer.data)

    def post(self, request, course_id):
        if not IsAuth(request):
            return Response({"detail": "Authentication required"}, status=401)
        if not has_permission("academy.change_course", request):
            return Response({"detail": "Permission denied"}, status=403)
        files = request.FILES.getlist('pdf_file')  # multiple files
        created_pdfs = []

        for f in files:
            data = {'course': course_id, 'pdf_file': f}
            serializer = CoursePDFSerializer(data=data, context={'request': request})
            if serializer.is_valid():
             pdf_instance = serializer.save()
             created_pdfs.append(CoursePDFSerializer(pdf_instance, context={'request': request}).data)  
   
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        return Response(created_pdfs, status=status.HTTP_201_CREATED)


class CoursePDFDeleteAPIView(APIView):
    def delete(self, request, pdf_id):
        if not IsAuth(request):
            return Response({"detail": "Authentication required"}, status=401)
        if not has_permission("academy.change_course", request):
            return Response({"detail": "Permission denied"}, status=403)
        pdf = get_object_or_404(CoursePDF, id=pdf_id)
        pdf.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

