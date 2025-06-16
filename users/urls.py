from django.urls import path
from .views import RegisterUserView
from users import views
from .views import get_student_info



urlpatterns = [
    path('token/', views.CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('user/register/', RegisterUserView.as_view(), name='register-user'),
    path('user/update/<int:user_id>/', RegisterUserView.as_view(), name='user-update'),
    path('user/<int:user_id>/', RegisterUserView.as_view(), name='user-info'),
    path('student-info/', get_student_info, name='student_info')
]


