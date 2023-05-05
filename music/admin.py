from django.contrib import admin
from .models import Track, LikedTracks, Playlist, Album, ListenedTracks, Genre
from base.services import get_image_html, get_audio_html


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
    readonly_fields = ('get_image',)
    list_display_links = ('id', 'name')

    def get_image(self, obj):
        return get_image_html(obj.cover, 300)

    get_image.short_description = 'Cover'
    get_image.allow_tags = True


admin.site.register(LikedTracks)
admin.site.register(ListenedTracks)
admin.site.register(Genre)
