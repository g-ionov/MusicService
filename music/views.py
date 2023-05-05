from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from music.serializers import TrackSerializer, TrackDetailSerializer, TrackCreateSerializer
from music.services.track_services import get_tracks_with_album_name_and_author_name, get_track_detail, mark_as_inspecting
from base.permissions import IsThatUserOrReadOnly


class TrackViewSet(viewsets.ModelViewSet):
    """ Track viewset """
    filter_backends = [SearchFilter, OrderingFilter]
    search_fields = ['name', 'album__name', 'created_tracks__username']
    ordering_fields = ['name', 'album__name', 'created_tracks__username', 'auditions', 'likes']

    def get_serializer_class(self):
        if self.action in ('retrieve', 'update', 'partial_update'):
            return TrackDetailSerializer
        elif self.action == 'create':
            return TrackCreateSerializer
        return TrackSerializer

    def get_queryset(self):
        if self.action == 'retrieve':
            return get_track_detail(self.kwargs.get('pk'))
        return get_tracks_with_album_name_and_author_name()

    def get_permissions(self):
        return [IsAuthenticated()] if self.action in ('create', 'my_tracks') else [IsThatUserOrReadOnly()]

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        mark_as_inspecting(instance)
        return super().update(request, *args, **kwargs)

    @action(methods=['get'], detail=False, url_path='my-tracks', url_name='my-tracks')
    def my_tracks(self, request):
        instance = self.get_queryset().filter(created_tracks=request.user)
        serializer = self.get_serializer(instance, many=True)
        return Response(serializer.data)
