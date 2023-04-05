from django.shortcuts import render


def yandex_login(request):
    return render(request, 'users/yandex_login.html')


def vk_login(request):
    return render(request, 'users/vk_login.html')
