# users/serializers.py (أو accounts/serializers.py)

from rest_framework import serializers
from .models import CustomUser
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.utils.timezone import now
from django.contrib.auth import get_user_model
# from rest_framework import serializers # مكرر

User = get_user_model()

class CustomUserSerializer(serializers.ModelSerializer):
    repeat_password = serializers.CharField(write_only=True)

    class Meta:
        model = CustomUser
        fields = [
            'email',
            'username', # هذا الحقل موجود في الـ User model
            'is_active',
            'full_name',
            'department',
            'academic_year',
            'password',
            'repeat_password',
        ]
        
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def validate(self, data):
        if data['password'] != data['repeat_password']:
            raise serializers.ValidationError("Passwords do not match.")
        return data

    def create(self, validated_data):
        validated_data.pop('repeat_password')
        password = validated_data.pop('password')
        user = CustomUser(**validated_data)
        user.set_password(password)
        user.save()
        return user

# --- التعديل هنا: لجعل TokenObtainPairSerializer يستخدم 'email' ---
class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    # إضافة حقل 'email'
    email = serializers.EmailField(write_only=True)

    # إزالة حقل 'username' من الـ base class
    # هذا ليس ضرورياً إذا كنت تريد الاحتفاظ به كخيار، ولكن للتوضيح
    # هذا السطر ليس موجوداً في الـ TokenObtainPairSerializer الأساسي
    # لذا فقط سنضيف email_field ونستخدمه في validate

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # إزالة حقل 'username' الافتراضي إذا لم نعد نحتاجه
        self.fields.pop('username', None) # لإزالة حقل 'username' إذا كان مضافاً افتراضياً

    def validate(self, attrs):
        # هنا سنقوم بتمرير 'email' كـ 'username' إلى الـ validate الأصلية
        # لأن الـ TokenObtainPairSerializer الأساسي يتوقع 'username'.
        # يجب أن يكون الـ CustomUser model الخاص بك يستخدم 'email' كـ USERNAME_FIELD
        # في settings.py: AUTH_USER_MODEL = 'users.CustomUser'
        # في CustomUser model: USERNAME_FIELD = 'email'
        # EMAIL_FIELD = 'email'

        email = attrs.get('email')
        password = attrs.get('password')

        # استخدام الـ validate الأصلية ولكن مع تمرير الإيميل كـ username
        attrs['username'] = email # هذا السطر هو الحل لجعلها تعمل بالإيميل

        data = super().validate(attrs) # استدعاء الـ validate الأصلية لـ TokenObtainPairSerializer

        # هنا يمكنك إضافة أي بيانات إضافية للتوكن بعد التحقق بنجاح (اختياري)
        # هذا الجزء كان موجود لديك بالفعل
        data['user_type'] = 'CustomUser'
        data['updatePassword'] = 1 if self.user.username == self.user.password else 0 # ملاحظة: self.user.username هنا هو الإيميل
        data['updateName'] = 0 if self.user.full_name else 1 # استخدام full_name بدلاً من first_name

        self.user.last_login = now()
        self.user.save(update_fields=['last_login'])

        return data

    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        # Add custom claims
        token['user_type'] = 'CustomUser'
        token['updatePassword'] = 1 if user.username == user.password else 0
        token['updateName'] = 0 if user.full_name else 1 # استخدام full_name بدلاً من first_name
        return token