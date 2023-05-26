from rest_framework import permissions


class IsThatUserOrStaff(permissions.BasePermission):
    """ Check that the user can only change his data or staff """
    def has_object_permission(self, request, view, obj):
        return obj.pk == request.user.pk or request.user.is_staff


class IsThatUserOrReadOnly(permissions.BasePermission):
    """ Check that the user can only change his profile data """
    def has_object_permission(self, request, view, obj):
        return obj.pk == request.user.pk or request.method in permissions.SAFE_METHODS


class IsThatUserIsAuthorOrReadOnly(permissions.BasePermission):
    """ Check that the user can only change his playlist. This permission is used for models with author field. """
    def has_object_permission(self, request, view, obj):
        return obj.user == request.user or request.method in permissions.SAFE_METHODS


class IsThatUserIsMusicAuthorOrReadOnly(permissions.BasePermission):
    """ Check that the user can only change his music """
    def has_object_permission(self, request, view, obj):
        return obj.author.filter(pk=request.user.pk).exists() or request.method in permissions.SAFE_METHODS
