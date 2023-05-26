from celery import shared_task
from celery_singleton import Singleton
from django.db import transaction
from django.db.models import F

from music.models import Track, Playlist


@shared_task(base=Singleton)
def add_like(model_name: str, instance_id: int):
    """ Add like to instance
    :arg model_name: Model name must be 'Track' or 'Playlist'
    :arg instance_id: Instance id"""
    if model_name not in ('Track', 'Playlist'):
        raise ValueError('Model name is not valid')

    model = Track if model_name == 'Track' else Playlist
    with transaction.atomic():
        model.objects.filter(pk=instance_id).update(likes=F('likes') + 1)


@shared_task(base=Singleton)
def remove_like(model_name:str, instance_id:int):
    """ Remove like from instance
    :arg model_name: Model name must be 'Track' or 'Playlist'
    :arg instance_id: Instance id"""
    if model_name not in ('Track', 'Playlist'):
        raise ValueError('Model name is not valid')

    model = Track if model_name == 'Track' else Playlist
    with transaction.atomic():
        model.objects.filter(pk=instance_id).update(likes=F('likes') - 1)

@shared_task(base=Singleton)
def add_audition(track_id: int):
    """ Add audition to track """
    with transaction.atomic():
        Track.objects.filter(pk=track_id).update(auditions=F('auditions') + 1)
