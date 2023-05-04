from django.core.exceptions import ValidationError
from django.utils.safestring import mark_safe

from config.settings import IMAGE_SIZE_LIMIT, AUDIO_SIZE_LIMIT


def get_user_main_image_path(instance, image):
    """ Getting path to users image. Format: media/user_image/user_id/image"""
    return f'user_image/{instance.id}/{image}'


def get_user_background_image_path(instance, image):
    """ Getting path to users background image. Format: media/user_background/user_id/image"""
    return f'user_background/{instance.id}/{image}'


def file_size_validator(file, size_limit):
    """ File size validator """
    if file.size > size_limit * 1024 ** 2:
        raise ValidationError(f"Максимальный размер файла составляет {size_limit} Мб")


def image_size_validator(image):
    """ Image size validator """
    file_size_validator(image, IMAGE_SIZE_LIMIT)


def track_size_validator(track):
    """ Track size validator """
    file_size_validator(track, AUDIO_SIZE_LIMIT)


def get_image_html(img, width=50):
    """ Getting image in admin panel """
    return mark_safe(f"<img src='{img.url}' width={width}>") if img else "Изображение отсутствует"


def get_user_track_path(instance, filename):
    """ Getting path to users track. Format: media/music/user_id/album_name/track_name"""
    return f'music/{instance.user.id}/{instance.album.name}/{filename}'
