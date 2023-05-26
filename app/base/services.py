import time

from django.core.exceptions import ValidationError
from django.utils.safestring import mark_safe

from mutagen import File
from config.settings import IMAGE_SIZE_LIMIT, AUDIO_SIZE_LIMIT


def get_user_main_image_path(instance, image) -> str:
    """ Getting path to users image. Format: media/user_image/user_id/image
    :param instance: user instance
    :param image: image file
    :return: path to image.
    """
    return f'user_image/{instance.id}/{image}'


def get_user_background_image_path(instance, image) -> str:
    """ Getting path to users background image. Format: media/user_background/user_id/image
    :param instance: user instance
    :param image: image file
    :return: path to image.
    """
    return f'user_background/{instance.id}/{image}'


def file_size_validator(file, size_limit):
    """ File size validator
    :param file: file
    :param size_limit: file size limit in MB
    """
    if file.size > size_limit * 1024 ** 2:
        raise ValidationError(f"Максимальный размер файла составляет {size_limit} Мб")


def image_size_validator(image):
    """ Image size validator
    :param image: image file
    """
    file_size_validator(image, IMAGE_SIZE_LIMIT)


def track_size_validator(track):
    """ Track size validator
    :param track: audio file"""
    file_size_validator(track, AUDIO_SIZE_LIMIT)


def get_image_html(img, width=50) -> str:
    """ Getting image in admin panel
    :param img: image file
    :param width: image width
    :return: image tag
    """
    return mark_safe(f"<img src='{img.url}' width={width}>") if img else "Изображение отсутствует"

def get_audio_html(audio) -> str:
    """ Getting audio in admin panel
    :param audio: audio file
    :return: audio tag
    """
    return mark_safe(f"<audio controls src='{audio.url}'></audio>")


def get_audio_duration(audio) -> str:
    """ Getting audio duration
     :param audio: audio file
     :return: audio duration in format MM:SS
    """
    return time.strftime("%M:%S", time.gmtime(File(audio).info.length))


def get_audio_name_from_file(audio) -> str:
    """ Getting audio name from file
    :param audio: audio file
    :return: audio name
    """
    return File(audio).tags.get('title', audio.name)