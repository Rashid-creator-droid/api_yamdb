from rest_framework import permissions, status
from rest_framework.permissions import SAFE_METHODS, BasePermission
from rest_framework.response import Response

from reviews.models import User


class IsSuperuser(permissions.BasePermission):

    def has_permission(self, request, view):
        if request.user.is_authenticated:
            user = User.objects.get(username=request.user)
            return (user.role == 'superuser'
                    or user.role == 'admin'
                    )
        return Response(status=status.HTTP_401_UNAUTHORIZED)

    def has_object_permission(self, request, view, obj):
        if request.user.is_authenticated:
            user = User.objects.get(username=request.user)
            return (user.role == 'superuser'
                    or user.role == 'admin'
                    )
        return Response(status=status.HTTP_401_UNAUTHORIZED)


class IsAdmin(permissions.BasePermission):

    def has_permission(self, request, view):
        if request.user.is_authenticated:
            user = User.objects.get(username=request.user)
            return (user.role == 'admin')
        return Response(status=status.HTTP_401_UNAUTHORIZED)

    def has_object_permission(self, request, view, obj):
        if request.user.is_authenticated:
            user = User.objects.get(username=request.user)
            return (user.role == 'admin')
        return Response(status=status.HTTP_401_UNAUTHORIZED)


class IsModerator(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        if request.user.is_authenticated:
            user = User.objects.get(username=request.user)
            return user.role == 'moderatror'


class IsUser(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        return (
            request.method in permissions.SAFE_METHODS
            or obj.author == request.user
        )


class IsAdminOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        return (request.method in permissions.SAFE_METHODS
                or request.user.is_authenticated and (
                    request.user.role == 'admin'
                    or request.user.role == 'superuser'
                ))


class IsAdminModeratorAuthorOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        return (request.method in permissions.SAFE_METHODS
                or request.user.is_authenticated)

    def has_object_permission(self, request, view, obj):
        return (request.method in permissions.SAFE_METHODS
                or request.user.role == 'moderator'
                or request.user.role == 'admin'
                or request.user.role == 'superuser'
                or obj.author == request.user)
