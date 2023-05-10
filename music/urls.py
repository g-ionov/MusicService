from django.urls import path, include
from rest_framework import routers

from music import views

router = routers.DefaultRouter()
router.register(r'track', views.TrackViewSet, basename='track')
router.register(r'album', views.AlbumViewSet, basename='album')

urlpatterns = [path('', include(router.urls))]