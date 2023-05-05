from django.db.models import QuerySet, Prefetch

from music.models import Track, Genre
from users.models import User


def get_tracks_with_album_name_and_author_name() -> QuerySet:
    """ Get tracks with album name and author name """
    return Track.objects.filter(status='published').select_related('album').prefetch_related\
        (Prefetch('created_tracks', queryset=User.objects.all().only('username')))


def get_track_detail(pk: int) -> QuerySet:
    """ Get track detail """
    return Track.objects.filter(pk=pk).select_related('album').prefetch_related\
        (Prefetch('created_tracks', queryset=User.objects.all().only('username', 'main_image')),
         Prefetch('album__genre', queryset=Genre.objects.all().only('name')))


def mark_as_inspecting(track: Track) -> None:
    """ Mark as inspecting """
    track.status = 'on_inspection'
    track.save()


def get_my_tracks(user: User) -> QuerySet:
    """ Get my tracks """
    return get_tracks_with_album_name_and_author_name().filter(created_tracks=user)