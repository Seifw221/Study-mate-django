# users/urls.py
from django.urls import path
from .views import RegisterUserAPIView , UserProfileAPIView
from users import views # تأكد من أن هذا الاستيراد صحيح

urlpatterns = [
    path('token/', views.CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('students/', RegisterUserAPIView.as_view(), name='student_list_create'),  # POST (Register) + GET (List all students)

    # New Endpoint: To get the currently authenticated user's profile
    path('profile/', UserProfileAPIView.as_view(), name='user_profile'), # <<< هذا هو الـ Endpoint الجديد

    # Existing Endpoint: To get/patch a user profile by ID (might require admin/staff permissions)
    path('students/<int:user_id>/', UserProfileAPIView.as_view(), name='student_update'),  # GET (specific student) + PATCH

]