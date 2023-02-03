from rest_framework import permissions
from reviews.models import User


class IsSuperuser(permissions.BasePermission):

    def has_permission(self, request, view):
        if request.user.is_authenticated:
            user = User.objects.get(username=request.user)
            return user.is_superuser

    def has_object_permission(self, request, view, obj):
        if request.user.is_authenticated:
            user = User.objects.get(username=request.user)
            return user.is_superuser


class IsAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.user.is_authenticated:
            user = User.objects.get(username=request.user)
            return (user.is_administrator)

    def has_object_permission(self, request, view, obj):
        if request.user.is_authenticated:
            user = User.objects.get(username=request.user)
            return (user.is_administrator)


class IsModerator(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        if request.user.is_authenticated:
            user = User.objects.get(username=request.user)
            return (user.is_moderator)


class IsUser(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        return (
            # request.method in permissions.SAFE_METHODS
            obj.user == request.user
        )


class IsAdminOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        return (
            request.method in permissions.SAFE_METHODS
            or request.user.is_authenticated and (
                request.user.role == 'admin'
                or request.user.role == 'superuser'
            )
        )


class IsAdminModeratorAuthorOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        return (
            request.method in permissions.SAFE_METHODS
            or request.user.is_authenticated
        )

    def has_object_permission(self, request, view, obj):
        return (
            request.method in permissions.SAFE_METHODS
            or request.user.role == 'moderator'
            or request.user.role == 'admin'
            or request.user.role == 'superuser'
            or obj.author == request.user
        )
