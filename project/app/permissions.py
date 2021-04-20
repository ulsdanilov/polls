from rest_framework.permissions import SAFE_METHODS, BasePermission


class IsAdminOrReadOnly(BasePermission):
    """
    The request is authenticated as Admin, or is a read-only request.
    """
    def has_permission(self, request, view):
        if (request.method in SAFE_METHODS) or \
            (request.user and request.user.is_authenticated and request.user.is_staff):
            return True
        return False
