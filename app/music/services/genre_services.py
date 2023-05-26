from django.db.models import QuerySet

from music.models import Genre


def get_genres() -> QuerySet:
    """ Get all genres """
    return Genre.objects.all().only('name')


def get_genre_detail(pk: int) -> Genre:
    """ Get genre detail """
    return Genre.objects.filter(pk=pk)
