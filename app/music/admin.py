from django.contrib import admin
from .models import Track, LikedTracks, Playlist, Album, ListenedTracks, Genre, Comment
from base.services import get_image_html, get_audio_html
from mptt.admin import DraggableMPTTAdmin


@admin.register(Track)
class TrackAdmin(admin.ModelAdmin):
    """ Track admin """
    list_display = ('id', 'name', 'album', 'status', 'auditions', 'likes', 'duration', 'get_audio')
    search_fields = ('name',)
    list_display_links = ('id', 'name')
    readonly_fields = ('get_audio', 'duration', 'auditions', 'likes')
    list_editable = ('status',)

    @staticmethod
    def get_audio(obj):
        return get_audio_html(obj.media_file)


@admin.register(Album)
class AlbumAdmin(admin.ModelAdmin):
    """ Album admin """
    list_display = ('id', 'name', 'date', 'status')
    search_fields = ('name',)
    list_filter = ('status', 'genre')
    readonly_fields = ('get_image',)
    list_display_links = ('id', 'name')

    @staticmethod
    def get_image(obj):
        return get_image_html(obj.cover, 300)

    get_image.short_description = 'Cover'
    get_image.allow_tags = True


@admin.register(Playlist)
class PlaylistAdmin(admin.ModelAdmin):
    """ Playlist admin """
    list_display = ('id', 'name', 'user')
    search_fields = ('name',)
    readonly_fields = ('get_image', 'likes')
    list_display_links = ('id', 'name')

    def get_image(self, obj):
        return get_image_html(obj.cover, 300)

    get_image.short_description = 'Cover'
    get_image.allow_tags = True


@admin.register(Comment)
class CommentAdmin(DraggableMPTTAdmin):
    """ Comment admin """
    list_display = (
    'tree_actions', 'indented_title', 'id', 'parent', 'user', 'track', 'short_text', 'created_at', 'updated_at')
    list_display_links = ('indented_title', 'short_text')
    search_fields = ('text',)
    readonly_fields = ('created_at', 'updated_at')

    def short_text(self, obj):
        return obj.text[:20] + '...' if len(obj.text) > 20 else obj.text


@admin.register(LikedTracks)
class LikedTracksAdmin(admin.ModelAdmin):
    """ Liked tracks admin """
    list_display = ('id', 'user', 'track', 'created_at')
    search_fields = ('user', 'track')
    list_display_links = ('id', 'user')
    readonly_fields = ('created_at',)


@admin.register(ListenedTracks)
class ListenedTracksAdmin(admin.ModelAdmin):
    """ Listened tracks admin """
    list_display = ('id', 'user', 'track', 'date_of_listening')
    search_fields = ('user', 'track')
    list_display_links = ('id', 'user')
    readonly_fields = ('date_of_listening',)


admin.site.register(Genre)
