from django.core.validators import FileExtensionValidator
from django.db import models
from mptt.fields import TreeForeignKey
from mptt.models import MPTTModel

from base.services import image_size_validator, track_size_validator, get_audio_duration, get_audio_name_from_file


class Album(models.Model):
    """ Album model """

    STATUS_CHOICES = [('draft', 'Draft'), ('published', 'Published'), ('on_inspection', 'On inspection')]

    name = models.CharField(max_length=255, verbose_name='Title')
    date = models.DateField(verbose_name='Date', auto_now_add=True)
    cover = models.ImageField(
        upload_to='covers/',
        verbose_name='Cover',
        validators=[image_size_validator, FileExtensionValidator(allowed_extensions=['jpg', 'png'])])
    description = models.TextField(verbose_name='Description')
    status = models.CharField(max_length=13, choices=STATUS_CHOICES, default='draft')
    genre = models.ManyToManyField('Genre', verbose_name='Genre', related_name='albums')

    class Meta:
        verbose_name = 'Album'
        verbose_name_plural = 'Albums'

    def __str__(self):
        return self.name


class Track(models.Model):
    """ Track model """
    STATUS_CHOICES = [('on_inspection', 'On inspection'), ('published', 'Published'), ('rejected', 'Rejected')]

    name = models.CharField(max_length=255, verbose_name='Title', blank=True)
    text = models.TextField(verbose_name='Lyrics')
    description = models.TextField(verbose_name='Description')
    album = models.ForeignKey(Album, on_delete=models.CASCADE, verbose_name='Album', related_name='tracks')
    media_file = models.FileField(upload_to='tracks/', verbose_name='Track',
                                  validators=[FileExtensionValidator(allowed_extensions=['mp3', 'wav', 'flac']),
                                              track_size_validator])
    auditions = models.PositiveIntegerField(verbose_name='Auditions', default=0)
    likes = models.PositiveIntegerField(verbose_name='Likes', default=0)
    duration = models.CharField(max_length=6, verbose_name='Duration', blank=True)
    status = models.CharField(max_length=15, choices=STATUS_CHOICES, default='on_inspection')


    class Meta:
        verbose_name = 'Track'
        verbose_name_plural = 'Tracks'


    def save(self, *args, **kwargs):
        if not self.duration:
            self.duration = get_audio_duration(self.media_file)
        if not self.name:
            self.name = get_audio_name_from_file(self.media_file)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class Genre(models.Model):
    """ Genre model """
    name = models.CharField(max_length=255, verbose_name='Title')
    description = models.TextField(verbose_name='Description')

    class Meta:
        verbose_name = 'Genre'
        verbose_name_plural = 'Genres'

    def __str__(self):
        return self.name


class Playlist(models.Model):
    """ Playlist model """
    name = models.CharField(max_length=255, verbose_name='Title')
    description = models.TextField(verbose_name='Description')
    user = models.ForeignKey('users.User', on_delete=models.CASCADE, verbose_name='User', related_name='playlists')
    likes = models.PositiveIntegerField(verbose_name='Likes', default=0)
    public = models.BooleanField(verbose_name='Public', default=False)
    created_at = models.DateTimeField(verbose_name='Created at', auto_now_add=True)
    tracks = models.ManyToManyField(Track, verbose_name='Tracks', related_name='playlists')
    cover = models.ImageField(upload_to='covers/', verbose_name='Cover', null=True, blank=True,
                              validators=[image_size_validator,
                                          FileExtensionValidator(allowed_extensions=['jpg', 'png'])],)

    class Meta:
        verbose_name = 'Playlist'
        verbose_name_plural = 'Playlists'

    def __str__(self):
        return self.name


class Comment(MPTTModel):
    """ Comment model """
    parent = TreeForeignKey('self', on_delete=models.CASCADE, verbose_name='Parent', related_name='children',
                               null=True, blank=True)
    user = models.ForeignKey('users.User', on_delete=models.CASCADE, verbose_name='User', related_name='comments')
    text = models.TextField(verbose_name='Text')
    created_at = models.DateTimeField(verbose_name='Created at', auto_now_add=True)
    updated_at = models.DateTimeField(verbose_name='Updated at', auto_now=True)
    track = models.ForeignKey(Track, on_delete=models.CASCADE, verbose_name='Track', related_name='comments')


    class Meta:
        verbose_name = 'Comment'
        verbose_name_plural = 'Comments'


    class MPTTMeta:
        order_insertion_by = ['created_at']

    def __str__(self):
        return self.text[:20]


class LikedTracks(models.Model):
    """ Liked tracks model """
    user = models.ForeignKey('users.User', on_delete=models.CASCADE, verbose_name='User')
    track = models.ForeignKey(Track, on_delete=models.CASCADE, verbose_name='Track')
    created_at = models.DateTimeField(verbose_name='Created at', auto_now_add=True)

    class Meta:
        verbose_name = 'Liked track'
        verbose_name_plural = 'Liked tracks'

    def __str__(self):
        return f'{self.user.username} - {self.track.name}'


class ListenedTracks(models.Model):
    """ Listened tracks model """
    user = models.ForeignKey('users.User', on_delete=models.CASCADE, verbose_name='User')
    track = models.ForeignKey(Track, on_delete=models.CASCADE, verbose_name='Track')
    date_of_listening = models.DateTimeField(verbose_name='Created at', auto_now_add=True)

    class Meta:
        verbose_name = 'Listened track'
        verbose_name_plural = 'Listened tracks'

    def __str__(self):
        return f'{self.user.username} - {self.track.name} - {self.date_of_listening}'