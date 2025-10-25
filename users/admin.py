from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as DjangoUserAdmin
from django.utils.translation import gettext_lazy as _

from .models import User


@admin.register(User)
class UserAdmin(DjangoUserAdmin):
    list_display = ("username", "email", "first_name", "last_name", "role", "is_staff")
    list_filter = ("role", "is_staff", "is_superuser", "is_active", "groups")
    fieldsets = DjangoUserAdmin.fieldsets + (
        (_("Información adicional"), {"fields": ("usuario", "role", "remember_me")}),
    )
    add_fieldsets = DjangoUserAdmin.add_fieldsets + (
        (_("Información adicional"), {"fields": ("usuario", "role", "remember_me")}),
    )
    search_fields = ("username", "email", "usuario")
    ordering = ("username",)
