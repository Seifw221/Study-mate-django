# tests/urls.py (معدل)
from django.urls import path
from .views import TestListCreateAPIView, TestDetailAPIView # استيراد الـ View الجديدة

urlpatterns = [
    path('assignments/', TestListCreateAPIView.as_view(), name='assignment-list-create'), # ممكن نغيرها من 'test' لـ 'assignments'
    path('assignments/<int:pk>/', TestDetailAPIView.as_view(), name='assignment-detail'), # لـ Retrieve, Update, Destroy
]