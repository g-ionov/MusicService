from rest_framework import status
from rest_framework.response import Response


def mark_as_inspecting(instance) -> None:
    """ Mark as inspecting
    :arg instance: Track or Album instance"""
    instance.status = 'on_inspection'
    instance.save()


def create(function):
    """ This function is used as decorator for create method of viewset """
    def wrapper(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        function(self, request, serializer.instance)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
    return wrapper
