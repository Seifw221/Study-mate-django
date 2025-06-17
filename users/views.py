from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.views import TokenObtainPairView
from .models import CustomUser
from .serializers import CustomUserSerializer, CustomTokenObtainPairSerializer
from rest_framework.permissions import AllowAny ,IsAuthenticated
from django.views.decorators.csrf import csrf_exempt # استيراد csrf_exempt
from django.utils.decorators import method_decorator # استيراد method_decorator
from rest_framework.parsers import MultiPartParser, FormParser
from project.shortcuts import IsAuth, get_object_or_404, has_permission


class RegisterUserAPIView(APIView):
    parser_classes = [MultiPartParser, FormParser]

    def post(self, request):
        if not IsAuth(request):
            return Response({"detail": "Authentication required"}, status=401)
        
        serializer = CustomUserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    def get(self, request, staff_id=None):
        if staff_id:
            staff = get_object_or_404(CustomUser, id=staff_id)
            serializer = CustomUserSerializer(staff)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            staff_list = CustomUser.objects.all()
            serializer = CustomUserSerializer(staff_list, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)

class UserProfileAPIView(APIView):
    parser_classes = [MultiPartParser, FormParser]

    def get(self, request, user_id):
        user_obj = CustomUser.objects.filter(id=user_id).first()
        if user_obj:
            serializer = CustomUserSerializer(user_obj)
            return Response(serializer.data)
        return Response({'error': 'User not found'}, status=404)

    def patch(self, request, user_id):
        if not IsAuth(request):
            return Response({"detail": "Authentication required"}, status=401)
        if not has_permission("users.change_user", request):
            return Response({"detail": "Permission denied"}, status=403)
        try:
            user_obj = CustomUser.objects.get(id=user_id)
        except CustomUser.DoesNotExist:
            return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)

        serializer = CustomUserSerializer(user_obj, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
@method_decorator(csrf_exempt, name='dispatch') 
class CustomTokenObtainPairView(TokenObtainPairView):
    permission_classes = [AllowAny]
    serializer_class = CustomTokenObtainPairSerializer

