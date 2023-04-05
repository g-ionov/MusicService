from django.contrib import admin
from .models import User, Subscribers, SocialMedia, SocialLink
from base.services import get_image_html


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('id', 'username', 'phone', 'email', 'is_staff', 'is_active', 'is_superuser')
    readonly_fields = ('date_joined', 'last_login', 'get_image', 'get_background_image')
    list_display_links = ('id', 'username')

    @staticmethod
    def get_image(obj):
        return get_image_html(obj.main_image, 300)

    @staticmethod
    def get_background_image(obj):
        return get_image_html(obj.background_image, 500)


@admin.register(Subscribers)
class SubscribersAdmin(admin.ModelAdmin):
    list_display = ('user', 'subscriber')


@admin.register(SocialMedia)
class SocialMediaAdmin(admin.ModelAdmin):
    list_display = ('name',)


@admin.register(SocialLink)
class SocialLinkAdmin(admin.ModelAdmin):
    list_display = ('user', 'social_media', 'url')


