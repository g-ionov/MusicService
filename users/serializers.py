from rest_framework import serializers

from .models import User, Subscribers
from .services import get_social_links


class UserSerializer(serializers.ModelSerializer):
    """ User serializer """
    subscribers = serializers.IntegerField(source='subscribers_count', read_only=True, default=0)
    subscriptions = serializers.IntegerField(source='subscriptions_count', read_only=True, default=0)

    class Meta:
        model = User
        fields = ('username', 'phone', 'email', 'subscribers', 'subscriptions', 'main_image', 'background_image')


class SimpleUserSerializer(serializers.ModelSerializer):
    """Serializer for user with simple information"""

    class Meta:
        model = User
        fields = ('username', 'main_image')


class SocialLinkSerializer(serializers.Serializer):
    """ Serializer for social links """
    name = serializers.CharField(max_length=63, source='social_media__name')
    url = serializers.URLField(max_length=255)


class SubscribersSerializer(serializers.ModelSerializer):
    """ Serializer for subscribers """
    subscriber = SimpleUserSerializer(read_only=True)

    class Meta:
        model = Subscribers
        fields = ('subscriber', 'date')


class UserSubscriptionsSerializer(serializers.ModelSerializer):
    """ Serializer for user subscriptions """
    user = SimpleUserSerializer(read_only=True)

    class Meta:
        model = Subscribers
        fields = ('user', 'date')


class UserDetailSerializer(serializers.ModelSerializer):
    """ User detail serializer """
    subscribers = serializers.IntegerField(source='subscribers_count', read_only=True, default=0)
    subscriptions = serializers.IntegerField(source='subscriptions_count', read_only=True, default=0)
    socials = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = (
        'username', 'phone', 'email', 'subscribers', 'subscriptions', 'socials', 'main_image', 'background_image')

    def get_socials(self, obj):
        """ Get social links """
        return SocialLinkSerializer(get_social_links(obj), many=True).data


class UserCreateSerializer(serializers.ModelSerializer):
    """ Serializer for user registration """

    class Meta:
        model = User
        fields = ('username', 'phone', 'email', 'password')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user


class UserLoginSerializer(serializers.Serializer):
    """ User login serializer """
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
    """ Empty serializer.
    Used for POST requests with empty body."""
    pass
