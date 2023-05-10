from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from music import serializers
from music.services import album_services, track_services, music_services
from base.permissions import IsThatUserOrReadOnly


class TrackViewSet(viewsets.ModelViewSet):
    """ Track viewset """
    filter_backends = [SearchFilter, OrderingFilter, DjangoFilterBackend]
    search_fields = ['name', 'album__name', 'created_tracks__username']
    ordering_fields = ['name', 'album__name', 'created_tracks__username', 'auditions', 'likes']
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
        switcher = {
            'retrieve': track_services.get_track_detail(self.kwargs.get('pk')),
            'my_tracks': track_services.get_my_tracks(self.request.user)}
        return switcher.get(self.action, track_services.get_tracks_with_album_name_and_author_name())

    def get_permissions(self):
        return [IsAuthenticated()] if self.action in ('create', 'my_tracks') else [IsThatUserOrReadOnly()]

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        music_services.mark_as_inspecting(instance)
        return super().update(request, *args, **kwargs)

    @action(methods=['get'], detail=False, url_path='my-tracks', url_name='my-tracks')
    def my_tracks(self, request):
        instance = self.get_queryset()
        serializer = self.get_serializer(instance, many=True)
        return Response(serializer.data)


class AlbumViewSet(viewsets.ModelViewSet):
    """ Album viewset """
    filter_backends = [SearchFilter, OrderingFilter, DjangoFilterBackend]
    search_fields = ['name', 'created_albums__username']
    filterset_fields = ['genre__name']
    ordering_fields = ['name', 'date', 'created_albums__username']

    def get_queryset(self):
        switcher = {
            'retrieve': album_services.get_album_detail(self.kwargs.get('pk')),
            'my_albums': album_services.get_my_albums(self.request.user)}
        return switcher.get(self.action, album_services.get_albums_with_genres())

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return serializers.AlbumDetailSerializer
        elif self.action == ('create', 'update', 'partial_update'):
            return serializers.AlbumCreateOrUpdateSerializer
        elif self.action == 'my_albums':
            return serializers.MyAlbumsSerializer
        return serializers.AlbumSerializer

    def get_permissions(self):
        return [IsAuthenticated()] if self.action in ('create', 'my_albums') else [IsThatUserOrReadOnly()]

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        music_services.mark_as_inspecting(instance)
        return super().update(request, *args, **kwargs)

    @action(methods=['get'], detail=False, url_path='my-albums', url_name='my-albums')
    def my_albums(self, request):
        instance = self.get_queryset()
        serializer = self.get_serializer(instance, many=True)
        return Response(serializer.data)
