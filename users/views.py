from rest_framework import viewsets, status
from rest_framework.filters import SearchFilter, OrderingFilter

from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response

from users.authentication import JWTAuthentication
from base.permissions import IsThatUserOrStaff
from users import serializers
from users.services import get_user_subscribers, subscribe_user, get_users, get_user, get_user_subscriptions


class UserViewSet(viewsets.ModelViewSet):
    """ API для пользователей """
    queryset = get_users()
    filter_backends = [SearchFilter, OrderingFilter]
    search_fields = ordering_fields = ['username', 'first_name', 'last_name']

    def get_permissions(self):
        if self.action in ['update', 'partial_update', 'destroy']:
            permission_classes = [IsThatUserOrStaff]
        elif self.action == 'me':
            permission_classes = [IsAuthenticated]
        else:
            permission_classes = [AllowAny]
        return [permission() for permission in permission_classes]

    def get_serializer_class(self):
        switcher = {
            'create': serializers.UserCreateSerializer,
            'get_user_subscribers': serializers.SubscribersSerializer,
            'subscribe': serializers.EmptySerializer,
            'get_user_subscriptions': serializers.UserSubscriptionsSerializer,
            'login': serializers.UserLoginSerializer,
            'retrieve': serializers.UserDetailSerializer,
            'me': serializers.UserDetailSerializer,
        }
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
            serializer = self.get_serializer(get_user(request.user.pk))
            if request.method == 'DELETE':
                request.user.delete()
                return Response(status=status.HTTP_204_NO_CONTENT)
        else:
            serializer = self.get_serializer(request.user, data=request.data, partial=True)
            serializer.is_valid(raise_exception=True)
            serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(detail=True, url_path='subscribers', url_name='subscribers')
    def get_user_subscribers(self, request, pk):
        """ Получить подписчиков пользователя или подписаться на него"""
        serializer = self.get_serializer(get_user_subscribers(pk), many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(detail=True, url_path='subscriptions', url_name='subscriptions')
    def get_user_subscriptions(self, request, pk):
        """ Получить подписки пользователя """
        serializer = self.get_serializer(get_user_subscriptions(pk), many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(methods=['post'], detail=True, url_path='subscribe', url_name='subscribe')
    def subscribe(self, request, pk):
        """ Подписаться на пользователя """
        return Response(status=subscribe_user(pk, request.user))
