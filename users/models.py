from django.core.validators import FileExtensionValidator
from django.db import models
from django.contrib.auth.models import AbstractUser
from phonenumber_field.modelfields import PhoneNumberField

from base.services import get_user_main_image_path, get_user_background_image_path, file_size_validator


class User(AbstractUser):
    """ Модель пользователя """
    phone = PhoneNumberField(verbose_name='Номер телефона', unique=True, region='RU')
    main_image = models.ImageField(
        upload_to=get_user_main_image_path,
        verbose_name='Изображение пользователя',
        null=True,
        blank=True,
        validators=[FileExtensionValidator(allowed_extensions=['jpg', 'png']), file_size_validator]
    )
    background_image = models.ImageField(
        upload_to=get_user_background_image_path,
        verbose_name='Фон профиля',
        null=True,
        blank=True,
        validators=[FileExtensionValidator(allowed_extensions=['jpg', 'png']), file_size_validator]
    )
    username = models.CharField(max_length=63, verbose_name='Имя пользователя', unique=True)

    REQUIRED_FIELDS = ['phone', 'email']

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return self.username


class Subscribers(models.Model):
    """ Модель подписчиков """
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Пользователь', related_name='owner')
    subscriber = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Подписчик', related_name='subscribers')
    date = models.DateTimeField(auto_now_add=True, verbose_name='Дата подписки')

    class Meta:
        verbose_name = 'Подписчик'
        verbose_name_plural = 'Подписчики'
        unique_together = ('user', 'subscriber')  # Проверка на уникальность
        ordering = ('-date',)  # Сортировка по дате
        # Проверка на то, что пользователь не может подписаться на самого себя.
        constraints = [
            models.CheckConstraint(
                check=~models.Q(user=models.F('subscriber')),
                name='check_user_subscriber'
            )
        ]

    def __str__(self):
        return f'{self.subscriber} подписчик {self.user}'


class SocialMedia(models.Model):
    """ Модель социальных сетей"""
    name = models.CharField(max_length=63, unique=True)

    class Meta:
        verbose_name = 'Социальная сеть'
        verbose_name_plural = 'Социальные сети'

    def __str__(self):
        return self.name


class SocialLink(models.Model):
    """ Модель ссылок на социальные сети пользователя"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Пользователь')
    social_media = models.ForeignKey(SocialMedia, on_delete=models.CASCADE, verbose_name='Социальная сеть')
    url = models.URLField(verbose_name='Ссылка', max_length=255)

    class Meta:
        verbose_name = 'Ссылка на социальную сеть'
        verbose_name_plural = 'Ссылки на социальные сети'

    def str__(self):
        return f'{self.user} - {self.social_media}'
