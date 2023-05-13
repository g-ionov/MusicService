from django.db.models import QuerySet, Prefetch, F, Q
from rest_framework import status

from music.models import Track, Genre, ListenedTracks, LikedTracks
from users.models import User


def get_tracks_with_album_name_and_author_name() -> QuerySet:
    """ Get tracks with album name and author name """
    return Track.objects.filter(status='published').select_related('album').prefetch_related \
        (Prefetch('author', queryset=User.objects.all().only('username')))


def get_track_detail(pk: int) -> QuerySet:
    """ Get track detail """
    return Track.objects.filter(pk=pk).select_related('album').prefetch_related \
        (Prefetch('author', queryset=User.objects.all().only('username', 'main_image')),
         Prefetch('album__genre', queryset=Genre.objects.all().only('name')))


def get_my_tracks(user: User) -> QuerySet:
    """ Get my tracks """
    return Track.objects.select_related('album').prefetch_related('author').filter(author=user)


def get_liked_tracks(user: User) -> QuerySet:
    """ Get liked tracks """
    return Track.objects.select_related('album').prefetch_related('author').filter(user_liked=user)


def listen_track(track_id: int, user: User) -> int:
    """ Listen track """
    ListenedTracks.objects.create(track_id=track_id, user=user)
    Track.objects.filter(pk=track_id).update(auditions=F('auditions') + 1)
    return status.HTTP_201_CREATED


def get_listened_tracks(user: User) -> QuerySet:
    """ Listened tracks """
    return Track.objects.select_related('album').prefetch_related('author').filter(listener=user)


def like_track(track_id: int, user: User) -> int:
    """ Like track
    If user liked track, then unlike track
    :arg track_id: Track id
    :arg user: User
    :return: status code
    """
    if not Track.objects.filter(id=track_id).exists():
        return status.HTTP_404_NOT_FOUND

    if not Track.objects.filter(Q(pk=track_id) & Q(user_liked=user)).exists():
        LikedTracks.objects.create(track_id=track_id, user=user)
        Track.objects.filter(pk=track_id).update(likes=F('likes') + 1)
        return status.HTTP_201_CREATED

    LikedTracks.objects.filter(Q(track_id=track_id) & Q(user=user)).delete()
    Track.objects.filter(pk=track_id).update(likes=F('likes') - 1)
    return status.HTTP_204_NO_CONTENT


def add_author_to_track(user_id: int, instance: Track) -> None:
    """ Add author during creation track """
    User.objects.get(pk=user_id).created_tracks.add(instance)
