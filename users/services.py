from rest_framework import status

from .models import User, Subscribers, SocialMedia, SocialLink


def get_user_subscribers(user):
    """ Получить подписчиков пользователя """
    return Subscribers.objects.filter(user=user)


def count_user_subscribers(user):
    """ Получить количество подписчиков пользователя """
    return get_user_subscribers(user).count()


def count_user_subscriptions(user):
    """ Получить количество подписок пользователя """
    return Subscribers.objects.filter(subscriber=user).count()


def subscribe_user(user_id: int, subscriber: User) -> int:
    """ Подписаться или отписаться от пользователя
    :param user_id: id пользователя
    :param subscriber: пользователь, который подписывается
    :return: статус ответа
    """
    try:
        user = User.objects.get(id=user_id)
    except User.DoesNotExist:
        return status.HTTP_404_NOT_FOUND
    if user == subscriber:
        return status.HTTP_400_BAD_REQUEST
    if get_user_subscribers(user).filter(subscriber=subscriber).exists():
        get_user_subscribers(user).filter(subscriber=subscriber).delete()
        return status.HTTP_204_NO_CONTENT
    else:
        Subscribers.objects.create(user=user, subscriber=subscriber)
        return status.HTTP_201_CREATED


def get_social_links(user):
    """ Получить социальные ссылки пользователя """
    return SocialLink.objects.filter(user=user).select_related('social_media').values('social_media__name', 'url')

