from django.contrib.auth import get_user_model
from rest_framework.permissions import BasePermission

User = get_user_model()


def _has_role(user, role):
    return bool(user and user.is_authenticated and getattr(user, "role", None) == role)


class IsCocina(BasePermission):
    def has_permission(self, request, view):
        return _has_role(request.user, User.Roles.COCINA)


class IsMesero(BasePermission):
    def has_permission(self, request, view):
        return _has_role(request.user, User.Roles.MESERO)


class IsCaja(BasePermission):
    def has_permission(self, request, view):
        return _has_role(request.user, User.Roles.CAJA)


class IsAdminRole(BasePermission):
    def has_permission(self, request, view):
        return _has_role(request.user, User.Roles.ADMIN)
