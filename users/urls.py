from django.urls import path
from .views import RegisterUserAPIView  , UserProfileAPIView
from users import views



urlpatterns = [
    path('token/', views.CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('students/', RegisterUserAPIView.as_view(), name='student_list_create'),  # POST + GET
    path('students/<int:user_id>/', UserProfileAPIView.as_view(), name='student_update'),  # GET + PATCH


]

