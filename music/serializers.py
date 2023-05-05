from rest_framework import serializers

from music.models import Track, Genre
from users.serializers import OnlyUsernameSerializer


class SimpleGenreSerializer(serializers.ModelSerializer):
    """ Simple genre serializer """

    class Meta:
        model = Genre
        fields = ('name',)


class TrackSerializer(serializers.ModelSerializer):
    """ Track serializer """
    cover = serializers.ImageField(read_only=True, source='album.cover')
    album = serializers.CharField(read_only=True, source='album.name')
    author = OnlyUsernameSerializer(read_only=True, many=True, source='created_tracks')


    class Meta:
        model = Track
        fields = ('cover', 'name', 'album', 'duration', 'author', 'media_file', 'auditions', 'likes')
        read_only_fields = ('auditions', 'likes', 'duration', 'media_file')


class TrackDetailSerializer(serializers.ModelSerializer):
    """ Track detail serializer """
    cover = serializers.ImageField(read_only=True, source='album.cover')
    album = serializers.CharField(read_only=True, source='album.name')
    author = OnlyUsernameSerializer(read_only=True, many=True, source='created_tracks')
    genre = SimpleGenreSerializer(read_only=True, many=True, source='album.genre')

    class Meta:
        model = Track
        fields = ('cover', 'name', 'album', 'duration', 'author', 'media_file',
                  'status', 'genre', 'auditions', 'likes', 'text', 'description')
        read_only_fields = ('auditions', 'likes', 'duration', 'media_file', 'status')


class TrackCreateSerializer(serializers.ModelSerializer):
    """ Track create serializer """

    class Meta:
        model = Track
        fields = ('name', 'album', 'media_file', 'text', 'description')
