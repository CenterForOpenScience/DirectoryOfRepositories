from rest_framework import permissions
from django.core.exceptions import PermissionDenied

class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    Custom permission to only allow owners of an object to edit it.
    """
    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to any request,
        # so we'll always allow GET, HEAD or OPTIONS requests.
        if request.method in permissions.SAFE_METHODS:
            return True

        # Write permissions are only allowed to the owner of the object.
        return obj.owner == request.user


class CanCreateOrReadOnly(permissions.BasePermission):
    """
    Custom permission to allow authorized journal/repo creators to create only one.
    """
    def has_object_permission(self, request, view, obj):
        if not request.method == 'POST':
            return True
        if not ((len(request.user.journals.all()) + len(request.user.repositorys.all()) <= 1) or request.user.username == 'admin'):
            obj.delete()
            raise PermissionDenied("Can create only 1 object instance per user")
        if not ((len(request.user.standards.all()) <= 1) or request.user.username == 'admin'):
            obj.delete()
            raise PermissionDenied("Can create only 1 standards instance per user")
        else:
            return True
