# users/serializers.py
from rest_framework import serializers
from .models import CustomUser
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.utils.timezone import now
from django.contrib.auth import get_user_model

User = get_user_model()

class CustomUserSerializer(serializers.ModelSerializer):
    repeat_password = serializers.CharField(write_only=True)

    class Meta:
        model = CustomUser
        fields = [
            'email',
            'username', # مهم جداً لو عايز تعمل validate عليه أو تعرضه
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

class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    email = serializers.EmailField(write_only=True)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields.pop('username', None) # لإزالة حقل 'username' الافتراضي

    def validate(self, attrs):
        email = attrs.get('email')
        password = attrs.get('password')

        attrs['username'] = email # هذا السطر هو الحل لجعلها تعمل بالإيميل

        data = super().validate(attrs)

        data['user_type'] = 'CustomUser'
        data['updatePassword'] = 1 if self.user.username == self.user.password else 0
        data['updateName'] = 0 if self.user.full_name else 1

        self.user.last_login = now()
        self.user.save(update_fields=['last_login'])

        return data

    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token['user_type'] = 'CustomUser'
        token['updatePassword'] = 1 if user.username == user.password else 0
        token['updateName'] = 0 if user.full_name else 1
        return token