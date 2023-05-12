from rest_framework import status

from music.models import Album, Track
from django.db.models import QuerySet, Prefetch, Q, F

from users.models import User


def get_albums_with_genres() -> QuerySet:
    """ Get all albums with genres """
    return Album.objects.prefetch_related('genre',
                                          Prefetch('author', queryset=User.objects.all().only('username'))
                                          ).filter(status='published')


def get_album_detail(pk: int) -> Album:
    """ Get album with tracks and genres """
    return Album.objects.prefetch_related('genre',
                                          Prefetch('author', queryset=User.objects.all().only('username')),
                                          Prefetch('tracks', queryset=Track.objects.prefetch_related
                                          (Prefetch('author', queryset=User.objects.all().only('username',))
                                          ))).filter(pk=pk)


def get_my_albums(user: User) -> QuerySet:
    """ Get my tracks """
    return Album.objects.prefetch_related('author').filter(author=user)


def get_liked_albums(user: User) -> QuerySet:
    """ Get liked albums """
    return Album.objects.prefetch_related('author', 'genre').filter(user_liked=user)


def like(album_id: int, user: User) -> int:
    """ Like album
    If user liked album, then unlike album
    :arg album_id: Album id
    :arg user: User
    :return: status code
    """
    if not Album.objects.filter(id=album_id).exists():
        return status.HTTP_404_NOT_FOUND

    if not Album.objects.filter(Q(pk=album_id) & Q(user_liked=user)).exists():
        Album.objects.get(pk=album_id).user_liked.add(user)
        return status.HTTP_201_CREATED

    Album.objects.get(pk=album_id).user_liked.remove(user)
    return status.HTTP_204_NO_CONTENT
