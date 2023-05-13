from rest_framework import status

from music.models import Comment
from django.db.models import QuerySet, Q

from users.models import User


def get_comments() -> QuerySet:
    """ Get all comments """
    return Comment.objects.all()

def get_comments_for_track(track_id: int) -> QuerySet:
    """ Get comments for track """
    return Comment.objects.filter(Q(track_id=track_id) & Q(level=0)).select_related('user')


def reply(user: User, text: str, comment_id: int) -> None:
    """ Reply to comment """
    Comment.objects.create(user=user, track_id=Comment.objects.get(id=comment_id).track_id,
                           text=text, parent_id=comment_id)
    return status.HTTP_201_CREATED
