from datetime import datetime

import jwt

from django.conf import settings
from .models import User

from rest_framework import exceptions
from rest_framework.authentication import TokenAuthentication


class JWTAuthentication(TokenAuthentication):
    """ Аутентификация по токену """

    def authenticate_credentials(self, key):
        try:
            payload = jwt.decode(key, settings.SECRET_KEY, algorithms=[settings.TOKEN_ENCODING_ALGORITHM])
        except jwt.ExpiredSignatureError:
            raise exceptions.AuthenticationFailed('Signature expired')
        except jwt.DecodeError:
            raise exceptions.AuthenticationFailed('Decode error')
        except jwt.InvalidTokenError:
            raise exceptions.AuthenticationFailed('Invalid token')

        token_expired = datetime.fromtimestamp(payload['exp'])
        if token_expired < datetime.now():
            raise exceptions.AuthenticationFailed('Token expired')

        try:
            user = User.objects.get(pk=payload['id'])
        except User.DoesNotExist:
            raise exceptions.AuthenticationFailed('No user matching this token was found')

        if not user.is_active:
            raise exceptions.AuthenticationFailed('User is inactive')

        return user, None

    @staticmethod
    def generate_token(user):
        payload = {
            'id': user.pk,
            'exp': datetime.now() + settings.ACCESS_TOKEN_LIFETIME,
        }
        return jwt.encode(payload, settings.SECRET_KEY, algorithm=settings.TOKEN_ENCODING_ALGORITHM)