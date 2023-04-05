from rest_framework import permissions


class IsThatUserOrStaff(permissions.BasePermission):
    """ Проверка, что пользователь может изменять только свой профиль """
    def has_object_permission(self, request, view, obj):
        return obj.pk == request.user.pk or request.user.is_staff
