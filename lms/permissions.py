from rest_framework import permissions


class IsLibrarian(permissions.BasePermission):

    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == "LIBRARIAN"


class IsOwnerOrReadOnly(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.user == request.user


class IsStudent(permissions.BasePermission):

    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == "STUDENT"
