# tests/views.py (معدل)
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAdminUser # ممكن تستخدمهم
from .models import Test
from .serializer import TestSerializer
from project.shortcuts import IsAuth, has_permission # استخدام الـ shortcuts بتاعتك
from rest_framework.exceptions import PermissionDenied # <--- أضف هذا الاستيراد





# ... بقية الـ Views بتاعتك زي ما هي ...


# View لجلب كل الـ tests أو إنشاء test جديد
class TestListCreateAPIView(ListCreateAPIView):
    queryset = Test.objects.all()
    serializer_class = TestSerializer
    # permission_classes = [IsAuthenticatedOrReadOnly] # مثال على الصلاحيات

    def get_queryset(self):
        # هنا ممكن تضيف فلترة لو عايز تجيب tests لكورس معين أو user معين
        # مثلاً لو عايز تجيب tests لكورس معين:
        # course_id = self.request.query_params.get('course_id')
        # if course_id:
        #     return Test.objects.filter(course_id=course_id)
        return Test.objects.all()

    def perform_create(self, serializer):
        # هنا بتضيف الـ permission check اللي عندك
        if not IsAuth(self.request) or not has_permission("academy.change_course", self.request):
            raise PermissionDenied("Authentication or permission denied")
        serializer.save()

# View لجلب test واحد، تحديثه، أو حذفه
class TestDetailAPIView(RetrieveUpdateDestroyAPIView):
    queryset = Test.objects.all()
    serializer_class = TestSerializer
    lookup_field = 'pk' # عشان تستخدم الـ ID في الـ URL زي /api/tests/1/

    def perform_update(self, serializer):
        if not IsAuth(self.request) or not has_permission("academy.change_course", self.request):
            raise PermissionDenied("Authentication or permission denied")
        serializer.save()

    def perform_destroy(self, instance):
        if not IsAuth(self.request) or not has_permission("academy.change_course", self.request):
            raise PermissionDenied("Authentication or permission denied")
        instance.delete()