from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import gettext_lazy as _
from account.models import (
    User,
    Role,
    Permission,
)


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    fieldsets = (
        (None, {"fields": ("username", "password")}),
        (_("Personal info"), {"fields": ("first_name", "last_name", "email", "phone_number", "role", "assigned_menus")}),
        (_("Permissions"), {"fields": ("is_active", "is_staff", "is_superuser", "groups", "user_permissions")}),
        (_("Important dates"), {"fields": ("last_login", "date_joined")}),
    )
    add_fieldsets = (
        (None, {
            "classes": ("wide",),
            "fields": ("username", "password1", "password2", "phone_number", "assigned_menus"),
        }),
    )
    list_display = ("id", "username", "email", "phone_number", "role", "is_staff", "is_active")
    search_fields = ("username", "email", "phone_number", "role__name")
    ordering = ("username",)

    filter_horizontal = ('assigned_menus', 'groups', 'user_permissions')


@admin.register(Role)
class RoleAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    search_fields = ('name',)
    filter_horizontal = ('permissions',)


@admin.register(Permission)
class PermissionAdmin(admin.ModelAdmin):
    list_display = ('id', 'permission_type', 'description')
    search_fields = ('permission_type',)

