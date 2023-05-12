from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly, AllowAny
from rest_framework.response import Response

from music import serializers
from music.services import album_services, track_services, music_services, genre_services, playlist_services
from base.permissions import IsThatUserIsMusicAuthorOrReadOnly, IsThatUserIsPlaylistAuthorOrReadOnly


class TrackViewSet(viewsets.ModelViewSet):
    """ Track viewset """
    filter_backends = [SearchFilter, OrderingFilter, DjangoFilterBackend]
    search_fields = ['name', 'album__name', 'author__username']
    ordering_fields = ['name', 'album__name', 'author__username', 'auditions', 'likes']
    filterset_fields = ['album__genre__name']

    def get_serializer_class(self):
        if self.action in ('retrieve', 'update', 'partial_update'):
            return serializers.TrackDetailSerializer
        elif self.action == 'create':
            return serializers.TrackCreateSerializer
        elif self.action == 'my_tracks':
            return serializers.MyTrackSerializer
        return serializers.TrackSerializer

    def get_queryset(self):
        if self.action == 'retrieve':
            return track_services.get_track_detail(self.kwargs.get('pk'))
        elif self.action == 'my_tracks':
            return track_services.get_my_tracks(self.request.user)
        elif self.action == 'liked_tracks':
            return track_services.get_liked_tracks(self.request.user)
        elif self.action == 'listened_tracks':
            return track_services.get_listened_tracks(self.request.user)
        return track_services.get_tracks_with_album_name_and_author_name()

    def get_permissions(self):
        if self.action in ('create', 'my_tracks', 'liked_tracks', 'listened_tracks', 'like'):
            return [IsAuthenticated()]
        elif self.action == 'listen':
            return [AllowAny()]
        return [IsThatUserIsMusicAuthorOrReadOnly()]

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        music_services.mark_as_inspecting(instance)
        return super().update(request, *args, **kwargs)

    @action(methods=['get'], detail=False, url_path='my-tracks', url_name='my-tracks')
    def my_tracks(self, request):
        return Response(self.get_serializer(self.get_queryset(), many=True).data)

    @action(methods=['post'], detail=True, url_path='like', url_name='like')
    def like(self, request, pk):
        return Response(status=track_services.like_track(pk, request.user))

    @action(methods=['get'], detail=False, url_path='liked', url_name='liked')
    def liked_tracks(self, request):
        return Response(self.get_serializer(self.get_queryset(), many=True).data)

    @action(methods=['post'], detail=True, url_path='listen', url_name='listen')
    def listen(self, request, pk):
        return Response(status=track_services.listen_track(pk, request.user))

    @action(methods=['get'], detail=False, url_path='listened', url_name='listened')
    def listened_tracks(self, request):
        return Response(self.get_serializer(self.get_queryset(), many=True).data)


class AlbumViewSet(viewsets.ModelViewSet):
    """ Album viewset """
    filter_backends = [SearchFilter, OrderingFilter, DjangoFilterBackend]
    search_fields = ['name', 'author__username']
    filterset_fields = ['genre__name']
    ordering_fields = ['name', 'date', 'author__username']

    def get_queryset(self):
        if self.action == 'retrieve':
            return album_services.get_album_detail(self.kwargs.get('pk'))
        elif self.action == 'my_albums':
            return album_services.get_my_albums(self.request.user)
        elif self.action == 'liked_albums':
            return album_services.get_liked_albums(self.request.user)
        return album_services.get_albums_with_genres()

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return serializers.AlbumDetailSerializer
        elif self.action == ('create', 'update', 'partial_update'):
            return serializers.AlbumCreateOrUpdateSerializer
        elif self.action == 'my_albums':
            return serializers.MyAlbumsSerializer
        return serializers.AlbumSerializer

    def get_permissions(self):
        return [IsAuthenticated()] if self.action in ('create', 'my_albums') else [IsThatUserIsMusicAuthorOrReadOnly()]

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        music_services.mark_as_inspecting(instance)
        return super().update(request, *args, **kwargs)

    @action(methods=['get'], detail=False, url_path='my-albums', url_name='my-albums')
    def my_albums(self, request):
        return Response(self.get_serializer(self.get_queryset(), many=True).data)

    @action(methods=['get'], detail=False, url_path='liked', url_name='liked')
    def liked_albums(self, request):
        return Response(self.get_serializer(self.get_queryset(), many=True).data)

    @action(methods=['post'], detail=True, url_path='like', url_name='like')
    def like(self, request, pk):
        return Response(status=album_services.like(pk, request.user))


class GenreViewSet(viewsets.ModelViewSet):
    """ Genre viewset """
    permission_classes = [IsAuthenticatedOrReadOnly]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['name']

    def get_queryset(self):
        if self.action == 'retrieve':
            return genre_services.get_genre_detail(self.kwargs.get('pk'))
        return genre_services.get_genres()

    def get_serializer_class(self):
        if self.action == 'list':
            return serializers.SimpleGenreSerializer
        return serializers.GenreSerializer


class PlaylistViewSet(viewsets.ModelViewSet):
    """ Playlist viewset """
    filter_backends = [SearchFilter, OrderingFilter, DjangoFilterBackend]
    search_fields = ['name', 'user']
    filterset_fields = ['created_at']
    ordering_fields = ['name', 'created_at']

    def get_queryset(self):
        if self.action == 'retrieve':
            return playlist_services.get_playlist_detail(self.kwargs.get('pk'))
        elif self.action == 'my_playlists':
            return playlist_services.get_my_created_playlists(self.request.user)
        elif self.action == 'liked_playlists':
            return playlist_services.get_my_liked_playlists(self.request.user)
        return playlist_services.get_playlists()

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return serializers.PlaylistDetailSerializer
        elif self.action in ('create', 'update', 'partial_update'):
            return serializers.PlaylistCreateOrUpdateSerializer
        return serializers.PlaylistSerializer

    def get_permissions(self):
        return [IsAuthenticated()] if self.action in ('create', 'my_playlists', 'like', 'liked_playlists', 'add_track',
                                                      'remove_track') else [IsThatUserIsPlaylistAuthorOrReadOnly()]

    @action(methods=['get'], detail=False, url_path='my-playlists', url_name='my-playlists')
    def my_playlists(self, request):
        return Response(self.get_serializer(self.get_queryset(), many=True).data)

    @action(methods=['get'], detail=False, url_path='liked-playlists', url_name='liked-playlists')
    def liked_playlists(self, request):
        return Response(self.get_serializer(self.get_queryset(), many=True).data)

    @action(methods=['post'], detail=True, url_path='like', url_name='like')
    def like(self, request, pk):
        return Response(status=playlist_services.like_playlist(pk, request.user))

    @action(methods=['post'], detail=True, url_path='add-track', url_name='add-track')
    def add_track(self, request, pk):
        """ Add track to playlist
        required params: track_id. Track id must be in request.data
        """
        return Response(status=playlist_services.add_track_to_playlist(pk, request.data.get('track_id')))

    @action(methods=['post'], detail=True, url_path='remove-track', url_name='remove-track')
    def remove_track(self, request, pk):
        """ Add track to playlist
        required params: track_id. Track id must be in request.data
        """
        return Response(status=playlist_services.remove_track_from_playlist(pk, request.data.get('track_id')))
