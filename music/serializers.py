from rest_framework import serializers

from music.models import Track, Genre, Album, Playlist
from users.serializers import OnlyUsernameSerializer


class SimpleGenreSerializer(serializers.ModelSerializer):
    """ Simple genre serializer """

    class Meta:
        model = Genre
        fields = ('id', 'name',)


class GenreSerializer(serializers.ModelSerializer):
    """ Genre serializer """

    class Meta:
        model = Genre
        fields = '__all__'


class TrackSerializer(serializers.ModelSerializer):
    """ Track serializer """
    cover = serializers.ImageField(read_only=True, source='album.cover')
    album = serializers.CharField(read_only=True, source='album.name')
    author = OnlyUsernameSerializer(read_only=True, many=True)


    class Meta:
        model = Track
        fields = ('id', 'cover', 'name', 'album', 'duration', 'author', 'media_file', 'auditions', 'likes')
        read_only_fields = ('auditions', 'likes', 'duration', 'media_file')


class TrackDetailSerializer(serializers.ModelSerializer):
    """ Track detail serializer """
    cover = serializers.ImageField(read_only=True, source='album.cover')
    album = serializers.CharField(read_only=True, source='album.name')
    author = OnlyUsernameSerializer(read_only=True, many=True)
    genre = SimpleGenreSerializer(read_only=True, many=True, source='album.genre')

    class Meta:
        model = Track
        fields = ('id', 'cover', 'name', 'album', 'duration', 'author', 'media_file',
                  'status', 'genre', 'auditions', 'likes', 'text', 'description')
        read_only_fields = ('auditions', 'likes', 'duration', 'media_file', 'status')


class TrackCreateSerializer(serializers.ModelSerializer):
    """ Track create serializer """

    class Meta:
        model = Track
        fields = ('name', 'album', 'media_file', 'text', 'description')


class MyTrackSerializer(serializers.ModelSerializer):
    """ Track serializer """
    cover = serializers.ImageField(read_only=True, source='album.cover')
    album = serializers.CharField(read_only=True, source='album.name')
    author = OnlyUsernameSerializer(read_only=True, many=True)

    class Meta:
        model = Track
        fields = ('id', 'cover', 'name', 'album', 'duration', 'author', 'media_file', 'status', 'auditions', 'likes')


class TrackForAlbumSerializer(serializers.ModelSerializer):
    """ Track serializer """
    author = OnlyUsernameSerializer(read_only=True, many=True)

    class Meta:
        model = Track
        fields = ('id', 'name', 'duration', 'media_file', 'author', 'auditions', 'likes')


class AlbumSerializer(serializers.ModelSerializer):
    """ Album serializer """
    genre = SimpleGenreSerializer(read_only=True, many=True)
    author = OnlyUsernameSerializer(read_only=True, many=True)

    class Meta:
        model = Album
        fields = ('id', 'name', 'author', 'cover', 'date', 'genre', 'description')


class AlbumDetailSerializer(serializers.ModelSerializer):
    """ Album detail serializer """
    genre = SimpleGenreSerializer(read_only=True, many=True)
    tracks = TrackForAlbumSerializer(read_only=True, many=True)
    author = OnlyUsernameSerializer(read_only=True, many=True)

    class Meta:
        model = Album
        fields = ('id', 'name', 'author', 'cover', 'date', 'genre', 'description', 'tracks')


class MyAlbumsSerializer(serializers.ModelSerializer):
    """ Album serializer for user """
    class Meta:
        model = Album
        fields = ('id', 'name', 'cover', 'date', 'status')


class AlbumCreateOrUpdateSerializer(serializers.ModelSerializer):
    """ Album create or update serializer """
    tracks = TrackCreateSerializer(many=True)

    class Meta:
        model = Album
        fields = ('name', 'cover', 'genre', 'description',)


class PlaylistSerializer(serializers.ModelSerializer):
    """ Playlist serializer """
    username = serializers.CharField(read_only=True, source='user.username')

    class Meta:
        model = Playlist
        fields = ('id', 'name', 'cover', 'username')


class PlaylistDetailSerializer(serializers.ModelSerializer):
    """ Playlist detail serializer """
    tracks = TrackForAlbumSerializer(read_only=True, many=True)
    username = serializers.CharField(read_only=True, source='user.username')

    class Meta:
        model = Playlist
        fields = ('id', 'cover', 'name', 'username', 'description', 'likes', 'created_at', 'tracks')


class PlaylistCreateOrUpdateSerializer(serializers.ModelSerializer):
    """ Playlist create or update serializer """
    class Meta:
        model = Playlist
        fields = ('name', 'description', 'cover', 'public')
