# courses/urls.py
from django.urls import path
from .views import CourseListCreateAPIView, CourseDetailAPIView, CoursePDFListCreateAPIView, CoursePDFDeleteAPIView

urlpatterns = [
    path('courses/', CourseListCreateAPIView.as_view(), name='course-list-create'),
    path('courses/<int:pk>/', CourseDetailAPIView.as_view(), name='course-detail'),
    path('courses/<int:course_id>/pdfs/', CoursePDFListCreateAPIView.as_view(), name='pdf-upload-list'),
    path('pdfs/<int:pdf_id>/delete/', CoursePDFDeleteAPIView.as_view(), name='pdf-delete'),
]


