from django.contrib import admin
from .models import Track, LikedTracks, Playlist, Album, ListenedTracks, Genre
from base.services import get_image_html


@admin.register(Track)
class TrackAdmin(admin.ModelAdmin):
    """ Track admin """
    list_display = ('id', 'name', 'album', 'auditions', 'likes')
    search_fields = ('name',)
    list_display_links = ('id', 'name')



@admin.register(Album)
class AlbumAdmin(admin.ModelAdmin):
    """ Album admin """
    list_display = ('id', 'name', 'date', 'genre', 'status', 'get_image')
    search_fields = ('name',)
    list_filter = ('status', 'genre')
    readonly_fields = ('get_image',)
    list_display_links = ('id', 'name')

    def get_image(self, obj):
        return get_image_html(obj.cover.url)

    get_image.short_description = 'Cover'
    get_image.allow_tags = True


@admin.register(Playlist)
class PlaylistAdmin(admin.ModelAdmin):
    """ Playlist admin """
    list_display = ('id', 'name', 'user', 'get_image')
    search_fields = ('name',)
    readonly_fields = ('get_image',)
    list_display_links = ('id', 'name')

    def get_image(self, obj):
        return get_image_html(obj.cover.url)

    get_image.short_description = 'Cover'
    get_image.allow_tags = True


admin.site.register(LikedTracks)
admin.site.register(ListenedTracks)
admin.site.register(Genre)
