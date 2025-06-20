# users/views.py
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.views import TokenObtainPairView
from .models import CustomUser
from .serializers import CustomUserSerializer, CustomTokenObtainPairSerializer
from rest_framework.permissions import AllowAny ,IsAuthenticated
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from rest_framework.parsers import MultiPartParser, FormParser
from project.shortcuts import IsAuth, get_object_or_404, has_permission # تأكد من أن 'project.shortcuts' مسار صحيح


class RegisterUserAPIView(APIView):
    parser_classes = [MultiPartParser, FormParser]

    def post(self, request):
        # التأكد من أن المستخدم الذي يحاول التسجيل غير مجهول (Authenticated)
        # إذا كان التسجيل للمستخدمين الجدد، يجب إزالة IsAuth هنا أو تعديلها
        # لو التسجيل لأي حد، ممكن تخلي permission_classes = [AllowAny]
        if not IsAuth(request):
            return Response({"detail": "Authentication required"}, status=status.HTTP_401_UNAUTHORIZED)

        serializer = CustomUserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # GET method to list all users (students) or get a specific one by staff_id
    def get(self, request, staff_id=None):
        # قد تحتاج صلاحيات هنا أيضاً
        if staff_id:
            staff = get_object_or_404(CustomUser, id=staff_id)
            serializer = CustomUserSerializer(staff)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            staff_list = CustomUser.objects.all()
            serializer = CustomUserSerializer(staff_list, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)

class UserProfileAPIView(APIView):
    # السماح فقط للمستخدمين الذين قاموا بتسجيل الدخول بالوصول لهذه الـ View
    permission_classes = [IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser]

    # GET method to retrieve profile of the currently authenticated user
    def get(self, request, user_id=None): # جعل user_id اختياري
        if user_id: # إذا تم تمرير user_id في الـ URL
            # يمكنك إضافة منطق هنا للسماح للمستخدمين (بصلاحيات معينة) برؤية ملفات تعريف مستخدمين آخرين
            # for now, let's allow fetching by ID only if the ID matches the requesting user or has special permission
            if request.user.id == user_id or request.user.is_staff: # مثال: لو المستخدم هو نفسه أو مدير
                user_obj = get_object_or_404(CustomUser, id=user_id)
                serializer = CustomUserSerializer(user_obj)
                return Response(serializer.data)
            else:
                return Response({'detail': 'Permission denied or user not found'}, status=status.HTTP_403_FORBIDDEN)
        else: # إذا لم يتم تمرير user_id، جلب ملف تعريف المستخدم الحالي
            serializer = CustomUserSerializer(request.user) # استخدام request.user
            return Response(serializer.data)

    def patch(self, request, user_id):
        if not IsAuth(request): # تأكد من منطق IsAuth أو استخدم IsAuthenticated
            return Response({"detail": "Authentication required"}, status=status.HTTP_401_UNAUTHORIZED)

        # التأكد من أن المستخدم الذي يحاول التعديل هو نفسه صاحب الملف الشخصي أو لديه صلاحيات
        user_obj = get_object_or_404(CustomUser, id=user_id)
        if request.user.id != user_obj.id and not request.user.is_staff:
            return Response({"detail": "Permission denied"}, status=status.HTTP_403_FORBIDDEN)

        serializer = CustomUserSerializer(user_obj, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@method_decorator(csrf_exempt, name='dispatch') 
class CustomTokenObtainPairView(TokenObtainPairView):
    permission_classes = [AllowAny]
    serializer_class = CustomTokenObtainPairSerializer