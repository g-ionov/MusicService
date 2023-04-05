from django.core.exceptions import ValidationError
from django.utils.safestring import mark_safe

from config.settings import IMAGE_SIZE_LIMIT


def get_user_main_image_path(instance, image):
    """ Получение пути к изображению пользователя. Формат: media/user_image/user_id/image"""
    return f'user_image/{instance.id}/{image}'


def get_user_background_image_path(instance, image):
    """ Получение пути к изображению пользователя. Формат: media/user_background/user_id/image"""
    return f'user_background/{instance.id}/{image}'


def file_size_validator(file):
    """ Проверка размера файла """
    size_limit = IMAGE_SIZE_LIMIT
    if file.size > size_limit * 1024 ** 2:
        raise ValidationError(f"Максимальный размер файла составляет {size_limit} Мб")


def get_image_html(img, width=50):
    """ Вывод изображения в админке """
    return mark_safe(f"<img src='{img.url}' width={width}>") if img else "Изображение отсутствует"
