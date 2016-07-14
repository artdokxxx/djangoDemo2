from django.shortcuts import render


def main(request):
    return render(request, 'admin/index.html')


def users_list(request):
    return render(request, 'admin/users.html')


def films_list(request):
    #TODO: Сделать страницу + вьюху для управления фильмами
    return render(request, 'admin/index.html')