# schedules/urls.py (بدون تغيير)

from django.urls import path
from .views import ScheduleListCreateAPIView, ScheduleByStageAndTypeAPIView , ScheduleDetailAPIView

urlpatterns = [
    path('schedules/', ScheduleListCreateAPIView.as_view(), name='schedule-list-create'),
    path('schedules/<int:stage>/<str:schedule_type>/', ScheduleByStageAndTypeAPIView.as_view(), name='schedule-by-stage-type'),
    path('schedules/<int:schedule_id>/', ScheduleDetailAPIView.as_view(), name='schedule-update'),
]