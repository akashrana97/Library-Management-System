from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from App_User.models import User


# Register your models here.

@admin.register(User)
class CustomUserAdmin(BaseUserAdmin):
    list_display = ('username', 'email', 'role', 'is_staff')
    fieldsets = BaseUserAdmin.fieldsets + (
        (('Custom Fields'), {'fields': ('role',)}),
    )
