from django.db.models import QuerySet, Prefetch, F
from rest_framework import status

from music.models import Playlist
from users.models import User


def check_track_id(track_id: int) -> None:
    """ Checking that the track id is passed to the function """
    if not track_id:
        raise ValueError('Track id is required')


def get_playlists()->QuerySet:
    """ Get all playlists with short info (name, image, author)"""
    return Playlist.objects.select_related('user').only('name', 'cover', 'user__username').filter(public=True)


def get_playlist_detail(pk: int) -> Playlist:
    """ Get playlist detail """
    return Playlist.objects.select_related('user').prefetch_related\
        ('tracks', Prefetch('tracks__author',queryset=User.objects.only('username'))).filter(pk=pk)


def get_my_created_playlists(user: User) -> QuerySet:
    """ Get users created playlists """
    return Playlist.objects.select_related('user').only('name', 'cover', 'user__username').filter(user=user)


def get_my_liked_playlists(user: User) -> QuerySet:
    """ Get users liked playlists """
    return Playlist.objects.select_related('user').prefetch_related('user_liked').filter(user_liked=user)


def get_tracks_in_playlist(playlist_id: int) -> QuerySet:
    """ Get tracks in playlist """
    return Playlist.objects.prefetch_related('tracks').filter(pk=playlist_id)


def add_track_to_playlist(playlist_id: int, track_id: int) -> int:
    """ Add track to playlist """
    check_track_id(track_id)
    if track_id in get_tracks_in_playlist(playlist_id):
        raise ValueError('Track is already in playlist')
    Playlist.objects.get(pk=playlist_id).tracks.add(track_id)
    return status.HTTP_201_CREATED



def remove_track_from_playlist(playlist_id: int, track_id: int):
    """ Remove track from playlist """
    check_track_id(track_id)
    Playlist.objects.get(pk=playlist_id).tracks.remove(track_id)
    return status.HTTP_204_NO_CONTENT


def like_playlist(playlist_id: int, user: User) -> int:
    """ Like playlist
    :arg playlist_id: playlist id
    :arg user: User object
    :return: status code
    """
    if user.liked_playlists.filter(pk=playlist_id).exists():
        user.liked_playlists.remove(playlist_id)
        Playlist.objects.filter(pk=playlist_id).update(likes=F('likes') - 1)
        return status.HTTP_204_NO_CONTENT
    user.liked_playlists.add(playlist_id)
    Playlist.objects.filter(pk=playlist_id).update(likes=F('likes') + 1)
    return status.HTTP_201_CREATED
