from rest_framework.permissions import BasePermission


class IsAdmin(BasePermission):

    def has_permission(self, request, view):
        return request.user and request.user.is_staff


class IsAdminOrCreateOnly(BasePermission):
    def has_permission(self, request, view):
        return (request.user and request.user.is_staff) or (request.user and request.method == "POST")
