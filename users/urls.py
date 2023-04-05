from django.urls import path, include
import users.views as views
import users.auth_views as auth_views
from rest_framework import routers


router = routers.DefaultRouter()
router.register(r'', views.UserViewSet, basename='users')


urlpatterns = [
    path('yandex_login/', auth_views.yandex_login, name='yandex_login'),
    path('vk_login/', auth_views.vk_login, name='vk_login'),
    path('logout/', views.UserViewSet.as_view, {'action': 'logout'}, name='logout'),
    path('', include(router.urls)),
]