from django.contrib import admin
from django.contrib.auth.admin import UserAdmin 
from .models import CustomUser , StudentInfo

class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = ('username', 'email', 'is_staff', 'is_active')
admin.site.register(CustomUser, CustomUserAdmin)


class StudentInfoAdmin(admin.ModelAdmin):
    model = StudentInfo

admin.site.register(StudentInfo,StudentInfoAdmin)
