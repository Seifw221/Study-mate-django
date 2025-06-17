# tests/urls.py

from django.urls import path
from .views import TestListCreateAPIView

urlpatterns = [
    path('test/', TestListCreateAPIView.as_view(), name='test-list-create'),
    path('<int:test_id>/', TestListCreateAPIView.as_view(), name='test-patch'),
]
