from rest_framework import permissions, status
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

    def has_object_permission(self, request, view, obj):
        if request.user.is_authenticated:
            user = User.objects.get(username=request.user)
            return (user.role == 'admin')


class IsModerator(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        if request.user.is_authenticated:
            user = User.objects.get(username=request.user)
            return (user.role == 'moderatror')


class IsUser(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        return (
            request.method in permissions.SAFE_METHODS
            or obj.author == request.user
        )
