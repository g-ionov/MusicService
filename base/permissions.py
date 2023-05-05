from rest_framework import permissions


class IsThatUserOrStaff(permissions.BasePermission):
    """ Check that the user can only change his data """
    def has_object_permission(self, request, view, obj):
        return obj.pk == request.user.pk or request.user.is_staff
