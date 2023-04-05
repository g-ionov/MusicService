from .models import User, Subscribers, SocialMedia, SocialLink


def get_user_subscribers(user):
    """ Получить подписчиков пользователя """
    return Subscribers.objects.filter(user=user)


def count_user_subscribers(user):
    """ Получить количество подписчиков пользователя """
    return get_user_subscribers(user).count()


def subscribe_user(user_id: int, subscriber: User):
    """ Подписаться или отписаться от пользователя """
    user = User.objects.get(id=user_id)
    if get_user_subscribers(user).filter(subscriber=subscriber).exists():
        get_user_subscribers(user).filter(subscriber=subscriber).delete()
    else:
        Subscribers.objects.create(user=user, subscriber=subscriber)


def get_social_links(user):
    """ Получить социальные ссылки пользователя """
    return SocialLink.objects.filter(user=user).select_related('social_media').values('social_media__name', 'url')

