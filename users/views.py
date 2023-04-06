from rest_framework import viewsets, status
from .authentication import JWTAuthentication
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response

from users.models import User
from users.permissions import IsThatUserOrStaff
from users import serializers
from users.services import get_user_subscribers, subscribe_user


class UserViewSet(viewsets.ModelViewSet):
    """ API для пользователей """
    serializer_class = serializers.UserSerializer
    queryset = User.objects.all()

    def get_permissions(self):
        if self.action in ['update', 'partial_update', 'destroy']:
            permission_classes = [IsThatUserOrStaff]
        elif self.action in ['me', 'logout']:
            permission_classes = [IsAuthenticated]
        else:
            permission_classes = [AllowAny]
        return [permission() for permission in permission_classes]

    def get_serializer_class(self):
        switcher = {
            'create': serializers.UserCreateSerializer,
            'get_user_subscribers': serializers.UserSubscribersSerializer,
            'login': serializers.UserLoginSerializer,
            'retrieve': serializers.UserDetailSerializer,
            'me': serializers.UserDetailSerializer,
        }

        if self.action == 'get_user_subscribers' and self.request.method == 'POST':
            return serializers.EmptySerializer
        return switcher.get(self.action, serializers.UserSerializer)


    @action(methods=['post'], detail=False, url_path='login', url_name='login')
    def login(self, request):
        """ Авторизация пользователя """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response({'token': JWTAuthentication.generate_token(serializer.validated_data['user'])},
                        status=status.HTTP_200_OK)

    @action(methods=['get', 'patch', 'put', 'delete'], detail=False, url_path='me', url_name='me')
    def me(self, request):
        """ Получить данные пользователя или обновить их"""
        if request.method in ['GET', 'DELETE']:
            serializer = self.get_serializer(request.user)
            if request.method == 'DELETE':
                request.user.delete()
                return Response(status=status.HTTP_204_NO_CONTENT)
        else:
            serializer = self.get_serializer(request.user, data=request.data, partial=True)
            serializer.is_valid(raise_exception=True)
            serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(methods=['get', 'post'], detail=True, url_path='subscribers', url_name='subscribers')
    def get_user_subscribers(self, request, pk):
        """ Получить подписчиков пользователя или подписаться на него"""
        if request.method == 'GET':
            serializer = self.get_serializer(get_user_subscribers(pk), many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        elif request.method == 'POST':
            subscribe_user(pk, request.user)
            return Response(status=status.HTTP_201_CREATED)
