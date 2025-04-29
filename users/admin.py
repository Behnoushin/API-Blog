from django.contrib import admin
from .models import CustomUser, UserProfile

class CustomUserAdmin(admin.ModelAdmin):
    list_display = ['username', 'email', 'phone_number', 'gender', 'age', 'country', 'city', 'last_login', 'date_joined']
    search_fields = ['username', 'email', 'phone_number']
    list_filter = ['gender', 'country', 'city', 'date_joined']
    ordering = ['username']
    readonly_fields = ['date_joined', 'last_login']
    list_per_page = 20

class UserProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'website', 'created_at', 'updated_at']
    search_fields = ['user__username', 'website']
    ordering = ['-created_at']
    list_filter = ['created_at']
    readonly_fields = ['created_at', 'updated_at']
    list_per_page = 20
    
admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(UserProfile, UserProfileAdmin)