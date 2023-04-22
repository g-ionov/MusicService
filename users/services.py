from django.db.models import QuerySet, Count, Prefetch
from rest_framework import status

from .models import User, Subscribers, SocialLink


def get_users() -> QuerySet:
    """ Получить список пользователей вместе с количеством подписчиков и подписок """
    return User.objects.annotate(subscribers_count=Count('owner'), subscriptions_count=Count('subscriber'))


def get_user(user_id: int) -> User:
    """ Получить пользователя по id вместе с количеством подписчиков и подписок. """
    return get_users().get(id=user_id)


def merge_users_and_subscribers()-> QuerySet:
    """ Выполнить JOIN таблиц пользователей и подписчиков """
    return Subscribers.objects.select_related('user').select_related('subscriber')


def get_user_subscribers(user: User) -> QuerySet:
    """ Получить подписчиков пользователя """
    return merge_users_and_subscribers().filter(user=user)

def get_user_subscriptions(user: User) -> QuerySet:
    """ Получить подписки пользователя """
    return merge_users_and_subscribers().filter(subscriber=user)


def count_user_subscribers(user: User) -> int:
    """ Получить количество подписчиков пользователя """
    return get_user_subscribers(user).count()


def count_user_subscriptions(user: User) -> int:
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


def get_social_links(user: User) -> QuerySet:
    """ Получить социальные ссылки пользователя """
    return SocialLink.objects.filter(user=user).select_related('social_media').values('social_media__name', 'url')
