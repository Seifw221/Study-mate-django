# tests/urls.py

from django.urls import path
from .views import TestListCreateAPIView, TestPatchAPIView

urlpatterns = [
    path('test', TestListCreateAPIView.as_view(), name='test-list-create'),
    path('<int:pk>/', TestPatchAPIView.as_view(), name='test-patch'),
]
