from rest_framework import permissions
from rest_framework.permissions import BasePermission

class IsAdminOrReadOnly(BasePermission):
    """
    Only admins are allowed to change data.
    Other users can only view the data.
    """
    def has_permission(self, request, view):
        if request.method in ['GET', 'HEAD', 'OPTIONS']:
            return True
        return request.user and request.user.is_staff


class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    Only the owner of the object can edit or delete it, others can only read it.
    """
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.author == request.user
