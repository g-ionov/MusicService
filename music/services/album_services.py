from music.models import Album, Track
from django.db.models import QuerySet, Prefetch

from users.models import User


def get_albums_with_genres() -> QuerySet:
    """ Get all albums with genres """
    return Album.objects.prefetch_related('genre',
                                          Prefetch('created_albums', queryset=User.objects.all().only('username'))
                                          ).filter(status='published')


def get_album_detail(pk: int) -> Album:
    """ Get album with tracks and genres """
    return Album.objects.prefetch_related('genre',
                                          Prefetch('created_albums', queryset=User.objects.all().only('username')),
                                          Prefetch('tracks', queryset=Track.objects.prefetch_related
                                          (Prefetch('created_tracks', queryset=User.objects.all().only('username',))
                                          ))).filter(pk=pk)


def get_my_albums(user: User) -> QuerySet:
    """ Get my tracks """
    return Album.objects.prefetch_related('created_albums').filter(created_albums=user)
