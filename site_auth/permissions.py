from rest_framework.permissions import BasePermission, IsAdminUser


class IsAdminOrCreateOnly(BasePermission):
    def has_permission(self, request, view):
        return (request.user and request.user.is_staff) or (request.user and request.method == "POST")


class IsAdminOrGetOnly(BasePermission):
    def has_permission(self, request, view):
        return (request.user and request.user.is_staff) or request.method == 'GET'
