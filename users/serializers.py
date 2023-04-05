from rest_framework import serializers

from .models import User, Subscribers
from .services import count_user_subscribers, get_user_subscribers, get_social_links as social_links


class UserSerializer(serializers.ModelSerializer):
    """ Сериализатор пользователя"""
    subscribers = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ('username', 'phone', 'email', 'subscribers', 'main_image', 'background_image')
        read_only_fields = ('id', 'date_joined', 'last_login')

    def get_subscribers(self, obj):
        return count_user_subscribers(obj)


class SocialLinkSerializer(serializers.Serializer):
    """ Сериализатор ссылки на социальную сеть """
    name = serializers.CharField(max_length=63, source='social_media__name')
    url = serializers.CharField(max_length=255)


class UserDetailSerializer(serializers.ModelSerializer):
    """ Сериализатор пользователя с подробной информацией """
    subscribers = serializers.SerializerMethodField()
    subscribers_list = serializers.SerializerMethodField()
    social_links = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ('username', 'phone', 'email', 'subscribers', 'subscribers_list', 'social_links',
                  'main_image', 'background_image')
        read_only_fields = ('id', 'date_joined', 'last_login')

    def get_subscribers(self, obj):
        return count_user_subscribers(obj)

    def get_subscribers_list(self, obj):
        return UserSubscribersSerializer(get_user_subscribers(obj), many=True).data

    def get_social_links(self, obj):
        return SocialLinkSerializer(social_links(obj), many=True).data


class UserCreateSerializer(serializers.ModelSerializer):
    """ Сериализатор создания пользователя """
    class Meta:
        model = User
        fields = ('username', 'phone', 'email', 'password')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user


class UserSubscribersSerializer(serializers.ModelSerializer):
    """ Сериализатор подписчиков пользователя """
    subscriber = UserSerializer()

    class Meta:
        model = Subscribers
        fields = ('subscriber', 'date')


class UserSubscribersCreateSerializer(serializers.ModelSerializer):
    """ Сериализатор создания подписчика пользователя """
    class Meta:
        model = Subscribers
        fields = ('user',)


class UserLoginSerializer(serializers.Serializer):
    """ Сериализатор аутентификации пользователя """
    username = serializers.CharField(max_length=150)
    password = serializers.CharField(max_length=128, write_only=True)

    def validate(self, attrs):
        username = attrs.get('username')
        password = attrs.get('password')

        if username and password:
            user = User.objects.filter(username=username).first()
            if user and user.check_password(password):
                attrs['user'] = user
                return attrs
            else:
                raise serializers.ValidationError('Неверные имя пользователя или пароль')
        else:
            raise serializers.ValidationError('Необходимо ввести имя пользователя и пароль')



class EmptySerializer(serializers.Serializer):
    """ Пустой сериализатор.
     Используется для валидации запроса без тела."""
    pass
