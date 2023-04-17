from rest_framework import serializers

from .models import User, Subscribers


class UserSerializer(serializers.ModelSerializer):
    """ Сериализатор пользователя"""
    subscribers = serializers.IntegerField(source='subscribers_count', read_only=True, default=0)
    subscriptions = serializers.IntegerField(source='subscriptions_count', read_only=True, default=0)

    class Meta:
        model = User
        fields = ('username', 'phone', 'email', 'subscribers', 'subscriptions', 'main_image', 'background_image')


class SimpleUserSerializer(serializers.ModelSerializer):
    """ Сериализатор пользователя с минимальной информацией"""

    class Meta:
        model = User
        fields = ('username', 'main_image')


class SocialLinkSerializer(serializers.Serializer):
    """ Сериализатор ссылки на социальную сеть """
    name = serializers.CharField(max_length=63, source='social_media.name')
    url = serializers.CharField(max_length=255)


class SubscribersSerializer(serializers.ModelSerializer):
    """ Сериализатор подписчиков пользователя """
    subscriber = SimpleUserSerializer(read_only=True)

    class Meta:
        model = Subscribers
        fields = ('subscriber', 'date')


class UserSubscriptionsSerializer(serializers.ModelSerializer):
    """ Сериализатор подписок пользователя """
    user = SimpleUserSerializer(read_only=True)

    class Meta:
        model = Subscribers
        fields = ('user', 'date')


class UserDetailSerializer(serializers.ModelSerializer):
    """ Сериализатор пользователя с подробной информацией """
    subscribers = serializers.IntegerField(source='subscribers_count', read_only=True, default=0)
    subscriptions = serializers.IntegerField(source='subscriptions_count', read_only=True, default=0)
    social_links = SocialLinkSerializer(many=True, read_only=True, source='sociallink_set')

    class Meta:
        model = User
        fields = (
        'username', 'phone', 'email', 'subscribers', 'subscriptions', 'social_links', 'main_image', 'background_image')


class UserCreateSerializer(serializers.ModelSerializer):
    """ Сериализатор создания пользователя """

    class Meta:
        model = User
        fields = ('username', 'phone', 'email', 'password')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user


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
