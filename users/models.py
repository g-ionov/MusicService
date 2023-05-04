from django.core.validators import FileExtensionValidator
from django.db import models
from django.contrib.auth.models import AbstractUser
from phonenumber_field.modelfields import PhoneNumberField

from music.models import Track, LikedTracks, Playlist, Album, ListenedTracks, Genre

from base.services import get_user_main_image_path, get_user_background_image_path, image_size_validator


class User(AbstractUser):
    """ User model """
    phone = PhoneNumberField(verbose_name='Phone number', unique=True, region='RU')
    email = models.EmailField(verbose_name='E-mail', unique=True)
    main_image = models.ImageField(
        upload_to=get_user_main_image_path,
        verbose_name='Main image',
        null=True,
        blank=True,
        validators=[FileExtensionValidator(allowed_extensions=['jpg', 'png']), image_size_validator]
    )
    background_image = models.ImageField(
        upload_to=get_user_background_image_path,
        verbose_name='Background image',
        null=True,
        blank=True,
        validators=[FileExtensionValidator(allowed_extensions=['jpg', 'png']), image_size_validator]
    )
    username = models.CharField(max_length=63, unique=True)
    social_links = models.ManyToManyField('SocialMedia', through='SocialLink', verbose_name='Social links')

    created_tracks = models.ManyToManyField(Track, verbose_name='Created tracks', related_name='created_tracks')
    liked_tracks = models.ManyToManyField(Track, through=LikedTracks,
                                          verbose_name='Liked tracks',
                                          related_name='liked_tracks')
    listened_tracks = models.ManyToManyField(Track, through=ListenedTracks,
                                             verbose_name='Listened tracks',
                                             related_name='listened_tracks')
    created_playlists = models.ManyToManyField(Playlist, verbose_name='Created playlists',
                                               related_name='created_playlists')
    liked_playlists = models.ManyToManyField(Playlist, verbose_name='Liked playlists', related_name='liked_playlists')
    created_albums = models.ManyToManyField(Album, verbose_name='Created albums', related_name='created_albums')
    liked_albums = models.ManyToManyField(Album, verbose_name='Liked albums', related_name='liked_albums')
    liked_genres = models.ManyToManyField(Genre, verbose_name='Liked genres', related_name='liked_genres')

    REQUIRED_FIELDS = ["email", "phone"]

    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'

    def __str__(self):
        return self.username


class Subscribers(models.Model):
    """ Модель подписчиков """
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='owner')
    subscriber = models.ForeignKey(User, on_delete=models.CASCADE, related_name='subscriber')
    date = models.DateTimeField(auto_now_add=True, verbose_name='Subscription date')

    class Meta:
        verbose_name = 'Subscriber'
        verbose_name_plural = 'Subscribers'
        unique_together = ('user', 'subscriber')
        ordering = ('-date',)
        # Check user cannot subscribe to himself
        constraints = [
            models.CheckConstraint(
                check=~models.Q(user=models.F('subscriber')),
                name='check_user_subscriber'
            )
        ]

    def __str__(self):
        return f'{self.subscriber} подписан на {self.user}'


class SocialMedia(models.Model):
    """ Social media model """
    name = models.CharField(max_length=63, unique=True)

    class Meta:
        verbose_name = verbose_name_plural = 'Social media'

    def __str__(self):
        return self.name


class SocialLink(models.Model):
    """ Social link model """
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    social_media = models.ForeignKey(SocialMedia, on_delete=models.CASCADE, verbose_name='Social media')
    url = models.URLField(verbose_name='Link', max_length=255)

    class Meta:
        verbose_name = 'Social link'
        verbose_name_plural = 'Social links'

    def str__(self):
        return f'{self.user} - {self.social_media}'
