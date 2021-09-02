from django.contrib import admin
from .models import User
from django.contrib.auth.admin import UserAdmin
# Register your models here.

class UserAdminConfig(UserAdmin):
    search_fields = ('email', 'first_name', 'username')
    list_display = ('username', 'first_name', 'email', 'is_active', 'is_staff')
    fieldsets = (
        (None, {'fields':('first_name', 'last_name', 'username', 'email', 'mobile')}),
        ('permissions', {'fields':('is_staff','is_active', 'is_verified','groups')}),
        ('Activity', {'fields':('date_joined', 'last_login')})
    )

admin.site.register(User, UserAdminConfig)  
