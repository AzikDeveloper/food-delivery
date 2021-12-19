from rest_framework.permissions import BasePermission
from rest_framework.generics import get_object_or_404


class IsAdminOrCreateOnly(BasePermission):
    def has_permission(self, request, view):
        return request.user and request.user.is_staff or request.method == 'POST'


class IsAdminOrGetOnly(BasePermission):
    def has_permission(self, request, view):
        return (request.user and request.user.is_staff) or request.method == 'GET'
