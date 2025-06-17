from django.contrib import admin
from django.contrib.auth.admin import UserAdmin 
from .models import CustomUser
class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = ('email', 'full_name', 'department', 'academic_year', 'is_active')
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal info', {'fields': ('username', 'full_name', 'department', 'academic_year')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2', 'full_name', 'department', 'academic_year'),
        }),
    )
    ordering = ('email',)

admin.site.register(CustomUser, CustomUserAdmin)
