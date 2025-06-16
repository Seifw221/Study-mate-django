from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.views import TokenObtainPairView
from django.shortcuts import get_object_or_404
from .models import CustomUser, StudentInfo
from .serializers import CustomUserSerializer, CustomTokenObtainPairSerializer
from rest_framework.permissions import AllowAny
from django.views.decorators.csrf import csrf_exempt # استيراد csrf_exempt
from django.utils.decorators import method_decorator # استيراد method_decorator
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from project.shortcuts import IsAuth, has_permission

class RegisterUserView(APIView):
    def post(self, request):
        if not IsAuth(request):
            return Response({"detail": "Authentication required"}, status=401)
        if not has_permission("users.change_user", request):
            return Response({"detail": "Permission denied"}, status=403)
        serializer = CustomUserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request, user_id):
        user = get_object_or_404(CustomUser, id=user_id)
        serializer = CustomUserSerializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def patch(self, request, user_id):
        if not IsAuth(request):
            return Response({"detail": "Authentication required"}, status=401)
        if not has_permission("users.change_user", request):
            return Response({"detail": "Permission denied"}, status=403)
        user = get_object_or_404(CustomUser, id=user_id)
        serializer = CustomUserSerializer(user, data=request.data, partial=True)
        if serializer.is_valid():
            if 'password' in request.data:
                user.set_password(request.data['password'])
                user.save()
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_student_info(request):
    user = request.user
    try:
        student_info = user.studentinfo
        return Response({
            "full_name": student_info.full_name,
            "department": student_info.department,
            "academic_year": student_info.academic_year
        })
    except StudentInfo.DoesNotExist:
        return Response({"error": "Student info not found."}, status=404)

@method_decorator(csrf_exempt, name='dispatch') # إضافة المزخرف هنا
class CustomTokenObtainPairView(TokenObtainPairView):
    permission_classes = [AllowAny]
    serializer_class = CustomTokenObtainPairSerializer

